# file to create the features for different prediction thresholds where virality threshold and set of topics remains same, adding std of conductance features #correction for self-initiated adopters and addition of tweeting entropy, number of adopters of followers
#using conductance and vertex expansion
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
import math
import random
import cPickle as pickle
from os import listdir
from os.path import isfile, join
#from decimal import *
#getcontext().prec = 28

buckets = [-1] * 7697889

numOfSets = 0
pset = []
setSize = []	
adj = dict() # check memory use, list of sets or list of lists
fetched_nodes = set()
id_not_found = 0
map_id_not_found = 0	
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
# open follower list files and store handles in a list
f_read_list = []
for i in arr:
	f_read_list.append(open("graph/" + i,'rb'))
	
line_offset = pickle.load( open( "follower_file_offset.pickle", "rb" ) )
print 'Follower file offset Read\n'

m = pickle.load(open( "map_user_index.pickle", "rb" ) )
'''fr = open("graph/map.txt")
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	m[int(u[0])] = int(u[1])
fr.close()'''

print 'Map Read\n'

'''adj = [[]] * 7697889
for i in range(0, 7697889):
	adj[i] = []'''
	
def getsechop(nodes):
	global adj
	global fetched_nodes
	global map_id_not_found
	for node in nodes:
		if node in fetched_nodes:
			return adj[node]
		elif node in line_offset:
			adj[node] = set()
			followers = set()
			fetched_nodes.add(node) # fetched even if exits from an if loop
			(file_count, offset) = line_offset[node] # node is mapped id, check if node in line_offset
			f_read_list[file_count].seek(offset)
			line = f_read_list[file_count].readline()
			line = line.rstrip()
			u = line.split(' ')
			if(int(u[0]) > 7697889):
				print "Number of followers exceeded" #check, remove
				return None
			if len(u) <= 2:
				print "no follower list"
				return set()
			#print line_offset[node]
			#print m[int(u[1])],node
			if m[int(u[1])]!=node:
				print "Error in index" #check, remove
				sys.exit(0) #check, remove
			for j in range(2,len(u)): # get two-hops list also
				followers.add(m[int(u[j])]) # check if u[j] in m
				#adj[node].add(m[int(u[j])])
			adj[node].update(followers)
			return followers
		else:
			adj[node] = set()
			fetched_nodes.add(node) # fetched even if exits from an if loop
			map_id_not_found+=1
			print "offset not found", node #check, remove
			return set()
		
def getadj(node):
	global adj
	global fetched_nodes
	global map_id_not_found
	if node in fetched_nodes:
		return adj[node]
	elif node in line_offset:
		adj[node] = set()
		followers = set()
		fetched_nodes.add(node) # fetched even if exits from an if loop
		(file_count, offset) = line_offset[node] # node is mapped id, check if node in line_offset
		f_read_list[file_count].seek(offset)
		line = f_read_list[file_count].readline()
		line = line.rstrip()
		u = line.split(' ')
		if(int(u[0]) > 7697889):
			print "Number of followers exceeded" #check, remove
			return None
		if len(u) <= 2:
			print "no follower list"
			return set()
		#print line_offset[node]
		#print m[int(u[1])],node
		if m[int(u[1])]!=node:
			print "Error in index" #check, remove
			sys.exit(0) #check, remove
		for j in range(2,len(u)): # get two-hops list also
			followers.add(m[int(u[j])]) # check if u[j] in m
			#adj[node].add(m[int(u[j])])
		adj[node].update(followers)
		_=getsechop(followers)
		return followers
	else:
		adj[node] = set()
		fetched_nodes.add(node) # fetched even if exits from an if loop
		map_id_not_found+=1
		print "offset not found", node #check, remove
		return set()

'''arr_friend = ["user_friends_bigger_graph.txt","user_friends_bigger_graph_2.txt", "user_friends_bigger_graph_i.txt","user_friends_bigger_graph_recrawl.txt"]'''
#arr = ["user_followers_bigger_graph_i.txt"]


def average(s): return sum(s) * 1.0 / len(s)

def stdev(s):
	if len(s)!=0:
		avg = average(s)
		variance = map(lambda x: (x - avg)**2, s)
		return math.sqrt(average(variance))
	else:
		return 0



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

