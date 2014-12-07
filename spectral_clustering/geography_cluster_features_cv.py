#cluster 94*94 matrix of geographies sharing hashtags for which they're of interest of

import time
import sys
import os
import cPickle as pickle
from sklearn.cluster import SpectralClustering,KMeans
from numpy import array,ones
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import normalize

# loc*loc matrix
"""country_map = dict()
country_map[93]='Unknown'
path_country_file = 'text1_country.txt'
with open(path_country_file, 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		country_map[int(u[0])]=u[1]"""
		
"""sim_mat = []
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

spectral = SpectralClustering(n_clusters=loc_mat_clusters, eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='precomputed', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None)
idx = spectral.fit(X_word).labels_
loc_cluster_num = list(idx)"""
		
# country_clusters = []
# for c in range(0,loc_mat_clusters):
	# country_clusters.append([i for i, x in enumerate(loc_cluster_num) if x == c])
# print country_clusters

# ht*loc matrix
"""sim_mat = []
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

indices = np.random.permutation(X_word.shape[0])
train_size = int(.9*(X_word.shape[0]))
training_idx, test_idx = indices[:train_size], indices[train_size:]
X_word_train, X_word_test = X_word[training_idx,:], X_word[test_idx,:]
ht_array = array(ht_map)
ht_train, ht_test = list(ht_array[training_idx]), list(ht_array[test_idx])"""

with open( "train_test_split.pickle", "rb" ) as fd:
	X_word_train=pickle.load(fd)
	X_word_test=pickle.load(fd)
	ht_train=pickle.load(fd)
	ht_test=pickle.load(fd)
# with open( "cluster_centres.pickle", "rb" ) as fd:
	# cluster_centres=pickle.load(fd)
	
if len(sys.argv)<2:
	mat_clusters = 10
else:
	mat_clusters = int(sys.argv[1])

# spectral = SpectralClustering(n_clusters=mat_clusters, eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='rbf', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', kernel_params=None)

kmeanspp = KMeans(n_clusters=mat_clusters, init='k-means++', n_init=1000, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
# kmeanspp = KMeans(n_clusters=mat_clusters, init=cluster_centres, n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
kmeanspp_model = kmeanspp.fit(X_word_train)
idx = kmeanspp_model.labels_
cluster_num = list(idx)
cluster_size = Counter(cluster_num)

"""with open( "train_test_split.pickle", "wb" ) as fd:
	pickle.dump(X_word_train,fd)
	pickle.dump(X_word_test,fd)
	pickle.dump(ht_train,fd)
	pickle.dump(ht_test,fd)"""
with open( "cluster_centres.pickle", "wb" ) as fd:
	pickle.dump(kmeanspp_model.cluster_centers_,fd)
cluster_num_test=list(kmeanspp_model.predict(X_word_test))
"""cluster_asgn = []
cluster_centers = dict()
for c in range(0,mat_clusters):
	cluster_asgn.append([i for i, x in enumerate(cluster_num) if x == c])
for c in range(0,mat_clusters):
	cluster_centers[c]=[0.0]*94
	count = 0
	for i in cluster_asgn[c]:
		count+=1
		cluster_centers[c]+=X_word_train[i]
	if count!=0:
		cluster_centers[c] = float(cluster_centers[c])/count
print cluster_num_test"""

"""ht_clusters = []
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
	ht_clusters.append([ht_map[i] for i, x in enumerate(cluster_num) if x == c])"""
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
	fd.write("TagName,ClusterNum,ClusterSize,TrainExample\n")
	# fd.write("TagName,ClusterNum,ClusterSize,InfectedCommunities\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		if tag in ht_train:
			tag_idx = ht_train.index(tag)
			fd.write(tag+","+str(cluster_num[tag_idx])+","+str(cluster_size[cluster_num[tag_idx]])+","+"1"+"\n")
		else:
			tag_idx = ht_test.index(tag)
			fd.write(tag+","+str(cluster_num_test[tag_idx])+","+str(cluster_size[cluster_num_test[tag_idx]])+","+"0"+"\n")
		# fd.write(tag+","+str(cluster_num[ht_map.index(tag)])+","+str(cluster_size[cluster_num[ht_map.index(tag)]])+","+str(len(ht_inf_loc[tag]))+"\n")