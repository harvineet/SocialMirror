#Python file to create the spread of topics according to parameters alpha and beta and using time decay diffusion of influence model
#adjacency list loaded from follower files using file offset
#grid search for selecting values of parameters, alpha and beta
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

def main(alpha, beta, sim_run):
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

	print 'Map Read\n'
		
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
			return followers
		else:
			adj[node] = set()
			fetched_nodes.add(node) # fetched even if exits from an if loop
			map_id_not_found+=1
			print "offset not found", node #check, remove
			return set()
			
	def load_coupling_pickle(tag):
		if isfile("parametric_spread/coupling/eta_"+tag+".pickle"):
			return pickle.load(open( "parametric_spread/coupling/eta_"+tag+".pickle", "rb" ) )
		else:
			eta = dict()
			pickle.dump(eta, open( "parametric_spread/coupling/eta_"+tag+".pickle", "wb" ) )
			return eta
	def dump_coupling_pickle(tag,eta):
		pickle.dump(eta, open( "parametric_spread/coupling/eta_"+tag+".pickle", "wb" ) )

	tic = time.clock()

	node_nbh = pickle.load(open( "friends_count_user.pickle", "rb" ) )
	print 'Friend count Read\n'

	toc = time.clock()
	#print "time elapsed", toc-tic
	
	print "alpha", alpha
	print "beta", beta
	fr = open('timeline_data/timeline_weng_sample', 'r')
	fd = open("parametric_spread/synthetic_spread_log/"+sim_run+"/"+alpha+"_"+beta+".txt", 'wb')
	fd.write("tagName,alpha,beta,totalSpread,initTweetNum,initTimeTime,totalSynSpread,10000tweetTime\n")

	#alpha = 0.07 #float() #0.01 #1.0
	#beta = 6.3 /3600 #float() # in hours, for underflow
	# (2.0,10.0) # script for different alpha, beta
	# (0.05,6.25)
	alpha = float(alpha)
	beta = float(beta)/3600
	#step_size = 20
	t_limit = 10000
	max_iter = 9000#math.ceil(float(t_limit)/step_size) # considering 1 tweet in 1 step size

	for line in fr:
		
		tic = time.clock()
		
		line = line.rstrip()
		u = line.split(' ')
		init_tweet_num = random.randint(1000,1500) # change for prediction threshold 1500
		init_tweet_time = int(u[init_tweet_num][0:u[init_tweet_num].index(',')])
		coup_prob = load_coupling_pickle(u[0]) # read pre-stored eta values for particular tag and corresponding timepoints of tweets
		print u[0],init_tweet_num,init_tweet_time
		nodes_time = dict()
		nodes = set()
		candidates = set()
		timestamp_col = []
		numTweets = 0
		timestamp = 0
		iterCount = 0
		synTweets = []
		
		for i in range(1, len(u)): 
			timestamp = int(u[i][0:u[i].index(',')])
			timestamp_col.append(timestamp)
			if(i <= init_tweet_num):
				numTweets = i
				author = int(u[i][u[i].index(',')+1 : ])
				author = m[author]
				nodes_time[author] = timestamp
				nodes.add(author)
				
				tic1 = time.clock()
				
				following_nodes=getadj(author)
				
				toc1 = time.clock()
				#print "Adj list query", (toc1-tic1)*1000

				candidates.update(following_nodes) # author not added in candidates
			
		toc = time.clock()
		print "initial real spread", (toc-tic)*1000

		tic = time.clock()
		
		present_time = init_tweet_time
		while numTweets < t_limit:
			
			tic1 = time.clock()
			iterCount+=1
			present_time = timestamp_col[init_tweet_num+iterCount] # next time taken from actual time, not taken
			#present_time += step_size 
			infected_candidates = set()
			for i in candidates:			# neighbours of infected nodes only
				prob_node = 0.0
				
				for j in nodes:
					if i in adj[j]: # check if j already in adj, as j is in nodes or getadj
						try:
							prob_node += math.log(1.0 - alpha*math.exp(-1*beta*(present_time-nodes_time[j]))/ node_nbh[i])
						except:
							id_not_found+=1
				prob_node = 1-math.exp(prob_node)
				# get random prob of coin toss from stored eta values
				if i in coup_prob:
					if present_time in coup_prob[i]:
						eta_prob_coupling = coup_prob[i][present_time]
					else:
						eta_prob_coupling = random.random()
						coup_prob[i][present_time] = eta_prob_coupling
				else:
					coup_prob[i] = dict()
					eta_prob_coupling = random.random() # check if higher precision can be taken
					coup_prob[i][present_time] = eta_prob_coupling
				if (eta_prob_coupling<=prob_node):
					nodes.add(i)
					
					tic2 = time.clock()
					
					following_new_node=getadj(i)
					
					toc2 = time.clock()
					#print "Adj list query", (toc2-tic2)*1000
				
					infected_candidates.update(following_new_node) # i not added in candidates
					nodes_time[i]=present_time
					numTweets+=1
			candidates.update(infected_candidates)
			print (init_tweet_num+iterCount),present_time,numTweets
			synTweets.append(numTweets)
			fd.write(u[0]+","+str(alpha)+","+str(beta)+","+str(len(u))+","+str(init_tweet_num)+","+str(init_tweet_time)+","+str(numTweets)+","+str(present_time)+"\n")
			
			if (iterCount>max_iter):
				break
			if len(synTweets)>10:
				if len(set(synTweets[-10:]))==1:
					break
				_=synTweets.pop(0)
					
			toc1 = time.clock()
			print "Synthetic spread tweet", (toc1-tic1)*1000
			fd.flush()
			
		toc = time.clock()
		print "Synthetic spread topic", (toc-tic)*1000
		
		dump_coupling_pickle(u[0],coup_prob)	
	fd.close()
	fr.close()
	# close file handles of follower list files
	for f in f_read_list:
		f.close()
	print "friends dictionary key not found", id_not_found
	print map_id_not_found

if __name__=='__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))