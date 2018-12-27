#!/usr/bin/env python

# use higher version than python 2.6 due to datetime module
import os,sys,datetime,calendar

# function to select valid log line
def log_extract(filename):

# input file : magnet-date.txt
# output file name is began with "ext"
	input_file = open(filename,"r")
	tmp_file = open("ext_"+filename,"w")
	flag_n = "done"
	file_n = filename[:4]

	for line in input_file:
		
		s_name= line[:7].strip()
		s_pts= line[9:14].strip()
		s_src= line[22:39].strip()
		s_week= line[39:42].strip()
		s_month= line[43:46].strip()
		s_begin= line[50:55].strip()
		s_end= line[58:63].strip()
		s_time= line[66:71]
		

# select options
# 1. account is not administrater - hsshin, root, reboot,nmrsu
# 2. usage time is not zero - 00:00
# 3. remote connection is not included - s_src>=6
# 4. system shutdown is not included - line length <=70,line[65]="(",line[58]=0,1,2
#  

		if s_name not in ["hsshin","root","reboot","nmrsu","nightrun","testuser","whoa","testabc"] :
			if s_time<>"00:00":
				if len(s_src) < 5 :
					if len(line)>70 :
						if line[65] == "(" :
							if line[58] in ["0","1","2"] :
								if file_n == "AS400" :
									if s_pts in [":0","0:0"] :
										tmp_file.write(line)	
									else : print line 
								else :
									if s_pts.strip() == "pts/1" :
										tmp_file.write(line)
									else : print line
							else : print line
						else : print line
					else : print line
				else : print line
			else : print line
		else : print line
			
	tmp_file.close()
	input_file.close()
	
# function to change format for MS access
def format_change(filename):

# load selected valid log line
# outfile name is began with "accept"
	input_file = open(filename,"r")
	f_name=filename[4:]
	magnet=f_name[:-12]
	output_file = open("accept_"+f_name,"w")
	
# determine final date of last month log data
	from time import strptime
	today = datetime.date.today()
	first = today.replace(day=1)
	lastMonth = first - datetime.timedelta(days=1)

# output format is like below
# date (XXXX-XX-XX), id, login time, logout time, usage time(not used), minute(not used), magnet
# value "not used" is not used for MS access usage calculation
	for line in input_file :

		kkk_name=line[:8]
		kkk_weekday=line[39:42]
		kkk_month=line[43:46]
		kkk_day=line[47:49]
		kkk_begin=line[50:55]
		kkk_end=line[58:63]
		kkk_usage=line[66:71]
		kkk_last=line[72:]
		
		kkk_year=lastMonth.year
		kkk_month_num=strptime(kkk_month,'%b').tm_mon
		kkk_day_num=int(kkk_day)
		kkk_time=int(kkk_usage[:2])*60 + int(kkk_usage[3:])

		kkk_date=lastMonth.replace(kkk_year,kkk_month_num,kkk_day_num)
		
#		print "%s  %s  %s  %s  %s  %4d %s" %(kkk_date,kkk_name,kkk_begin,kkk_end,kkk_usage,kkk_time,kkk_last)
		if kkk_name not in ["nightrun","testuser","testabc","nmrsu"] :
			output_file.write('%s  %s  %s  %s  %s  %4d %s %s' %(kkk_date,kkk_name,kkk_begin,kkk_end,kkk_usage,kkk_time,magnet,kkk_last))


	input_file.close()
	output_file.close()

if __name__ == "__main__":

# log_extract : select valid log line
# format_change : change format for MS access
	log_extract(sys.argv[1])
	format_change("ext_"+sys.argv[1])