# fr = open('timeline_data/timeline_weng', 'r')
# fr1 = open('retweeteds_weng', 'r')
# fr2 = open('user_mentions_weng', 'r')
# fd = open("feature_1000_no5hr.csv", 'w')
# fd.write("TagName,RatioSecondtoFirst,RatioSelfInitCommu,RatioCrossGeoEdges,#globalAdoptersFollowers,#globalAdopters,#heavyusers,Density,LargestSize,NumEdges,Conduct1,Conduct2,Conduct3,Conduct4,Conduct2d,NumTweets,TimeFirst1000,NoOfAdopters,Conductance,RatioOfSingletons,RatioOfConnectedComponents,InfectedCommunities,UsageEntropy,NumOfRT,NumOfMention,IntraRT,IntraMen,Class\n")
# mention_line = "";
# u2 = []

# retweet_line = "";
# u1 = []
tic = time.clock()
for pred_thr in [1500,250,500,1000,2000,2500]:#200,250,500,750,1000,
	fr = open('timeline_data/timeline_weng', 'r')
	fr1 = open('retweeteds_weng', 'r')
	fr2 = open('user_mentions_weng', 'r')
	fd=open("./conductance_std_features_td/cond_ve_features/feature_"+str(pred_thr)+".csv",'w')
	fd_cond=open("./conductance_std_features_td/cond_ve_features/cond_values_all/feature_"+str(pred_thr)+".csv",'w')
	fd.write("TagName,RatioSecondtoFirst,RatioSelfInitCommu,RatioCrossGeoEdges,#globalSelfInitAdoptersFollowers,#globalAdopters,#heavyusers,Density,LargestSize,NumEdges,Conduct1,Conduct2,Conduct3,Conduct4,Conduct2d,NumTweets,TimeFirst1000,NoOfAdopters,Conductance,RatioOfSingletons,RatioOfConnectedComponents,InfectedCommunities,UsageEntropy,NumOfRT,NumOfMention,IntraRT,IntraMen,UsageEntropyTweets,#globalAdoptersFollowers,Conduct1_std,Conduct2_std,Conduct3_std,Conduct4_std,Conduct2d_std,Conductance_std,Conduct1_ve,Conduct2_ve,Conduct3_ve,Conduct4_ve,Conduct2d_ve,Conductance_ve,Conduct1_vestd,Conduct2_vestd,Conduct3_vestd,Conduct4_vestd,Conduct2d_vestd,Conductance_vestd,Class\n")
	if(pred_thr==200):
		cond_values_all = ",".join(["Cond"+str(c) for c in reversed(range(200))])
	elif(pred_thr==250):
		cond_values_all = ",".join(["Cond"+str(c) for c in reversed(range(250))])
	else:
		cond_values_all = ",".join(["Cond"+str(c) for c in reversed(range(251))])
	fd_cond.write("TagName,"+cond_values_all+",Class\n")
	mention_line = "";
	u2 = []
	retweet_line = "";
	u1 = []
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		#moving window conductance features
		comm = [0]*141
		comm_tweets = [0]*141
		timestamp = 0
		nodes = set()
		numTweets = 0
		expose = 0.1
		expose_num = 0.1
		expose_col = [] #conductance
		expose_ve_col = [] #vertex expansion
		timestamp_col = []
		numTweets1 = 0
		numEdges = 0.000001
		numEdgesCrossing = 0
		heavy = 0
		globalAdopters = 0
		globalFollowerAdopters_set = set()
		globalFollowerAdopters = 0
		exposureGA = 0
		selfInitGeo = 0
		for i in range(1, len(u)):
			timestamp = int(u[i][0:u[i].index(',')])
			numTweets1 = i
			if(numTweets1 > pred_thr):
				break
			#if(timestamp - int(u[1][0:u[1].index(',')]) < 18000):
			numTweets = i
			author = int(u[i][u[i].index(',')+1 : ])
			author = m[author]
			
			community = buckets[author]
			comm_tweets[community] = comm_tweets[community] + 1
			if author not in nodes:
				comm[community] = comm[community] + 1
				freshGeo = False
				if comm[community] == 1:
					freshGeo = True
				if len(getadj(author)) > 3000:
					heavy = heavy + 1
				globalFollowerAdopters_set.update(getadj(author))
				if author in globalFollowerAdopters_set:
					globalFollowerAdopters_set.remove(author)
				expose = expose + len(getadj(author))
				expose_num = expose_num + len(getadj(author))
				booladopt = True
				for value in nodes:
					if author in getadj(value):
						booladopt = False
						expose_num = expose_num - 1
						numEdges = numEdges + 1
						if(buckets[author] != buckets[value]):
							numEdgesCrossing = numEdgesCrossing + 1
					if value in getadj(author):
						booladopt = False
						expose_num = expose_num - 1
						globalFollowerAdopters_set.remove(value)
						numEdges = numEdges + 1
						if(buckets[author] != buckets[value]):
							numEdgesCrossing = numEdgesCrossing + 1
				if freshGeo and booladopt:
					selfInitGeo = selfInitGeo + 1
				if booladopt:
					globalAdopters = globalAdopters + 1
					exposureGA = exposureGA + len(getadj(author))
				globalFollowerAdopters = len(globalFollowerAdopters_set)
			nodes.add(author)
			timestamp_col.append(timestamp)
			expose_col.append(float(expose_num)/expose)
			# expose_col.append(float(expose_num)/len(nodes))
			expose_ve_col.append(float(globalFollowerAdopters)/len(nodes))

		nodes = list(nodes)
		initSet(len(nodes))
		singleton = len(nodes)
		
		for i in range(0, len(nodes)):
			for j in range(0, i):
				temp1 = (nodes[j] in getadj(nodes[i]))
				temp2 = (nodes[i] in getadj(nodes[j])) 
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
		val = int(u[pred_thr][0:u[pred_thr].index(',')]) - int(u[1][0:u[1].index(',')])

		infectCommunit = sum([1 for x in comm if x > 0])
		infectCommunit = infectCommunit + 0.00000001
		n = sum([x for x in comm if x > 0])
		usagee = -sum([(float(x)/n)*math.log((float(x)/n)) for x in comm if x > 0])
		usagee_tweets = -sum([(float(x)/n)*math.log((float(x)/n)) for x in comm_tweets if x > 0])

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
		#expose5 = 0
		expose2d = 0
		
		c_expose1 = []
		c_expose2 = []
		c_expose3 = []
		c_expose4 = []
		#c_expose5 = []
		c_expose2d = []
		c_cond = expose_col[-100:]
		for i in reversed(range(0,100)):
			try:
				expose1 = (expose_col[l-i] - expose_col[l-i-20])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-20])
				c_expose1.append(expose1)
				expose2 = (expose_col[l-i] - expose_col[l-i-50])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-50])
				c_expose2.append(expose2)
				expose3 = (expose_col[l-i] - expose_col[l-i-100])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-100])
				c_expose3.append(expose3)
				pexpose2 = (expose_col[l-i-50] - expose_col[l-i-100])*36000000/(timestamp_col[l-i-50] - timestamp_col[l-i-100])
				expose2d = (expose2 - pexpose2)*36000000/(timestamp_col[l-i] - timestamp_col[l-i-50])
				c_expose2d.append(expose2d)
				if(pred_thr==200 or pred_thr==250):
					expose4 = (expose_col[l-i] - expose_col[0])*36000000/(timestamp_col[l-i] - timestamp_col[0]) # 250 not correct, changes for different i
					c_expose4.append(expose4)
				else:
					expose4 = (expose_col[l-i] - expose_col[l-i-250])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-250])
					c_expose4.append(expose4)
				#expose5 = (expose_col[l] - expose_col[l-500])*36000000/(timestamp_col[l] - timestamp_col[l-500])
			except:
				print u[0]
		l = len(expose_ve_col) - 1
		expose1_ve = 0
		expose2_ve = 0
		expose3_ve = 0
		expose4_ve = 0
		#expose5 = 0
		expose2d_ve = 0
		
		c_expose1_ve = []
		c_expose2_ve = []
		c_expose3_ve = []
		c_expose4_ve = []
		#c_expose5 = []
		c_expose2d_ve = []
		c_cond_ve = expose_ve_col[-100:]
		for i in reversed(range(0,100)):
			try:
				expose1_ve = (expose_ve_col[l-i] - expose_ve_col[l-i-20])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-20])
				c_expose1_ve.append(expose1_ve)
				expose2_ve = (expose_ve_col[l-i] - expose_ve_col[l-i-50])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-50])
				c_expose2_ve.append(expose2_ve)
				expose3_ve = (expose_ve_col[l-i] - expose_ve_col[l-i-100])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-100])
				c_expose3_ve.append(expose3_ve)
				pexpose2_ve = (expose_ve_col[l-i-50] - expose_ve_col[l-i-100])*36000000/(timestamp_col[l-i-50] - timestamp_col[l-i-100])
				expose2d_ve = (expose2_ve - pexpose2_ve)*36000000/(timestamp_col[l-i] - timestamp_col[l-i-50])
				c_expose2d_ve.append(expose2d_ve)
				if(pred_thr==200 or pred_thr==250):
					expose4_ve = (expose_ve_col[l-i] - expose_ve_col[0])*36000000/(timestamp_col[l-i] - timestamp_col[0]) # 250 not correct, changes for different i
					c_expose4_ve.append(expose4_ve)
				else:
					expose4_ve = (expose_ve_col[l-i] - expose_ve_col[l-i-250])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-250])
					c_expose4_ve.append(expose4_ve)
				#expose5 = (expose_ve_col[l] - expose_ve_col[l-500])*36000000/(timestamp_col[l] - timestamp_col[l-500])
			except:
				print u[0]
		if len(u) > 10000:
			'''fdtemp = open('dumpviral/'+u[0], 'w')
			for i in range(0, len(timestamp_col)):
				fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
			fdtemp.close()'''
			fd.write(str(u[0])+','+str(float(secondLarge)/large)+','+str(selfInitGeo/infectCommunit)+','+str(numEdgesCrossing/numEdges)+','+str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(large)+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(infectCommunit)+','+str(usagee)+','+str(numRT)+','+str(numMention)+','+str(val1)+','+str(val2)+','+str(usagee_tweets)+','+str(globalFollowerAdopters)+','+str(stdev(c_expose1))+','+str(stdev(c_expose2))+','+str(stdev(c_expose3))+','+str(stdev(c_expose4))+','+str(stdev(c_expose2d))+','+str(stdev(c_cond))+',' + str(expose1_ve)+','+str(expose2_ve)+','+str(expose3_ve)+','+str(expose4_ve)+','+str(expose2d_ve)+','+str(float(globalFollowerAdopters)/len(nodes))+','+str(stdev(c_expose1_ve))+','+str(stdev(c_expose2_ve))+','+str(stdev(c_expose3_ve))+','+str(stdev(c_expose4_ve))+','+str(stdev(c_expose2d_ve))+','+str(stdev(c_cond_ve))+',1\n')
			
			fd_cond.write(str(u[0])+','+','.join(str(x) for x in expose_col[-251:])+',1\n')
		else:
			'''fdtemp = open('dumpnviral/'+u[0], 'w')
			for i in range(0, len(timestamp_col)):
				fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
			fdtemp.close()'''
			fd.write(str(u[0])+','+str(float(secondLarge)/large)+','+str(selfInitGeo/infectCommunit)+','+str(numEdgesCrossing/numEdges)+','+str(exposureGA)+','+str(globalAdopters)+','+str(heavy)+','+str(float(numEdges)/len(nodes))+','+str(large)+','+str(numEdges)+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+str(numTweets)+','+str(val)+','+str(len(nodes))+','+str(float(expose_num)/expose)+','+str(float(singleton)/len(nodes))+','+str(float(numOfSets)/len(nodes))+','+str(infectCommunit)+','+str(usagee)+','+str(numRT)+','+str(numMention)+','+str(val1)+','+str(val2)+','+str(usagee_tweets)+','+str(globalFollowerAdopters)+','+str(stdev(c_expose1))+','+str(stdev(c_expose2))+','+str(stdev(c_expose3))+','+str(stdev(c_expose4))+','+str(stdev(c_expose2d))+','+str(stdev(c_cond))+',' + str(expose1_ve)+','+str(expose2_ve)+','+str(expose3_ve)+','+str(expose4_ve)+','+str(expose2d_ve)+','+str(float(globalFollowerAdopters)/len(nodes))+','+str(stdev(c_expose1_ve))+','+str(stdev(c_expose2_ve))+','+str(stdev(c_expose3_ve))+','+str(stdev(c_expose4_ve))+','+str(stdev(c_expose2d_ve))+','+str(stdev(c_cond_ve))+',0\n')
			
			fd_cond.write(str(u[0])+','+','.join(str(x) for x in expose_col[-251:])+',0\n')
	fd.close()
	fd_cond.close()
	fr.close()
	fr1.close()
	fr2.close()

print id_not_found
toc = time.clock()
print "time elapsed", toc-tic