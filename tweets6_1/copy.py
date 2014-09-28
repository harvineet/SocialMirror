#file to check duplicate filenames in AMAZON folders
import os

# path = '/mnt/filer01/Crawl1_extracts/AMAZON_Crawl1'
dir = []
dup=[]
for d in os.listdir('./AMAZON_Crawl1'):
	if os.path.isdir(os.path.join('./AMAZON_Crawl1',d)):
		for i in os.listdir(os.path.join('./AMAZON_Crawl1',d)):
			if i in dir:
				print "repeat filename", d, i
				dup.append(i)
			dir.append(i)
			
print len(dir), len(set(dir))
print dup
print set(dup)