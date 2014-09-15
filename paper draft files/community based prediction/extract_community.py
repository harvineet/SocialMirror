#file to extract communitites for Weng et al dataset, follower_gcc.anony.dat file, using Infomap with options -z -2 -i link-list ../virality2013/follower_gcc.anony.dat ../output1
from collections import defaultdict

def get_community_map(fname):
    #fname = "output1/follower_gcc.anony.tree"

	community_node_map = defaultdict(lambda: [])
	node_community_map = defaultdict(lambda: [])
	deleted_nodes = []
	covered_nodes_num = 0
	with open(fname) as f:
		next(f)
		for line in f:
			line = line.rstrip()
			[c_num_two,_,node_name] = line.split(' ')
			[cluster_num,_] = c_num_two.split(':')
			node_name = node_name.replace('"','')
			community_node_map[cluster_num].append(node_name)
				
	for i in community_node_map.keys():
		if len(community_node_map[i]) < 3:
			deleted_nodes = deleted_nodes + community_node_map[i]
			del community_node_map[i]
		else:
			covered_nodes_num += len(community_node_map[i])

	for cluster_num in community_node_map:
		for node_name in community_node_map[cluster_num]:
			node_community_map[node_name] = cluster_num
	print covered_nodes_num, len(deleted_nodes), len(community_node_map)
	return node_community_map, deleted_nodes

def get_adj_list(ffname):
	# ffname = "virality2013/follower_gcc.anony.dat"
	fn = "adjacency_list.dat"
	adj_list = defaultdict(lambda: [])
	with open(ffname) as f:
		for line in f:
			line = line.rstrip()
			[node1,node2] = line.split(' ')
			adj_list[node1].append(node2)
			adj_list[node2].append(node1)

		# giant connected component of adj list

	# with open(fn) as f1:
	# 	for i in adj_list:
	# 		f1.write(i+' '+)

	return adj_list