#python code to get unique locations
import json
from os import listdir
from os.path import isfile, join

lis = set()
count=0
fr = open('location.txt', 'r')
for line in fr:
	line = line.rstrip()
	line = line.lstrip()
	u = line.split('\t')
	if len(u)<2:
		count+=1
		continue
	try:
		lis.add(u[1].lower())	
	except:
		lis.add(u[1])
fr.close()
fr = open('unknown2.txt', 'r')
for line in fr:
	line = line.rstrip()
	line = line.lstrip()
	u = line.split('\t')
	if len(u)<2:
		count+=1
		continue
	try:
		lis.add(u[1].lower())	
	except:
		lis.add(u[1])
fr.close()

print count
print len(lis)
