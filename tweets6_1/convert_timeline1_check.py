#s code helps convert the dif_timeline1s to other timelines with standard features for topics with atleast 10 tweets with only fresh topics
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
pred_thr=1500
fd = open("timeline1500hash", 'w')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	if u[0] != prev and prev != "":
		if(count < 5 and count1 >= pred_thr):
			fd.write(prev + '\n')
		count = 0
		count1 = 0
	count1 = count1 + 1
	if int(u[1]) < 1395901801:
		count = count + 1

	prev = u[0]
if(count < 5 and count1 >= pred_thr):
	fd.write(prev + '\n')
fr.close()
fd.close()
