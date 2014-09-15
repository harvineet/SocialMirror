import json
import sys
import time
import datetime
import dateutil.tz
import calendar
import math
from os import listdir
from os.path import isfile, join

fr = open('tag_tweet_count_201202.csv','r')
fr.readline()
s = set()
for line in fr:
	line = line.rstrip()
	u = line.split(',')
	if(int(u[1]) > 20):
		s.add(u[0])
fr.close()

fr = open('timeline_tag.anony_modified.dat','r')
total = 0
viral = 0
arr = []
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	if(u[1] in s or int(u[0]) < 51):
		continue
	total = total + 1
	#if(int(u[0]) > 1000):
	viral = viral + 1
	dif = int(u[52][0:u[52].find(',')]) - int(u[2][0:u[2].find(',')])
	arr.append(dif)
arr.sort()
fr.close()

fd = open('dump1','w')
for i in arr:
	fd.write(str(i) + '\n')
fd.close()

print total
print viral
