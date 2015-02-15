#cluster words from vocab word classes txt file and form histogram vectors for hashtags in the dataset using idf weights for words
#number of tweets from tweet extracts before 1500 threshold not same as in timeline_weng, 6 hashtags also missing
# yfsfant1
# beforedadeal
# bb07
# maverickradio
# mbeurope
# goodchocolate

#usage python hashtag_clyster.py <tag_clusters>
import time
import sys
import os
import cPickle as pickle
# from sklearn.cluster import KMeans
from numpy import array
from scipy.cluster.vq import kmeans,vq
# import numpy as np
from collections import Counter
import math

word_clusters_dim = 1000 #sys.argv[1] is 1000 according to word classes file used
path_class_file = '/mnt/filer01/word2vec/twitter_vectors_classes.sorted.txt'
word_to_cluster = dict()
with open(path_class_file, 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		word_to_cluster[u[0]]=int(u[1])

tag_labels = []
num_tags = 0
with open('/mnt/filer01/tweets_repository/Nov2013/tag_tweets_bow.txt', 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		tag = u[0]
		tag_labels.append(tag)
		num_tags+=1

word_doc_freq = dict()
tag_bow = []
with open('/mnt/filer01/tweets_repository/Nov2013/tag_tweets_bow_processed.txt', 'rb') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		tag = u[0]
		words = u[1:]
		tag_bow.append(words) # remove duplicate words also
		doc_words = set()
		for w in words:
			if w not in doc_words:
				if w not in word_doc_freq:
					word_doc_freq[w]=0
				word_doc_freq[w]+=1
				doc_words.add(w)
		
word_not_found=set()
hist_feature = []
for tag_words in tag_bow:
	tag_feature = [0]*word_clusters_dim
	num_words = 0
	# word_term_freq = Counter(tag_words)
	for word in tag_words:
		try: #words from tag bow missing in word vector, may be because of min limit on word occurrence 5
			cluster_id = word_to_cluster[word] # cluster index from 0, and order of idx and labels same
			df = word_doc_freq[word] #document frequency of words from vocab file
			idf = math.log10(float(num_tags)/df)
			tag_feature[cluster_id]+=1*idf #using idf as word relevance
			num_words+=1*idf
		except:
			word_not_found.add(word)
	#normalise by total number of words
	# num_words = len(tag_words)
	if num_words==0:
		print "error, tag with no words"
		num_words = 0.1
	hist_feature.append([float(x)/num_words for x in tag_feature])
# with open('hashtag_vec_tfidf.pickle', 'wb') as fd:
	# pickle.dump(hist_feature,fd)
print len(word_doc_freq), len(word_not_found)

"""with open('error_hashtag_cluster.txt', 'wb') as fd:
	for i in word_not_found:
		fd.write(i+"\n")"""
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
with open('kmeans_output_tfidf'+'_'+str(tag_clusters)+'.pickle', 'wb') as fd:
	pickle.dump(tag_labels,fd)
	pickle.dump(hist_feature,fd)
	pickle.dump(centroids_tag,fd)
	pickle.dump(idx_tag,fd)
		
path_cluster_file = 'tag_clusters_tfidf_1000_'+str(tag_clusters)+'.csv'
path_histogram_file = 'tag_histograms_tfidf_1000.csv'

pred_thr = 1500
with open('/twitterSimulations/timeline_data/timeline_weng', 'rb') as fr, open(path_cluster_file,'wb') as fd, open(path_histogram_file,'wb') as fd_hist:
	fd.write("TagName,ClusterNum,ClusterSize\n")
	fd_hist.write("TagName,"+",".join(["HistVector"+str(num) for num in range(0,word_clusters_dim)])+"\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		if tag in ["yfsfant1","beforedadeal","bb07","maverickradio","mbeurope","goodchocolate"]:
			fd.write(tag+","+str(0)+","+str(cluster_size[0])+"\n")
			fd_hist.write(tag+","+",".join(map(str,[0.]*word_clusters_dim))+"\n")
		else:
			fd.write(tag+","+str(idx_tag[tag_labels.index(tag)])+","+str(cluster_size[idx_tag[tag_labels.index(tag)]])+"\n")
			fd_hist.write(tag+","+",".join(map(str,hist_feature[tag_labels.index(tag)]))+"\n")
