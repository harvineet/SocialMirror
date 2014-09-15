#Python file to create the spread of topics according to parameters alpha and beta and using time decay diffusion of influence model
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
import math
import random
from os import listdir
from os.path import isfile, join
#from decimal import *
#getcontext().prec = 28

buckets = [-1] * 7697889

numOfSets = 0
pset = []
setSize = []
id_not_found = 0
friend_id_not_found = 0
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

arr_friend = ["user_friends_bigger_graph.txt","user_friends_bigger_graph_2.txt", "user_friends_bigger_graph_i.txt","user_friends_bigger_graph_recrawl.txt"]
#arr = ["user_followers_bigger_graph_i.txt"]
node_nbh = dict()

adj = [set()] * 7697889

for i in range(0, 7697889):
	adj[i] = set()

m = dict()
fr = open("graph/map.txt")
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	m[int(u[0])] = int(u[1])
fr.close()

print 'Map Read\n'

tic = time.clock()

for i in arr:
	with open("graph/" + i,'r') as fr:
		for line in fr:
			line = line.rstrip()
			u = line.split(' ')
			if(int(u[0]) > 7697889):
				continue
			if len(u) > 2:
				for j in range(2,len(u)):
					adj[m[int(u[1])]].add(m[int(u[j])])
	print i

toc = time.clock()
print "time elapsed", toc-tic

tic = time.clock()

for i in arr_friend:
	with open("graph/" + i,'r') as fr:
		for line in fr:
			line = line.rstrip()
			u = line.split(' ')
			if(int(u[0]) > 7697889):
				continue
			try:
				node_nbh[m[int(u[1])]] = int(u[0])
			except:
				friend_id_not_found += 1
	print i

print 'Graph Read\n'

toc = time.clock()
print "time elapsed1", toc-tic
'''
tic = time.clock()

for i in range(0, 7697889):
	adj[i] = set(adj[i])

print 'Graph Set\n'

toc = time.clock()
print "time elapsed2", toc-tic

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
'''
fr = open('timeline_data/timeline_weng_sample', 'r')
#fr1 = open('retweeteds_weng', 'r')
#fr2 = open('user_mentions_weng', 'r')
fd = open("synthetic_spread_log.txt", 'w')
fd.write("tagName,alpha,beta,totalSpread,initTweetNum,initTimeTime,totalSynSpread,10000tweetTime\n")

alpha = 0.1 #float() #0.01 #1.0
beta = 5.0 /3600 #float() # in hours, for underflow
step_size = 20
t_limit = 10000
max_iter = 9500#math.ceil(float(t_limit)/step_size) # considering 1 tweet in 1 step size

#mention_line = "";
#u2 = []

#retweet_line = "";
#u1 = []

for line in fr:
	
	tic = time.clock()
	
	line = line.rstrip()
	u = line.split(' ')
	init_tweet_num = random.randint(500,1000)
	init_tweet_time = int(u[init_tweet_num][0:u[init_tweet_num].index(',')])
	print u[0],init_tweet_num,init_tweet_time
	nodes_time = dict()
	nodes = set()
		
	'''comm = [0]*141
	expose = 0.1
	expose_num = 0.1
	expose_col = []
	timestamp_col = []
	numEdges = 0.000001
	numEdgesCrossing = 0
	heavy = 0
	globalAdopters = 0
	exposureGA = 0
	selfInitGeo = 0'''
	numTweets = 0
	timestamp = 0
	iterCount = 0
	synTweets = []
	
	for i in range(1, len(u)):
		timestamp = int(u[i][0:u[i].index(',')])
		numTweets = i
		if(numTweets > init_tweet_num):
			break
		author = int(u[i][u[i].index(',')+1 : ])
		author = m[author]
		nodes_time[author] = timestamp
		nodes.add(author)
		
	toc = time.clock()
	print "time elapsed3", toc-tic

	tic = time.clock()
	
	present_time = init_tweet_time
	while numTweets < t_limit:
	
		tic = time.clock()
		
		present_time += step_size
		for i in range(0, 7697889):			
			prob_node = 0.0
			
			for j in nodes:
				if i in adj[j]:
					try:
						prob_node += math.log(1.0 - alpha*math.exp(-1*beta*(present_time-nodes_time[j]))/ node_nbh[i])
					except:
						id_not_found+=1
			prob_node = 1-math.exp(prob_node)
			if (random.random()<=prob_node):
				nodes.add(i)
				nodes_time[i]=present_time
				numTweets+=1
		print present_time,numTweets
		synTweets.append(numTweets)
		fd.write(u[0]+","+str(alpha)+","+str(beta)+","+str(len(u))+","+str(init_tweet_num)+","+str(init_tweet_time)+","+str(numTweets)+","+str(present_time)+"\n")
		iterCount+=1
		if (iterCount>max_iter):
			break
		if len(synTweets)>10:
			if len(set(synTweets[-10:]))==1:
				break
			_=synTweets.pop(0)
				
		toc = time.clock()
		print "time elapsed4", toc-tic
		fd.flush()
		
	toc = time.clock()
	print "time elapsed5", toc-tic
	
	"""community = buckets[author]
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
	val = int(u[pt][0:u[pt].index(',')]) - int(u[1][0:u[1].index(',')])

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
		fd.write(str(pt)+','+str(u[0])+','+str(float(secondLarge)/large)+','+str(selfInitGeo/infectCommunit)+','+str(numEdgesCrossing/numEdges)+','+str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(large)+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(infectCommunit)+','+str(usagee)+','+str(numRT)+','+str(numMention)+','+str(val1)+','+str(val2)+',1\n')
	else:
		'''fdtemp = open('dumpnviral/'+u[0], 'w')
		for i in range(0, len(timestamp_col)):
			fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
		fdtemp.close()'''
		fd.write(str(pt)+','+str(u[0])+','+str(float(secondLarge)/large)+','+str(selfInitGeo/infectCommunit)+','+str(numEdgesCrossing/numEdges)+','+str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(large)+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(infectCommunit)+','+str(usagee)+','+str(numRT)+','+str(numMention)+','+str(val1)+','+str(val2)+',0\n')"""
fd.close()
fr.close()
#fr1.close()
#fr2.close()

print "friends dictionary key not found", id_not_found
print friend_id_not_found