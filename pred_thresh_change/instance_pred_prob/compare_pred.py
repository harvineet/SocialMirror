tags_1000 = dict()
tweets_1000 = dict()
tags_1500 = dict()
with open('correctly_pred.csv', 'r') as fr:
	next(fr)
	for line in fr:
		line = line.rstrip()
		u = line.split(',')
		if u[0]!='':
			tags_1000[u[0]]=int(u[1])
		if u[3]!='':
			tags_1500[u[3]]=int(u[4])
with open('tweets_considered_1000.csv', 'r') as fr:
	next(fr)
	for line in fr:
		line = line.rstrip()
		u = line.split(',')
		tweets_1000[u[0]]=int(u[1])
		
tag1 = tags_1000.keys()
print len(tag1)
tag2 = tags_1500.keys()
intsc = []
for x in tag1:
	if x not in tag2:
		intsc.append((x,tweets_1000[x]))
print len(intsc)
print intsc