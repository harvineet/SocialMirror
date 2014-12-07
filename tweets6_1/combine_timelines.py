#this file will be used to combine the different timelines.txt
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
from os import listdir
from os.path import isfile, join
root_dir = '/mnt/filer01/AMAZON'
onlydirs = [ f for f in listdir(root_dir) if not isfile(join(root_dir,f)) ]
start = int(int(sys.argv[1]))
end = int(sys.argv[2])
fr = open("/twitterSimulations/filtered.txt",'r')
s = set()
for line in fr:
	line = line.rstrip()
	s.add(int(line))
fr.close()
count = 0
fd = open("user_mention1", 'w')
for i in onlydirs:
	if count < start or count >= end:
		continue
	count = count + 1
	dir_path = join(root_dir,i)
	try:
		fr = open(join(dir_path,'user_mention.txt'),'r')
		for line in fr:
			line = line.rstrip()
			u = line.split('\t')
			if(int(u[2]) >= 1395858601	 and int(u[2]) <= 1398796199):
				if(int(u[3]) in s):
					fd.write(u[0] + '\t' + u[2] + '\t' + u[3] + '\t' + u[1] +'\n')
		fr.close()
	except:
		a = 1
	try:
		fr = open(join(dir_path,'user_mention1.txt'),'r')
		for line in fr:
			line = line.rstrip()
			u = line.split('\t')
			if(int(u[2]) >= 1395858601 and int(u[2]) <= 1398796199):
				if(int(u[3]) in s):
					fd.write(u[0] + '\t' + u[2] + '\t' + u[3] + '\t' + u[1] +'\n')
		fr.close()
	except:
		a = 1
	print i
fd.close()
