#Python file to create the features related to geography
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
import math
from os import listdir
from os.path import isfile, join

buckets = [-1] * 7697889

numOfSets = 0
pset = []
setSize = []
id_not_found = 0
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

arr = ["user_followers_bigger_graph.txt","user_followers_bigger_graph_2.txt", "user_followers_bigger_graph_i.txt","user_followers_bigger_graph_recrawl_2.txt", "user_followers_bigger_graph_recrawl_3.txt","user_followers_bigger_graph_recrawl.txt"]
#arr = ["user_followers_bigger_graph_i.txt"]
adj = [[]] * 7697889

for i in range(0, 7697889):
	adj[i] = []

m = dict()
fr = open("graph/map.txt")
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	m[int(u[0])] = int(u[1])
fr.close()

print 'Map Read\n'

for i in arr:
	fr = open("graph/" + i,'r')
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if(int(u[0]) > 7697889):
			continue
		if len(u) > 2:
			for j in range(2,len(u)):
				adj[m[int(u[1])]].append(m[int(u[j])])
	fr.close()
	print i

print 'Graph Read\n'

for i in range(0, 7697889):
	adj[i] = set(adj[i])

print 'Graph Set\n'

fr = open('known_locations.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	#print m[int(u[0])]
	try:
		buckets[m[int(u[0])]] = int(u[1])
	except:
		a = 1
fr.close()

fr = open('known_locations1.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	#print m[int(u[0])]
	try:
		buckets[m[int(u[0])]] = int(u[1])
	except:
		a = 1
fr.close()

print 'Location Read\n'

fr = open('timeline_data/timeline_weng', 'r')
fr1 = open('retweeteds_weng', 'r')
fr2 = open('user_mentions_weng', 'r')
fd = open("feature11_check_org_geo.csv", 'w')
fd.write("RatioSecondtoFirst,RatioSelfInitCommu,RatioCrossGeoEdges,#globalAdoptersFollowers,#globalAdopters,#heavyusers,Density,LargestSize,NumEdges,Conduct1,Conduct2,Conduct3,Conduct4,Conduct2d,NumTweets,TimeFirst1000,NoOfAdopters,Conductance,RatioOfSingletons,RatioOfConnectedComponents,InfectedCommunities,UsageEntropy,NumOfRT,NumOfMention,IntraRT,IntraMen,Class\n")
mention_line = "";
u2 = []

retweet_line = "";
u1 = []
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	comm = [0]*141
	timestamp = 0
	nodes = set()
	numTweets = 0
	expose = 0.1
	expose_num = 0.1
	expose_col = []
	timestamp_col = []
	numTweets1 = 0
	numEdges = 0.000001
	numEdgesCrossing = 0
	heavy = 0
	globalAdopters = 0
	exposureGA = 0
	selfInitGeo = 0
	for i in range(1, len(u)):
		timestamp = int(u[i][0:u[i].index(',')])
		numTweets1 = i
		if(timestamp - int(u[1][0:u[1].index(',')]) > 18000 and numTweets1 > 1000):
			break
		if(timestamp - int(u[1][0:u[1].index(',')]) < 18000):
			numTweets = i
		author = int(u[i][u[i].index(',')+1 : ])
		author = m[author]
		
		community = buckets[author]
		if author not in nodes:
			comm[community] = comm[community] + 1
			freshGeo = False
			if comm[community] == 1:
				freshGeo = True
			if len(adj[author]) > 3000:
				heavy = heavy + 1
			expose = expose + len(adj[author])
			expose_num = expose_num + len(adj[author])
			booladopt = True
			for value in nodes:
				if author in adj[value]:
					booladopt = False
					expose_num = expose_num - 1
					numEdges = numEdges + 1
					if(buckets[author] != buckets[value]):
						numEdgesCrossing = numEdgesCrossing + 1
				if value in adj[author]:
					booladopt = False
					expose_num = expose_num - 1
					numEdges = numEdges + 1
					if(buckets[author] != buckets[value]):
						numEdgesCrossing = numEdgesCrossing + 1
			if freshGeo and (not booladopt):
				selfInitGeo = selfInitGeo + 1
			if booladopt:
				globalAdopters = globalAdopters + 1
				exposureGA = exposureGA + len(adj[author])
		nodes.add(author)
		timestamp_col.append(timestamp)
		expose_col.append(float(expose_num)/expose)

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

	large = setSize[0]
	secondLarge = 0
	for p in range(1, len(setSize)):
		if setSize[p] > secondLarge:
			secondLarge = setSize[p]
		if setSize[p] > large:
			secondLarge = large
			large = setSize[p]

	#val5 = int(u[2000][0:u[2000].index(',')]) - int(u[1][0:u[1].index(',')])
	val = int(u[1000][0:u[1000].index(',')]) - int(u[1][0:u[1].index(',')])

	infectCommunit = sum([1 for x in comm if x > 0])
	infectCommunit = infectCommunit + 0.00000001
	n = sum([x for x in comm if x > 0])
	usagee = -sum([(float(x)/n)*math.log((float(x)/n)) for x in comm if x > 0])

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

	intraRT_num = 0
	intraRT_den = 0
	intraMen_num = 0
	intraMen_den = 0
	if(rt_found):
		for i in range(1, len(u1)):
			timestamp1 = int(u1[i][0:u1[i].index(',')])
			if timestamp1 > timestamp:
				break
			author = int(u1[i][u1[i].rfind(',')+1 : ])
			user2 = int(u1[i][u1[i].index(',')+1:u1[i].rfind(',')])
			numRT = numRT + 1
			try:
				author = m[author]
				user2 = m[user2]
			except:
				id_not_found+=1
				continue
			if buckets[author] == -1 or buckets[user2] == -1:
				continue
			intraRT_den = intraRT_den + 1
			if buckets[author] ==  buckets[user2]:
				intraRT_num = intraRT_num + 1

	if(mention_found):
		for i in range(1, len(u2)):
			timestamp1 = int(u2[i][0:u2[i].index(',')])
			if timestamp1 > timestamp:
				break
			author = int(u2[i][u2[i].rfind(',')+1 : ])
			user2 = int(u2[i][u2[i].index(',')+1:u2[i].rfind(',')])
			numMention = numMention + 1
			try:
				author = m[author]
				user2 = m[user2]
			except:
				id_not_found+=1
				continue
			if buckets[author] == -1 or buckets[user2] == -1:
				continue
			intraMen_den = intraMen_den + 1
			if buckets[author] ==  buckets[user2]:
				intraMen_num = intraMen_num + 1	

	val1 = 0
	if(intraRT_den > 0):
		val1 = float(intraRT_num)/intraRT_den
	val2 = 0
	if(intraMen_den > 0):
		val2 = float(intraMen_num)/intraMen_den

	l = len(expose_col) - 1
	expose1 = 0
	expose2 = 0
	expose3 = 0
	expose4 = 0
	expose5 = 0
	expose2d = 0
	try:
		expose1 = (expose_col[l] - expose_col[l-20])*36000000/(timestamp_col[l] - timestamp_col[l-20])
		expose2 = (expose_col[l] - expose_col[l-50])*36000000/(timestamp_col[l] - timestamp_col[l-50])
		expose3 = (expose_col[l] - expose_col[l-100])*36000000/(timestamp_col[l] - timestamp_col[l-100])
		expose4 = (expose_col[l] - expose_col[l-250])*36000000/(timestamp_col[l] - timestamp_col[l-250])
		expose5 = (expose_col[l] - expose_col[l-500])*36000000/(timestamp_col[l] - timestamp_col[l-500])
		pexpose2 = (expose_col[l-50] - expose_col[l-100])*36000000/(timestamp_col[l-50] - timestamp_col[l-100])
		expose2d = (expose2 - pexpose2)*36000000/(timestamp_col[l] - timestamp_col[l-50])
	except:
		print u[0]
	if len(u) > 10000:
		'''fdtemp = open('dumpviral/'+u[0], 'w')
		for i in range(0, len(timestamp_col)):
			fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
		fdtemp.close()'''
		fd.write(str(float(secondLarge)/large)+','+str(selfInitGeo/infectCommunit)+','+str(numEdgesCrossing/numEdges)+','+str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(large)+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(infectCommunit)+','+str(usagee)+','+str(numRT)+','+str(numMention)+','+str(val1)+','+str(val2)+',1\n')
	else:
		'''fdtemp = open('dumpnviral/'+u[0], 'w')
		for i in range(0, len(timestamp_col)):
			fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
		fdtemp.close()'''
		fd.write(str(float(secondLarge)/large)+','+str(selfInitGeo/infectCommunit)+','+str(numEdgesCrossing/numEdges)+','+str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(large)+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(infectCommunit)+','+str(usagee)+','+str(numRT)+','+str(numMention)+','+str(val1)+','+str(val2)+',0\n')
fd.close()
fr.close()
fr1.close()
fr2.close()

print id_not_found