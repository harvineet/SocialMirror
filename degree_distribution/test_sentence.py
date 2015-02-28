#extract hashtag graphs from sequence of authors adopting a hashtag and find all paths in the graphs to write into corpus file as sentences for training using word2vec 
import time
import sys
import os
import cPickle as pickle

min_tweets_sequence = 0 # minimum number of tweets on a hashtag to remove hashtags with only few tweets available for extracting context

#conditions for edges between tweets
time_diff_for_edge = 10
# time_diff_for_edge = 12*60*60
follower_following_cond = False
geography_cond = False

min_context_length = 0 #minimum length of context or length of paths to consider

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
	stack = [(start, [start])]
	while stack:
		(vertex, path) = stack.pop()
		nbh = set(adj[vertex]) - set(path)
		if len(nbh)==0:
			yield path
		for next in nbh:
			stack.append((next, path + [next])) #instead of paths of fixed length, get maximum length paths in the graph
	
#get user ids from vertex ids in paths
def path_to_sentence(nodes,path):
	for i in path:
		_,author = nodes[i]
		yield str(author) #type of str for author is needed for using join

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
		
#get adjacency list of hashtag graph from a segment
"""
def get_hashtag_graph_adj(segment):
	num_nodes = len(segment)
	adj_list = init_adj_list(num_nodes) #adjacency list for directed graph
	if num_nodes==1:
		return adj_list
	for i in range(0,num_nodes):
		time_first,_ = segment[i]
		for j in range(i+1,num_nodes):
			time_second,_ = segment[j]
			if time_second-time_first<=time_diff_for_edge: # only time difference considered for an edge, check other conditions
				adj_list[i].append(j)
			else:
				break #tweets are arranged in increasing time, so no edges will be there with vertices past present node
			#location
			#follower relation
			#check if more than one connected components in a segment if single path is considered for each segment
	return adj_list
"""
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
	if len(nodes)<min_context_length: #only if fixed length paths are taken and less than m length paths are not taken
		yield []
	#DFS for paths starting from a vertex
	for start in range(0,len(nodes)):
		paths_vertices = dfs_paths(adj,start)
		for p in paths_vertices:
			if len(p)>=min_context_length: #only take paths above minimum context length
				yield list(path_to_sentence(nodes,p))

#get sentences from hashtag sequences
sentences=[]
tag_count = 0

adoption_sequence = dict()
adoption_sequence['test']=[(10,1),(15,2),(21,3),(23,4),(26,5)]
location_buckets = {1:1,2:1,3:2,5:2}
tag_count = 0
def get_sentences(adoption_sequence):
	global tag_count
	for t in adoption_sequence:
		seq=adoption_sequence[t]
		segments = get_adoption_segments(seq)
		for seg in segments:
			hashtag_graph_adj = get_hashtag_graph_adj(seg)
			paths = get_paths_from_graph(seg, hashtag_graph_adj)
			for p in paths: #change if only one path generated from a hashtag graph
				yield p 
		tag_count+=1
		if tag_count%100==0:
			print "Hashtag number", tag_count

print(list(get_sentences(adoption_sequence)))