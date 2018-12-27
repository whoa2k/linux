#!/usr/bin/env python

# use higher version than python 2.6 due to datetime module
import os,sys,datetime,calendar

# function to change format from Iconnmr.breif to MS access format 
def icon_to_log(filename):

# input file : as400A-YYYY-MM.brief
# output file name is began with "ext"
	input_file = open(filename,"r")
	tmp_file = open("tmp_"+filename,"w")

	flg_i = "True"
	pre_file = filename[:-14]

	print "%s is converted to lastlog format" %(pre_file)

	for line in input_file:
		
		if line[:7].strip() == "name:" : 
			i_name = line[8:16].strip()
		if line[:15].strip() == "timeOfStart:" :
			begin_date = line[15:25].strip()
			begin_month = begin_date[:2]
			begin_day = begin_date[3:5]
			begin_year = begin_date[6:]
			line_date = begin_year + "-" + begin_month + "-" + begin_day
			begin_time = line[26:34].strip()
			begin_hour = begin_time[:2]
			begin_minute = begin_time[3:5]
			begin_second = begin_time[6:]
			beg_time = begin_hour + ":" + begin_minute

			begin_text = line[35:45].strip('\n')
			begin_linux = int(begin_text)
			
	
		if line[:8] == "#Failure" :
			flg_i = "Fail"

		if line[:20].strip() == "timeOfTermination:" :
			termi_date = line[21:31].strip()
			termi_time = line[32:40].strip()

			termi_hour = termi_time[:2]
			termi_minute = termi_time[3:5]
			termi_second = termi_time[6:]

			ter_time = termi_hour + ":" + termi_minute

			termi_text = line[41:51].strip('\n')
			termi_linux = int(termi_text)

			linux_time = (termi_linux - begin_linux)
			linux_hour = (linux_time/60) // 60
			linux_min  = (linux_time/60) % 60

			if flg_i == "True" :
#				print "%s  %-8s  %s  %s  %02d:%02d %5d %s" %(line_date,i_name,beg_time,ter_time,linux_hour,linux_min,linux_time,pre_file)
				tmp_file.write('%s  %-8s  %s  %s  %02d:%02d %5d %s\n' %(line_date,i_name,beg_time,ter_time,linux_hour,linux_min,linux_time/60,pre_file[:-1]))
			else : flg_i = "True" 
	
	tmp_file.close()
	input_file.close()
	
# select options
# 1. account is not administrater - hsshin, root, reboot,nmrsu
# 2. failed experiment is not included
#  
def select_period(filename):

# 
# outfile name is began with "accept"
	tmp_file = open(filename,"r")
	f_name=filename[4:-6]
	magnet=f_name[:-8]
	s_time=f_name[-7:]

	output_file = open('accept_'+f_name+'.txt',"w")

#	s_year = s_time[:4].strip()
#	s_month = s_time[-2:].strip()
#	s_begin= datetime.date(int(s_year),int(s_month),1)
#	s_tmp  = datetime.date(int(s_year),int(s_month)+1,1)
#	s_end  = s_tmp + datetime.timedelta(days=-1)
#	print f_name,magnet,s_month,s_time
# determine final date of last month log data
#	from time import strptime
#	month_first = datetime.date.today()
#	month_last = month_first - datetime.timedelta(days=1)
# output format is like below
# date (XXXX-XX-XX), id, login time, logout time, usage time(not used), minute(not used), magnet
# value "not used" is not used for MS access usage calculation

	for line in tmp_file:

		s_name =line[12:21].strip()
		check_date=line[:7]
		
		if s_name not in ["hsshin","nightrun","testabc","testuser","whoa","nmrsu"]:	
			if check_date == s_time :
				output_file.write(line)

	tmp_file.close()
	output_file.close()

if __name__ == "__main__":

# log_extract : select valid log line
# format_change : change format for MS access
	icon_to_log(sys.argv[1])
	select_period("tmp_"+sys.argv[1])

