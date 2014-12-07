#This file will traverse all the folders to concantenate the time overlaps
import json
from os import listdir
from os.path import isfile, join

fd = open('time_overlap2.txt', 'w')
root_dir = '/mnt/filer01/round2'
onlydirs = [ f for f in listdir(root_dir) if not isfile(join(root_dir,f)) ]
for i in onlydirs:
	dir_path = join(root_dir,i)
	try:
		fr = open(join(dir_path,'time_overlap.txt'),'r')
		for line in fr:
			fd.write(line)
		fr.close()
	except:
		a = 1

	try:
		fr = open(join(dir_path,'time_overlap1.txt'),'r')
		for line in fr:
			fd.write(line)
		fr.close()
	except:
		a = 1

	try:
		fr = open(join(dir_path,'time_overlap2.txt'),'r')
		for line in fr:
			fd.write(line)
		fr.close()
	except:
		a = 1
		
	print i + ' Done'
	fd.flush()
fd.close()
