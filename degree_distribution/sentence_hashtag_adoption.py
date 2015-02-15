#write sequence of authors adopting a hashtag for hashtags with atleast 10 adoptions as sentences for training using word2vec 
import time
import sys
import os
import cPickle as pickle

adoption_sequence = dict()
with open('/twitterSimulations/timeline_data/dif_timeline1s', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		tag = u[0]
		author = u[2]
		if tag not in adoption_sequence:
			adoption_sequence[tag]=[]
		adoption_sequence[tag].append(author)
print len(adoption_sequence)

min_tweets = 10
with open("hashtagAdoptionSentences.txt","wb") as fd:
	for tag in adoption_sequence:
		if len(adoption_sequence[tag])>=min_tweets:
			fd.write(" ".join(adoption_sequence[tag])+"\n") #author is of type str for using join