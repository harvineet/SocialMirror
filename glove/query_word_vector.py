#extract words from GloVe pre-trained vector file and query for hashtags in the dataset
import time
import sys
import os

fd = open("tag_wordvec_glove.txt","w")
path_txtfile = 'glove/twitter_vectors.txt'
# path_txtfile = 'glove.twitter.27B.200d.txt'
pred_thr = 1500
tag_selected = set()
with open('/twitterSimulations/timeline_data/timeline_weng', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		tag_selected.add(tag)
		
found = set()
total = set()
with open(path_txtfile, 'r') as fr:
	for line in fr:
		try:
			line = line.rstrip()
			u = line.split(' ')
			word = u[0].lower()
			# vector = map(float,u[1:])
			total.add(word)
			if word in tag_selected:
				found.add(word)
				fd.write(line+"\n")
		except Exception as e:
			print e
			# print line
fd.close()
# for word in tag_selected:
	# if word in total:
		# found.add(word)
print len(total)
print len(found), len(tag_selected)
print list(found)[0:30]