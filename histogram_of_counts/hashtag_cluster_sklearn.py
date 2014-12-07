#cluster words from pre-trained vector txt file and form histogram vectors for hashtags in the dataset
#number of tweets from tweet extracts before 1500 threshold not same as in timeline_weng, 6 hashtags also missing
# yfsfant1
# beforedadeal
# bb07
# maverickradio
# mbeurope
# goodchocolate

import time
import sys
import os
from sklearn.cluster import KMeans
from numpy import array
# from scipy.cluster.vq import kmeans,vq
# import numpy as np

# word_vectors = dict()
word_vectors = []
path_vec_file = 'twitter_vectors.txt'
# path_vec_file = '/mnt/filer01/word2vec/twitter_vectors.txt'
with open(path_vec_file, 'rb') as fr:
	next(fr)
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) != 201:
			print "vector length error"
		word = u[0]
		vec = map(float,u[1:])
		# word_vectors[word] = vec
		word_vectors.append([word]+vec)
labels = [x[0] for x in word_vectors]
X_word = array([x[1:] for x in word_vectors])
tag_bow = dict()
with open('tag_tweets_bow_processed.txt', 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		tag = u[0]
		words = u[1:]
		tag_bow[tag] = words

print "word vectors and tag words read"
word_clusters = 100
kmeans = KMeans(init='k-means++', n_clusters=word_clusters, n_init=1, max_iter=15, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=-2)
idx = list(kmeans.fit(X_word).labels_)
# centroids,distortion = kmeans(X_word,word_clusters)
# print distortion
# idx,_ = vq(X_word,centroids)

print len(word_vectors)
print len(tag_bow)

hist_feature = []
for tag in tag_bow:
	tag_feature = [0]*word_clusters
	for word in tag_bow[tag]:
		cluster_id = idx[labels.index(word)] # cluster index from 0
		tag_feature[cluster_id]+=1
	#normalise by total number of words
	num_words = len(tag_bow[tag])
	hist_feature.append([tag]+[float(x)/num_words for x in tag_feature])
tag_labels = [x[0] for x in hist_feature]
X_tag = array([x[1:] for x in hist_feature])
tag_clusters = 9
kmeans_tag = KMeans(init='k-means++', n_clusters=tag_clusters, n_init=1, max_iter=15, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=-2)
idx_tag = list(kmeans.fit(X_tag).labels_)
# centroids_tag,distortion_tag = kmeans(X_tag,word_clusters)
# print distortion_tag
# idx_tag,_ = vq(X_tag,centroids_tag)
		
path_cluster_file = 'tag_clusters.txt'
pred_thr = 1500
with open('../../timeline_weng', 'rb') as fr, open(path_cluster_file,'wb') as fd:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		fd.write(tag+","+str(idx_tag[tag_labels.index(tag)])+"\n")
