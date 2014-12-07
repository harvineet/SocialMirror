#cluster 94*94 matrix of geographies sharing hashtags for which they're of interest of

import time
import sys
import os
import cPickle as pickle
from sklearn.cluster import SpectralClustering
from numpy import array,ones
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import normalize

"""country_map = dict()
country_map[93]='Unknown'
path_country_file = 'text1_country.txt'
with open(path_country_file, 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		country_map[int(u[0])]=u[1]"""
		
sim_mat = []
path_mat_file = 'matrix_loc.txt'
with open(path_mat_file, 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) != 94:
			print "vector length error"
		vec = map(float,u)
		# word_vectors[word] = vec
		sim_mat.append(vec)

X_word = array(sim_mat)

# norm2 = normalize(X_word, norm='l2')
# X_word = norm2

loc_mat_clusters = 10

spectral = SpectralClustering(n_clusters=loc_mat_clusters, eigen_solver=None, random_state=None, n_init=1000, gamma=1.0, affinity='precomputed', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None)
idx = spectral.fit(X_word).labels_
loc_cluster_num = list(idx)
		
# country_clusters = []
# for c in range(0,loc_mat_clusters):
	# country_clusters.append([i for i, x in enumerate(loc_cluster_num) if x == c])
# print country_clusters

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
			if vec[d]>0.0067:
				ht_inf_loc[u[0]].add(d)
		# word_vectors[word] = vec
		sim_mat.append(vec)
		
X_word = array(sim_mat)

if len(sys.argv)<2:
	mat_clusters = 10
else:
	mat_clusters = int(sys.argv[1])
spectral = SpectralClustering(n_clusters=mat_clusters, eigen_solver=None, random_state=None, n_init=1000, gamma=1.0, affinity='rbf', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', kernel_params=None)
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
num_cluster_ht_spread = dict() #num of location by location matrix clusters to which hashtag spread
for i in range(0,len(ht_map)):
	cluster=cluster_num[i]
	tag=ht_map[i]
	if cluster not in num_loc_clusters:
		num_loc_clusters[cluster]=set()
	num_loc_clusters[cluster].update(ht_inf_loc[tag])
	#unique location clusters a hashtag spread to
	uniq_clus = set()
	for loc in ht_inf_loc[tag]:
		uniq_clus.add(loc_cluster_num[loc])
	num_cluster_ht_spread[tag]=uniq_clus
	
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
	fd.write("TagName,ClusterNum,ClusterSize,NumClusterLocations,InfectedInterestCommunities,InfectedClusterCommunities\n")
	# fd.write("TagName,ClusterNum,ClusterSize,InfectedCommunities\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		fd.write(tag+","+str(cluster_num[ht_map.index(tag)])+","+str(cluster_size[cluster_num[ht_map.index(tag)]])+","+str(len(num_loc_clusters[cluster_num[ht_map.index(tag)]]))+","+str(len(ht_inf_loc[tag]))+","+str(len(num_cluster_ht_spread[tag]))+"\n")
		# fd.write(tag+","+str(cluster_num[ht_map.index(tag)])+","+str(cluster_size[cluster_num[ht_map.index(tag)]])+","+str(len(ht_inf_loc[tag]))+"\n")