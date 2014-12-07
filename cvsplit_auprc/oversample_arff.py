# oversample viral topics in arff train file
import random

for i in range(1,11):
	sample = []
	majority = []
	oversample = []
	header=''
	fr = open('data/train/train'+str(i)+'.arff', 'r')
	count = 0
	for line in fr:
		header+=line
		count+=1
		if count == 31: break
	for line in fr:
		line = line.rstrip()
		u = line.split(',')
		if(u[-1]=='1'):
			sample.append(line)
		else:
			majority.append(line)
	fr.close()
	maj_num = len(majority)
	min_num = len(sample)
	while (9*(len(oversample)+min_num)<maj_num): #len(sample)
		oversample.append(random.choice(sample))
	sample += oversample
	sample += majority
	with open('data/train'+str(i)+'_oversample.arff', 'wb') as fd:
		fd.write(header)
		for line in sample:
			fd.write(line+"\n")
	fr.close()