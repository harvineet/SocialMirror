#This code helps convert the dif_timeline1s to other timelines with standard features for 1000 tweets with only fresh topics
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
from os import listdir
from os.path import isfile, join
fr = open("dif_timeline1s", 'r')
prev = ""
count = 0
count1 = 0
s = set()
fr1 = open("timeline1500hash", 'r')
for line in fr1:
	line = line.rstrip()
	s.add(line)
fr1.close()
fd = open("timeline1500", 'w')
prev = ""
prin = False
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	if u[0] != prev:
		if u[0] in s:
			prin = True
		else:
			prin = False
	if prin:
		fd.write(line + '\n')
	prev = u[0]
fr.close()
fd.close()
