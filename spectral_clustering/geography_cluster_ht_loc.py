#cluster 94*94 matrix of geographies sharing hashtags for which they're of interest of

import time
import sys
import os
import cPickle as pickle
from sklearn.cluster import SpectralClustering,KMeans#,AgglomerativeClustering
# from numpy import array,ones
import numpy as np
# from scipy.cluster.vq import kmeans,vq
import matplotlib.pyplot as plt
from collections import Counter
import math
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

		# word_vectors[word] = vec
		sim_mat.append(vec)
		
X_word = np.array(sim_mat)

with open( "cluster_centres.pickle", "rb" ) as fd:
	cluster_centres=pickle.load(fd)

# norm2 = normalize(X_word, norm='l2')
# X_word = norm2

if len(sys.argv)<2:
	mat_clusters = 10
else:
	mat_clusters = int(sys.argv[1])
	
# spectral = SpectralClustering(n_clusters=mat_clusters, eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='rbf', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None)
# idx = spectral.fit(X_word).labels_

# kmeanspp = KMeans(n_clusters=mat_clusters, init='k-means++', n_init=100, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
kmeanspp = KMeans(n_clusters=mat_clusters, init=cluster_centres, n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
idx = kmeanspp.fit(X_word).labels_

# centroids,distortion = kmeans(X_word,mat_clusters, iter=10, thresh=1e-05)
# print distortion
# idx,_ = vq(X_word,centroids)

# aggclust = AgglomerativeClustering(n_clusters=mat_clusters, affinity='euclidean', connectivity=None, n_components=None, linkage='ward')
# idx = aggclust.fit(X_word).labels_

cluster_num = list(idx)
cluster_size = Counter(cluster_num)
# plt.matshow(X_word)
# plt.show()

# print len(cluster_num),len(ht_map)
# for tag in ['craftconf','tvof']:
	# print X_word[ht_map.index(tag)]

ht_clusters = []
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
	fd.write("TagName,ClusterNum,ClusterSize\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		# fd.write(tag+","+str(cluster_num[ht_map.index(tag)])+","+str(int(math.log10(cluster_size[cluster_num[ht_map.index(tag)]])))+"\n")
		fd.write(tag+","+str(cluster_num[ht_map.index(tag)])+","+str(cluster_size[cluster_num[ht_map.index(tag)]])+"\n")