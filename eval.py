#python code to evaluate the location data of users
import json
from os import listdir
from os.path import isfile, join

s = dict()
fr = open('text1', 'r')
temp = 0
for line in fr:
	line = line.rstrip()
	s[line] = temp
	temp = temp + 1
fr.close()

prev_auth = 0
prev_loc = ""
fr = open('location.txt', 'r')
fd = open('known_locations.txt', 'w')
count = 0
for line in fr:
	try:
		line = line.rstrip()
		line = line.lstrip()
		u = line.split('\t')
		if int(u[0]) != prev_auth:
			if prev_loc in s:
				count = count + 1
				fd.write(str(prev_auth) + '\t' + str(s[prev_loc]) + '\n')
			else:
				a = 1
		prev_auth = int(u[0])
		prev_loc = u[1]
	except:
		continue
print count
print s
fr.close()
