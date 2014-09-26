# segment hashtags into words using code by Peter Norvig, removing numbers from tags

from ngrams_tw_corpus import *
# from ngrams import *
import re
import random
def seg2(s): return segment2(s)[1]
def seg2num(s): 
	log_prob = 0.0
	seg_words = []
	for w in s:
		seg_words+=segment2(w)[1]
		log_prob+=segment2(w)[0]
	return ",".join(seg_words),log_prob
def num_sep(tag):
	return re.findall(r'[\d.]+|\D+', tag) #[x for x in re.split(r'((\d*\.?\d*)+)',tag) if x is not '']
tag_split_num = []
with open('../tag_freq.csv', 'r') as fr:
	next(fr)
	for line in fr:
		line = line.rstrip()
		u = line.split(',')
		tag = u[0]
		tag_split_num.append((num_sep(tag),int(u[1]),tag)) # extract numbers from tag
		# tag_split_num.append((tag,int(u[1])))#numeric also
tags_sorted = sorted(tag_split_num,key=lambda x: x[1], reverse=True)
tag_segment_prob = []
with open('../tag_segments_tw.txt', 'w') as fd:	
	for (i,_,tag) in tags_sorted:
		seg_words,log_prob = seg2num(i)
		tag_segment_prob.append((tag,seg_words,log_prob))
		fd.write(tag+"\t"+seg_words+"\n") #str(log_prob)+"\t"+
tags_prob_sorted = sorted(tag_segment_prob,key=lambda x: x[2])
with open('../tag_segments_prob_sorted_tw.txt', 'w') as fd:	
	for (tag,seg,prob) in tags_prob_sorted:
		fd.write(str(prob)+"\t"+tag+"\t"+seg+"\n")
		# fd.write(i+"\t"+",".join(seg2(i))+"\n")
		
rand_smpl = [ tags_prob_sorted[i] for i in sorted(random.sample(xrange(len(tags_prob_sorted)), 100)) ] #test segmentation for random 100 hashtags
with open('../random_sample_tag_segments_tw.txt', 'w') as fd:
	for (tag,seg,prob) in rand_smpl:
		fd.write(str(prob)+"\t"+tag+"\t"+seg+"\n")