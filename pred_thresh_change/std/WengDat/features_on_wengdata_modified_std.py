#Python file to create the features related to geography
#n file to create the features related to geography
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
import math
from os import listdir
from os.path import isfile, join

numOfSets = 0
pset = []
setSize = []
def initSet(n):
	global pset
	pset = [0]*n
	global setSize
	setSize = [1]*n
	global numOfSets
	numOfSets = n
	for i in range(0, n):
		pset[i] = i

def findSet(a):
	global pset
	if pset[a] == a:
		return a
	else:		
		pset[a] = findSet(pset[a])
		return pset[a]

def isSameSet(a, b):
	if findSet(a) == findSet(b):
		return True
	else:
		return False

def MergeSet(a, b):
	if not isSameSet(a,b):
		global numOfSets
		numOfSets = numOfSets - 1
		global setSize
		setSize[findSet(b)] = setSize[findSet(b)] + setSize[findSet(a)]
		setSize[findSet(a)] = 0
		global pset		
		pset[findSet(a)] = findSet(b)

def average(s): return sum(s) * 1.0 / len(s)

def stdev(s):
	if len(s)!=0:
		avg = average(s)
		variance = map(lambda x: (x - avg)**2, s)
		return math.sqrt(average(variance))
	else:
		return 0

arr = ["follower_gcc.anony.dat"]
adj = [[]] * 600000

for i in range(0, 600000):
	adj[i] = []

for i in arr:
	fr = open("/twitterSimulations/virality2013/" + i,'r')
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if(int(u[0]) > 595460):
			continue
		if(int(u[1]) > 595460):
			continue
		adj[int(u[1])].append(int(u[0]))
		adj[int(u[0])].append(int(u[1]))
	fr.close()
	print i

print 'Graph Read\n'

for i in range(0, 600000):
	adj[i] = set(adj[i])

print 'Graph Set\n'


fr = open('virality2013/weng_line_format', 'r')
fr1 = open('virality2013/timeline_tag_rt.anony.dat', 'r')
fr2 = open('virality2013/timeline_tag_men.anony.dat', 'r')
fd = open("feature_wengdata_modified_5509_std.csv", 'w')
fd.write("#globalAdoptersFollowers,#globalAdopters,#heavyusers,Density,LargestSize,NumEdges,Conduct1,Conduct2,Conduct2d,Conduct1_std,Conduct2_std,Conduct2d_std,Conductance_std,NumTweets,TimeFirst1000,NoOfAdopters,Conductance,RatioOfSingletons,RatioOfConnectedComponents,NumOfRT,NumOfMention,Class\n")
mention_line = "";
u2 = []

