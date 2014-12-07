#keep most frequent words for each hashtag in the dataset in pre-trained vector file
import time
import sys
import os

path_txtfile = 'twitter_vectors.txt'

filter_words = dict()
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