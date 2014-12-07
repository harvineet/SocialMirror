#This file will combine crawl1 and crawl2 to tell the number of users that are missing
import json
from os import listdir
from os.path import isfile, join
import datetime

s = dict()
s1 = dict()
fr = open('time_overlap.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	s[u[0]] = int(u[1])
	s1[u[0]] = line
fr.close()

l = []
missing = 0
incomplete = 0
fr = open('time_overlap2.txt', 'r')
fd = open('new_time.txt', 'w')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	if u[0] not in s:
		missing = missing + 1
	elif s[u[0]] >= int(u[2]):	
		incomplete = incomplete + 1
#		print (u[2]) + ' ' + str(s[u[0]])
		#l.append(int(u[2]) - s[u[0]])
		fd.write(s1[u[0]] + '\n')
fr.close()
fd.close()
l.sort()
l.reverse()
#for i in range(0,100):

print missing
print incomplete
