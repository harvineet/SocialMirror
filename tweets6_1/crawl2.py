import json
import time
import datetime
import re

import calendar
import sys


store = dict()
fr = open('oregon18/time_overlap.txt', 'r')
for i in fr:
	i = i.rstrip()
	u = i.split('\t')
	store[long(u[0])] = long(u[1])
fr.close()

print 'Done\n'