retweet_line = "";
u1 = []
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	if len(u) <= 50:
		continue
	timestamp = 0
	nodes = set()
	numTweets = 0
	expose = 0.1
	expose_num = 0.1
	expose_col = []
	timestamp_col = []
	numTweets1 = 0
	numEdges = 0.000001
	heavy = 0
	globalAdopters = 0
	exposureGA = 0
	for i in range(1, len(u)):
		timestamp = int(u[i][0:u[i].index(',')])
		numTweets1 = i
		if(numTweets1 > 50):
			break
		#if(timestamp - int(u[1][0:u[1].index(',')]) < 18000):
		numTweets = i
		author = int(u[i][u[i].index(',')+1 : ])
		if author > 595460:
			continue

		if author not in nodes:
			if len(adj[author]) > 1000:
				heavy = heavy + 1
			expose = expose + len(adj[author])
			expose_num = expose_num + len(adj[author])
			booladopt = True
			for value in nodes:
				if author in adj[value]:
					booladopt = False
					expose_num = expose_num - 1
					numEdges = numEdges + 1
				if value in adj[author]:
					booladopt = False
					expose_num = expose_num - 1
					numEdges = numEdges + 1
			if booladopt:
				globalAdopters = globalAdopters + 1
				exposureGA = exposureGA + len(adj[author])
		nodes.add(author)
		timestamp_col.append(timestamp)
		expose_col.append(float(expose_num)/expose)
	if(len(nodes) == 0):
		continue 

	nodes = list(nodes)
	initSet(len(nodes))
	singleton = len(nodes)
	
	for i in range(0, len(nodes)):
		for j in range(0, i):
			temp1 = (nodes[j] in adj[nodes[i]])
			temp2 = (nodes[i] in adj[nodes[j]]) 
			if temp1 or temp2:
				if setSize[findSet(i)] == 1:
					singleton = singleton - 1
				if setSize[findSet(j)] == 1:
					singleton = singleton - 1
				MergeSet(i, j)


	val = int(u[50][0:u[50].index(',')]) - int(u[1][0:u[1].index(',')])


	mention_found = False
	rt_found = False

	if retweet_line == "":
		retweet_line = fr1.readline()
		retweet_line = retweet_line.rstrip()
		u1 = retweet_line.split(' ')

	while retweet_line and u[0] > u1[0]:
		retweet_line = fr1.readline()
		retweet_line = retweet_line.rstrip()
		u1 = retweet_line.split(' ')

	if retweet_line and u1[0] == u[0]:
		#print 'Hola ' + u[0]
		rt_found = True

	if mention_line == "":
		mention_line = fr2.readline()
		mention_line = mention_line.rstrip()
		u2 = mention_line.split(' ')

	while mention_line and u[0] > u2[0]:
		mention_line = fr2.readline()
		mention_line = mention_line.rstrip()
		u2 = mention_line.split(' ')

	if mention_line and u2[0] == u[0]:
		mention_found = True	


	numRT = 0
	numMention = 0

	if(rt_found):
		for i in range(1, len(u1)):
			timestamp1 = int(u1[i][0:u1[i].index(',')])
			if timestamp1 > timestamp:
				break
			author = int(u1[i][u1[i].rfind(',')+1 : ])
			user2 = int(u1[i][u1[i].index(',')+1:u1[i].rfind(',')])
			numRT = numRT + 1

	if(mention_found):
		for i in range(1, len(u2)):
			timestamp1 = int(u2[i][0:u2[i].index(',')])
			if timestamp1 > timestamp:
				break
			author = int(u2[i][u2[i].rfind(',')+1 : ])
			user2 = int(u2[i][u2[i].index(',')+1:u2[i].rfind(',')])
			numMention = numMention + 1


	l = len(expose_col) - 1
	expose1 = 0
	expose2 = 0
	expose3 = 0
	expose4 = 0
	expose5 = 0
	expose2d = 0
	num_std_values=10
	c_expose1 = []
	c_expose2 = []
	c_expose2d = []
	c_cond = expose_col[-num_std_values:]
	for i in reversed(range(0,num_std_values)):
		try:
			expose1 = (expose_col[l-i] - expose_col[l-i-20])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-20])
			c_expose1.append(expose1)
			if (i==0):
				expose2 = (expose_col[l-i] - expose_col[l-i-49])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-49])
			else:
				expose2 = (expose_col[l-i] - expose_col[0])*36000000/(timestamp_col[l-i] - timestamp_col[0])
			c_expose2.append(expose2)
			#expose3 = (expose_col[l] - expose_col[l-100])*36000000/(timestamp_col[l] - timestamp_col[l-100])
			#expose4 = (expose_col[l] - expose_col[l-250])*36000000/(timestamp_col[l] - timestamp_col[l-250])
			#expose5 = (expose_col[l] - expose_col[l-500])*36000000/(timestamp_col[l] - timestamp_col[l-500])
			if (i==10):
				pexpose2 = (expose_col[l-i-20] - expose_col[0])*36000000/(timestamp_col[l-i-20] - timestamp_col[0])
				expose2d = (expose2 - pexpose2)*36000000/(timestamp_col[l-i] - timestamp_col[0])
			else:
				pexpose2 = (expose_col[l-i-20] - expose_col[l-i-40])*36000000/(timestamp_col[l-i-20] - timestamp_col[l-i-40])
				expose2d = (expose2 - pexpose2)*36000000/(timestamp_col[l-i] - timestamp_col[l-i-40])
			c_expose2d.append(expose2d)
		except:
			print u[0]
	if len(u) > 399:
		'''fdtemp = open('dumpviral/'+u[0], 'w')
		for i in range(0, len(timestamp_col)):
			fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
		fdtemp.close()'''
		fd.write(str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(max(setSize))+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose2d)+','+str(stdev(c_expose1))+','+str(stdev(c_expose2))+','+str(stdev(c_expose2d))+','+str(stdev(c_cond))+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(numRT)+','+str(numMention)+',1\n')
	else:
		'''fdtemp = open('dumpnviral/'+u[0], 'w')
		for i in range(0, len(timestamp_col)):
			fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
		fdtemp.close()'''
		fd.write(str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(max(setSize))+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose2d)+','+str(stdev(c_expose1))+','+str(stdev(c_expose2))+','+str(stdev(c_expose2d))+','+str(stdev(c_cond))+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(numRT)+','+str(numMention)+',0\n')
fd.close()
fr.close()
fr1.close()
fr2.close()

