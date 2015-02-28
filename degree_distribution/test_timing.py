#extract hashtag graphs from sequence of authors adopting a hashtag and find all paths in the graphs to write into corpus file as sentences for training using word2vec 
import time
import sys
import os
import cPickle as pickle

min_tweets_sequence = 10 # minimum number of tweets on a hashtag to remove hashtags with only few tweets available for extracting context

#conditions for edges between tweets
time_diff_for_edge = 12*60*60
# time_diff_for_edge = 12*60*60
follower_following_cond = False
geography_cond = False

min_context_length = 10 #minimum length of context or length of paths to consider

#read adoption sequence from dif_timeline1s file
adoption_sequence = dict()
with open('/twitterSimulations/timeline_data/dif_timeline1s', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		tag = u[0]
		time = int(u[1])
		author = int(u[2])
		if tag not in adoption_sequence:
			adoption_sequence[tag]=[]
		adoption_sequence[tag].append((time,author))
		# if len(adoption_sequence)>300:
			# break
print len(adoption_sequence)

#location information files
#can use location combined by country in known_locations_country_us and known_locations1_country_us files
location_buckets = dict() #map to -1 for users not in location files #[-1] * 7697889
fr = open('/twitterSimulations/known_locations.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	location_buckets[int(u[0])] = int(u[1])
fr.close()

fr = open('/twitterSimulations/known_locations1.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	location_buckets[int(u[0])] = int(u[1])
fr.close()

def get_location(author):
	if author in location_buckets:
		return location_buckets[author]
	else:
		return -1 #location unknown
		
#initialise adjacency list
def init_adj_list(num_nodes):
	adj = [[]] * num_nodes
	for i in range(0, num_nodes):
		adj[i] = []
	return adj

#get all paths starting from a vertex using DFS on hashtag graph
#Reference: http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
def dfs_paths(adj,start):
	paths = []
	visited = set()
	stack = [(start, [start])]
	while stack:
		(vertex, path) = stack.pop()
		# print vertex, path
		nbh = set(adj[vertex]) - visited # visit each vertex once
		if len(nbh)==0:
			paths.append(path)
		for next in nbh:
			stack.append((next, path + [next])) #instead of all possible paths from all vertices, get maximum length paths in the graph
			visited.add(next)
	return paths
	
#get user ids from vertex ids in paths
def path_to_sentence(nodes,path):
	s=[]
	for i in path:
		_,author = nodes[i]
		s.append(str(author)) #type of str for author is needed for using join
	return s
"""
#separate hashtag segments from adoption sequence of a hashtag using maximum time difference allowed for edges for reducing length of sequence to consider for hashtag graph
def get_adoption_segments(sequence):
	first_tw_time,first_tw_author = sequence[0]
	prev_time = first_tw_time
	seg = [] #group of tweets or segment
	seg.append(sequence[0])
	segments=[] #group of segments
	for i in sequence[1:]:
		time,_ = i
		if time-prev_time>time_diff_for_edge:
			segments.append(seg)
			seg = []
		seg.append(i)
		prev_time = time
	if seg!=[]:
		segments.append(seg)
	return segments
"""		
#get adjacency list of hashtag graph from a segment
def get_hashtag_graph_adj(segment):
	num_nodes = len(segment)
	# adj_list = init_adj_list(num_nodes) #adjacency list for directed graph
	adj_list = [[]] * num_nodes
	for i in range(0, num_nodes):
		adj_list[i] = []
	if num_nodes==1:
		return adj_list
	location = dict()
	for i in range(0,num_nodes):
		_,author = segment[i]
		author_loc = get_location(author)
		if author_loc not in location:
			location[author_loc]=[]
		location[author_loc].append(i) #time sorted order will change across locations, but not within location. order of vertices in adjacency list is still same
	for loc in location:
		same_loc_seq = location[loc]
		for i in range(0,len(same_loc_seq)):
			vertex_index_first = same_loc_seq[i]
			time_first,_ = segment[vertex_index_first]
			for j in range(i+1,len(same_loc_seq)):
				vertex_index_second = same_loc_seq[j]
				time_second,_ = segment[vertex_index_second]
				if time_second-time_first<=time_diff_for_edge: # only time difference considered for an edge, check other conditions
					adj_list[vertex_index_first].append(vertex_index_second)
				else:
					break #tweets are arranged in increasing time, so no edges will be there with vertices past present node
				#follower relation
				#check if more than one connected components in a segment if single path is considered for each segment
	return adj_list

#get all paths of length m from hashtag graph
def get_paths_from_graph(nodes, adj):
	paths = []
	if len(nodes)<min_context_length: #only if less than m length paths are not taken
		return []
	#DFS for paths starting from a vertex
	for start in range(0,len(nodes)):
		if len(nodes)-start-1<min_context_length: #number of vertices left are less than min context length
			break
		print "DFS from", start
		paths_vertices = dfs_paths(adj,start)
		print "DFS done"
		for p in paths_vertices:
			if len(p)>=min_context_length: #only take paths above minimum context length
				paths.append(path_to_sentence(nodes,p))
	return paths

#get sentences from hashtag sequences
tag_count = 0
def get_sentences(adoption_sequence):
	global tag_count
	for t in adoption_sequence:
		seq=adoption_sequence[t]
		
		tag_count+=1 #print number of hashtags processed
		# if tag_count%100==0:
		print "Hashtag count", tag_count, "Hashtag", t, "tweets", len(seq)
		
		"""
		segments = get_adoption_segments(seq)
		for seg in segments:
			hashtag_graph_adj = get_hashtag_graph_adj(seg)
			paths = get_paths_from_graph(seg, hashtag_graph_adj)
			for p in paths: #change if only one path generated from a hashtag graph
				yield p 
		"""
		hashtag_graph_adj = get_hashtag_graph_adj(seq)
		print "Adjacency list formed"
		# with open("test_timing.pickle","wb") as fd:
			# pickle.dump(seq,fd)
			# pickle.dump(hashtag_graph_adj,fd)
		# paths = get_paths_from_graph(seq, hashtag_graph_adj)
		# print "Paths formed"
		# print "Number of paths", len(paths)
		# for p in paths: #change if only one path generated from a hashtag graph
			# yield p 

#check how many users from dif_timeline1s are not mapped to any location
"""
not_found=0
for t in adoption_sequence:
	seq=adoption_sequence[t]
	for time,author in seq:
		if author not in location_buckets:
			not_found+=1
print not_found #13736074
"""

#check if adoption sequence is time sorted
"""
for t in adoption_sequence:
	seq=adoption_sequence[t]
	time_sorted = sorted(seq,key=lambda x: x[0]) # time is of type int
	if seq!=time_sorted:
		print "not time ordered", t #yes
"""
#write adoption sequence to file
"""
adoption_sequence_removed = dict()
with open("hashtagAdoptionSequences_workingset.pickle","wb") as fd:
	for tag in adoption_sequence:
		if len(adoption_sequence[tag])>=min_tweets_sequence:
			adoption_sequence_removed[tag] = adoption_sequence[tag]
			# fd.write(" ".join(adoption_sequence[tag])+"\n") #author is of type str for using join
	pickle.dump(adoption_sequence_removed,fd)
"""
#write adoption sentences to file

with open("hashtagAdoptionSentences.txt","wb") as fd:
	get_sentences(adoption_sequence)
	# for s in sentences:
		# fd.write(" ".join(s)+"\n")
		# print "Path length", len(s)
		# _=len(s)
