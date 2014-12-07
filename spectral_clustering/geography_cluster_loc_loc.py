#cluster 94*94 matrix of geographies sharing hashtags for which they're of interest of

import time
import sys
import os
import cPickle as pickle
from sklearn.cluster import SpectralClustering
from numpy import array,ones
import matplotlib.pyplot as plt

country_map = dict()
country_map[93]='Unknown'
path_country_file = 'text1_country.txt'
with open(path_country_file, 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		country_map[int(u[0])]=u[1]
		
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

if len(sys.argv)<2:
	mat_clusters = 10
else:
	mat_clusters = int(sys.argv[1])
spectral = SpectralClustering(n_clusters=mat_clusters, eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='precomputed', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None)
idx = spectral.fit(X_word).labels_
cluster_num = list(idx)

plt.matshow(X_word)
plt.show()

country_clusters = []
for c in range(0,mat_clusters):
	country_clusters.append([country_map[i] for i, x in enumerate(cluster_num) if x == c])
print country_clusters
"""
with open('spectral_output_'+str(mat_clusters)+'.pickle', 'wb') as fd:
	pickle.dump(centroids,fd)
		
path_cluster_file = 'tag_clusters_'+str(word_clusters)+'_'+str(tag_clusters)+'.csv'

pred_thr = 1500
with open('/twitterSimulations/timeline_data/timeline_weng', 'rb') as fr, open(path_cluster_file,'wb') as fd:
	fd.write("TagName,ClusterNum,ClusterSize\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		fd.write(tag+","+str(idx_tag[tag_labels.index(tag)])+","+str(cluster_size[idx_tag[tag_labels.index(tag)]])+"\n")
"""