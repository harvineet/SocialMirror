#cluster 94*94 matrix of geographies sharing hashtags for which they're of interest of

import time
import sys
import os
import cPickle as pickle
from sklearn.cluster import SpectralClustering
from numpy import array,ones
import matplotlib.pyplot as plt
from collections import Counter

"""country_map = dict()
country_map[93]='Unknown'
path_country_file = 'text1_country.txt'
with open(path_country_file, 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		country_map[int(u[0])]=u[1]"""
		
sim_mat = []
path_mat_file = 'ht_loc_matrix.txt'
ht_map=[]
ht_inf_loc=dict()
with open(path_mat_file, 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		if len(u) != 95:
			print "vector length error"
		ht_map.append(u[0])
		vec = map(float,u[1:])
		if sum(vec) < 0.999 or sum(vec) > 1.0001:
			print "vector value error"
		ht_inf_loc[u[0]]=set()
		for d in range(0,len(vec)):
			if vec[d]>0.0065:
				ht_inf_loc[u[0]].add(d)
		# word_vectors[word] = vec
		sim_mat.append(vec)
		
X_word = array(sim_mat)

if len(sys.argv)<2:
	mat_clusters = 10
else:
	mat_clusters = int(sys.argv[1])
spectral = SpectralClustering(n_clusters=mat_clusters, eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='rbf', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', kernel_params=None)
idx = spectral.fit(X_word).labels_
cluster_num = list(idx)
cluster_size = Counter(cluster_num)
# plt.matshow(X_word)
# plt.show()

# print len(cluster_num),len(ht_map)
# for tag in ['craftconf','tvof']:
	# print X_word[ht_map.index(tag)]

ht_clusters = []
num_loc_clusters = dict() #num of locations in cluster to which hashtag belongs to
for i in range(0,len(ht_map)):
	cluster=cluster_num[i]
	tag=ht_map[i]
	if cluster not in num_loc_clusters:
		num_loc_clusters[cluster]=set()
	num_loc_clusters[cluster].update(ht_inf_loc[tag])
	
for c in range(0,mat_clusters):
	ht_clusters.append([ht_map[i] for i, x in enumerate(cluster_num) if x == c])
# with open('cluster_members_loc_'+str(mat_clusters)+'.txt','wb') as fd:
	# for item in ht_clusters:
		# fd.write("%s\n" % ",".join(item))
"""
with open('spectral_output_'+str(mat_clusters)+'.pickle', 'wb') as fd:
	pickle.dump(centroids,fd)
		
"""
path_cluster_file = 'tag_clusters_loc_rbf_'+str(mat_clusters)+'.csv'
pred_thr = 1500
with open('../timeline_weng', 'rb') as fr, open(path_cluster_file,'wb') as fd:
	fd.write("TagName,ClusterNum,ClusterSize,NumClusterLocations,InfectedCommunities\n")
	# fd.write("TagName,ClusterNum,ClusterSize,InfectedCommunities\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		fd.write(tag+","+str(cluster_num[ht_map.index(tag)])+","+str(cluster_size[cluster_num[ht_map.index(tag)]])+","+str(len(num_loc_clusters[cluster_num[ht_map.index(tag)]]))+","+str(len(ht_inf_loc[tag]))+"\n")
		# fd.write(tag+","+str(cluster_num[ht_map.index(tag)])+","+str(cluster_size[cluster_num[ht_map.index(tag)]])+","+str(len(ht_inf_loc[tag]))+"\n")