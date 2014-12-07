#This file filters all the users in the domain of interest
#29th April 2014	--	 27th March 2014
# 1398796199 -- 1395858601
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
        s1[u[0]] = int(u[2])
fr.close()

l = []
missing = 0
incomplete = 0
fr = open('time_overlap2.txt', 'r')
fd = open('filtered.txt', 'w')
for line in fr:
        line = line.rstrip()
        u = line.split('\t')
        if u[0] not in s:
            missing = missing + 1
        elif s[u[0]] < int(u[2]):      
            incomplete = incomplete + 1
        else:
        	if s1[u[0]] < 1395858601:
        		fd.write(u[0] + '\n')
fr.close()
fd.close()
#for i in range(0,100):

print missing
print incomplete
