#python code to evaluate the location data of users
import json
from os import listdir
from os.path import isfile, join

lis = []
fr = open('disam', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	lis.append(u[0].lower())	
fr.close()

#fd = open('unknown1.txt', 'w')
fr = open('unknown1.txt', 'r')
count = 0
for line in fr:
	line = line.rstrip()
	line = line.lower()
	found = False
	for i in lis:
		if line.find(i) > -1:
			found = True
	if found:
		count = count + 1
		continue
fr.close()
print count 
