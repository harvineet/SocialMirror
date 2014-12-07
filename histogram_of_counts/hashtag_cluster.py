#cluster words from pre-trained vector txt file and form histogram vectors for hashtags in the dataset
#number of tweets from tweet extracts before 1500 threshold not same as in timeline_weng, 6 hashtags also missing
# yfsfant1
# beforedadeal
# bb07
# maverickradio
# mbeurope
# goodchocolate

#usage python hashtag_clyster.py <word_clusters> <tag_clusters>
import time
import sys
import os
import cPickle as pickle
# from sklearn.cluster import KMeans
from numpy import array
from scipy.cluster.vq import kmeans,vq
# import numpy as np
from collections import Counter

word_vectors = []
path_vec_file = '/mnt/filer01/word2vec/twitter_vectors.txt'
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
tag_bow_org = []
with open('tag_tweets_bow.txt', 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		tag = u[0]
		tag_bow_org.append(tag)
tag_bow = []
tag_bow_processed = []
with open('tag_tweets_bow_processed.txt', 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		tag = u[0]
		words = u[1:]
		tag_bow.append(words) # remove duplicate words also
		tag_bow_processed.append(tag)
print "word vectors and tag words read"
word_clusters = int(sys.argv[1])#1000
# kmeans = KMeans(init='k-means++', n_clusters=word_clusters, n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
# idx = list(kmeans.fit(X_word).labels_)
centroids,distortion = kmeans(X_word,word_clusters, iter=5, thresh=1e-05)
print distortion
idx,_ = vq(X_word,centroids)

word_to_cluster = dict()
for i in range(0,len(idx)):
	word_to_cluster[labels[i]] = idx[i]
	
print len(word_to_cluster)
print len(word_vectors)
print len(tag_bow)

word_not_found=set()
hist_feature = []
for tag_words in tag_bow:
	tag_feature = [0]*word_clusters
	num_words = 0
	for word in tag_words:
		try: #words from tag bow missing in word vector, may be because of min limit on word occurrence 5
			# cluster_id = idx[labels.index(word)] # cluster index from 0, and order of idx and labels same
			cluster_id = word_to_cluster[word] # cluster index from 0, and order of idx and labels same
			tag_feature[cluster_id]+=1
			num_words+=1
		except:
			word_not_found.add(word)
	#normalise by total number of words
	# num_words = len(tag_words)
	if num_words==0:
		print "error, tag with no words"
		num_words = 0.1
	hist_feature.append([float(x)/num_words for x in tag_feature])
print len(word_not_found)
with open('error_hashtag_cluster.txt', 'wb') as fd:
	for i in word_not_found:
		fd.write(i+"\n")
tag_labels = tag_bow_org #order might be different, check
X_tag = array(hist_feature)
tag_clusters = int(sys.argv[2])#25
centroids_tag,distortion_tag = kmeans(X_tag,tag_clusters, iter=10, thresh=1e-05)
print distortion_tag
idx_tag,_ = vq(X_tag,centroids_tag)
cluster_size = Counter(idx_tag)

"""print len(tag_bow_processed)==len(tag_bow_org)
with open('tag_names_order_check.csv', 'wb') as fd:
	for i in range(0,len(tag_bow_org)):
		fd.write(tag_bow_org[i]+","+tag_bow_processed[i]+"\n")"""
with open('kmeans_output_'+str(word_clusters)+'_'+str(tag_clusters)+'.pickle', 'wb') as fd:
	pickle.dump(centroids,fd)
	pickle.dump(idx,fd)
	pickle.dump(tag_labels,fd)
	pickle.dump(hist_feature,fd)
	pickle.dump(centroids_tag,fd)
	pickle.dump(idx_tag,fd)
		
path_cluster_file = 'tag_clusters_'+str(word_clusters)+'_'+str(tag_clusters)+'.csv'
path_histogram_file = 'tag_histograms_'+str(word_clusters)+'.csv'

pred_thr = 1500
with open('/twitterSimulations/timeline_data/timeline_weng', 'rb') as fr, open(path_cluster_file,'wb') as fd, open(path_histogram_file,'wb') as fd_hist:
	fd.write("TagName,ClusterNum,ClusterSize\n")
	fd_hist.write("TagName,"+",".join(["HistVector"+str(num) for num in range(0,word_clusters)])+"\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		if tag in ["yfsfant1","beforedadeal","bb07","maverickradio","mbeurope","goodchocolate"]:
			fd.write(tag+","+str(0)+","+str(cluster_size[0])+"\n")
			fd_hist.write(tag+","+",".join(map(str,[0.]*word_clusters))+"\n")
		else:
			fd.write(tag+","+str(idx_tag[tag_labels.index(tag)])+","+str(cluster_size[idx_tag[tag_labels.index(tag)]])+"\n")
			fd_hist.write(tag+","+",".join(map(str,hist_feature[tag_labels.index(tag)]))+"\n")
