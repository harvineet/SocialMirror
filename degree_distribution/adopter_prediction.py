#write features for hashtags in virality prediction using user vectors

import cPickle as pickle
import time
from distance_w2v import *
import random

vec_file = "/mnt/filer01/word2vec/node_vectors_1hr.txt"
adoption_sequence_filename = "/mnt/filer01/word2vec/degree_distribution/hashtagAdoptionSequences.txt" #"sample_sequences"

vec,vocab,dim = read_vector_file(vec_file)
vocab_set = set(vocab)
# vocab_index=dict()
# for i in range(0,len(vocab)):
# 	vocab_index[vocab[i]]=i


not_found_vocab=[]
source_thr = 1395901801 + 7*24*60*60
tag_seq = []
with open(adoption_sequence_filename, "rb") as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		not_found=0
		first_timestamp = int(u[1][0:u[1].index(',')])
		if first_timestamp<source_thr:
			continue
		seq=[]
		for i in range(1, len(u)):
			#timestamp = int(u[i][0:u[i].index(',')])
			author = int(u[i][u[i].index(',')+1 : ])
			seq.append(author)
		tag_seq.append(seq)

seq_count=10000
source_pres=0
mean_ap=0
N=100
seq_sample_index=range(0,len(tag_seq))
random.shuffle(seq_sample_index)
for i in seq_sample_index:
	seq_sample = tag_seq[i]
	source_user=seq_sample[0]
	if source_user not in vocab_set:
		continue
	seq_sample_vocab = [x for x in seq_sample[1:] if x in vocab_set]
	if len(seq_sample_vocab)==0:
		continue
	seq_sample_vocab = set(seq_sample_vocab)
	M = len(seq_sample_vocab)
	not_found=len(seq_sample)-1-M
	#source_vec=vec[vocab_index[source_user]]
	adopters_vec = get_Nnearest(source_user,vec,vocab,N)
	precision_k = 0.0
	num_hits = 0.0
	for k,p in enumerate(adopters_vec[:N]):
		if p in seq_sample_vocab:
			num_hits+=1.0
			precision_k += num_hits/(k+1.0)
	average_precision = precision_k/min(M,N)
	print average_precision, not_found, len(seq_sample)
	mean_ap+=average_precision
	source_pres+=1
	seq_count-=1
	# if seq_count==0:
	# 	break
print source_pres
print mean_ap/float(source_pres)
#print sum(not_found_vocab)/float(len(not_found_vocab)),max(not_found_vocab),min(not_found_vocab)
#pickle.dump(source_time,open("source_time.pickle","wb"))
