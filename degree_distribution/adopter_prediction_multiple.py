#get nearest users to the initial adopters of a hashtag sequence in test sequences using user vectors and compare with actual adopters in the sequence

import cPickle as pickle
import time
from math import sqrt
import random
from heapq import nsmallest

vec_file = "/mnt/filer01/word2vec/node_vectors_1hr_bfsr.txt"
adoption_sequence_filename = "/mnt/filer01/word2vec/degree_distribution/hashtagAdoptionSequences.txt" #"sample_sequences"
num_init_adopters = 20
par_m = 2
print vec_file, num_init_adopters

with open("/mnt/filer01/word2vec/degree_distribution/sequence_file_split_indices.pickle","rb") as fr:
	_ = pickle.load(fr)
	test_seq_id = pickle.load(fr)
test_seq_id = set(test_seq_id)

def read_vector_file(path_vectors_file):
	vocab = []
	vectors = []
	with open(path_vectors_file,"rb") as fr:
		_,dim = next(fr).rstrip().split(' ')
		word_vector_dim = int(dim)
		next(fr)
		for line in fr:
			line = line.rstrip()
			u = line.split(' ')
			if len(u) != word_vector_dim+1:
				print "vector length error"
			word = int(u[0])
			#normalise to length 1
			vec = []
			length = 0.0
			for d in u[1:]:
				num=float(d)
				vec.append(num)
				length+=num**2
			#vec = map(float,u[1:])
			#length = sum(x**2 for x in vec)
			length = sqrt(length)
			vec_norm = [x/length for x in vec]
			vocab.append(word)
			vectors.append(vec_norm)
	return vectors, vocab, word_vector_dim

vec,vocab,dim = read_vector_file(vec_file)
vocab_index=dict()
for i in xrange(0,len(vocab)):
	vocab_index[vocab[i]]=i
num_users = len(vocab)
print "num users in train sequences", num_users
# print "users removed from vocab", len(set(users_train)-set(vocab))
# print "users in test sequences but not in vocab", len(users_test-set(vocab))

def get_Nranked_list(query_set,N):
	# wordN = [0]*N
	# distN = [0.0]*N
	dist_total = []
	set_size = len(query_set)
	try:
		query_set_ind = [ vocab_index[query] for query in query_set ]
	except KeyError:
		print "query word not present"
		return
	for i in xrange(0,len(vec)):
		if i in query_set_ind:
			continue
		pres_word = vocab[i]
		pres_vec = vec[i]
		dist_k = [0.0]*set_size
		k=0
		for voc_ind in query_set_ind:
			user_vec = vec[voc_ind]
			#Euclidean distance (user_vec[x]-pres_vec[x])**2, same as cosine dis-similarity user_vec[x]*pres_vec[x] for norm 1 when subtracted by 1 and multiplied by 2
			dist = sum( (user_vec[x]-pres_vec[x])**2 for x in xrange(0,dim) )
			dist_k[k]= sqrt(dist)
			k+=1
			# dist = 0.0
			# for x in xrange(0,dim):
			# 	dist+=(user_vec[x]-pres_vec[x])**2 
		#distance of a point from a set
		# dist_k_sorted = sorted(dist_k)
		nearest_k = min(dist_k) # dist_k_sorted[0] #  if sorted not needed
		if nearest_k!=0.0:
			dist_set=sum( (nearest_k/dist_k[p])**(par_m) for p in xrange(0,set_size) )
			dist_set = nearest_k * (dist_set)**(1.0/set_size)
		else:
			dist_set=0.0
		dist_total.append((pres_word,dist_set))
		# for j in xrange(0,N):
		# 	if dist>distN[j]:
		# 		for k in xrange(N-1,j,-1):
		# 			distN[k] = distN[k-1]
		# 			wordN[k] = wordN[k-1]
		# 		distN[j] = dist
		# 		wordN[j] = pres_word
		# 		break
	wordN = [w for w,_ in nsmallest(N,dist_total,key=lambda x: x[1])]
	return wordN #zip(wordN,distN)

not_found_vocab=[]
# source_thr = 1395858601 + 12*60*60
non_emergent_tags = pickle.load(open("/mnt/filer01/word2vec/degree_distribution/nonEmergentHashtags.pickle","rb"))
tag_seq = []
count=0
# nb_seq = dict()
# adlen = []
with open(adoption_sequence_filename, "rb") as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		not_found=0
		adopters = set()
		first_timestamp = int(u[1][0:u[1].index(',')])
		# first tweet only after source_thr timestamp
		# if first_timestamp>=source_thr
		# check if <5 tweets in 12 hours for emergent hashtags, not already popular
		# u[0] not in non_emergent_tags and
		if count in test_seq_id:
			seq=[]
			for i in xrange(1, len(u)):
				#timestamp = int(u[i][0:u[i].index(',')])
				author = int(u[i][u[i].index(',')+1 : ])
				if author in vocab_index:
					# removing repeat adopters
					if author not in adopters:
						seq.append(author)
						adopters.add(author)
				else:
					not_found+=1
			if len(seq)>num_init_adopters:
				tag_seq.append(seq)
				not_found_vocab.append(not_found)
				# adlen.append(len(seq))
		# elif count not in test_seq_id:
		# 	adop=[]
		# 	for i in xrange(1, len(u)):
		# 		author = int(u[i][u[i].index(',')+1 : ])
		# 		if author in vocab_index:
		# 			adop.append(author)
		# 	for author in set(adop):			
		# 		try:
		# 			nb_seq[author]+=1
		# 		except KeyError:
		# 			nb_seq[author]=1
		count+=1
#nb, number of training sequences participated in
# nb_seq_part = [(a,nb_seq[a]) for a in nb_seq]
# nb_seq_part_sorted = sorted(nb_seq_part, key=lambda x: x[1], reverse=True)
# nb_seq_order = [a for a,_ in nb_seq_part_sorted]
# pickle.dump(nb_seq_order,open("adopter_pred_files/baseline_user_order_bfsr.pickle","wb"))
# pickle.dump(adlen,open("adlen.pickle","wb"))
nb_seq_order = pickle.load(open("/mnt/filer01/word2vec/degree_distribution/adopter_pred_files/baseline_user_order_bfsr.pickle","rb"))
print len(nb_seq_order)
print len(tag_seq),len(test_seq_id),count
print sum(not_found_vocab)/float(len(not_found_vocab)),max(not_found_vocab),min(not_found_vocab)

seq_count_limit=100
num_seqs=0
mean_ap=0.0
# mean_prec_r=0.0
mean_prec_k=0.0
mean_rec_k=0.0
mean_ap_nbapp=0.0
# mean_prec_r_nbapp=0.0
mean_prec_k_nbapp=0.0
mean_rec_k_nbapp=0.0

#test sequences in random order
seq_random_index=range(0,len(tag_seq))
random.shuffle(seq_random_index)
for i in seq_random_index:
	seq_sample_vocab = tag_seq[i]
	# source_user=seq_sample[0]
	# if source_user not in vocab_index:
	# 	continue
	init_adopters=seq_sample_vocab[0:num_init_adopters]
	seq_sample_vocab = set(seq_sample_vocab[num_init_adopters:])
	M = len(seq_sample_vocab)
	N = 1000 #M #num_users
	if M<1000:
		continue
	not_found=not_found_vocab[i]
	#source_vec=vec[vocab_index[source_user]]

	#precision, recall evaluation
	adopters_vec = get_Nranked_list(init_adopters,N)
	precision_k = 0.0
	num_hits = 0.0
	for k,p in enumerate(adopters_vec):
		if p in seq_sample_vocab:
			num_hits+=1.0
			precision_k += num_hits/(k+1.0)
	average_precision = precision_k/min(M,N)
	# prec_r = num_hits/M
	prec_k = num_hits/N
	rec_k = num_hits/M
	print "Avg precision", average_precision, "num of users not found", not_found, "num of adopters in seq", len(seq_sample_vocab)
	# print "RPrecision", prec_r
	print "Precision", prec_k, "Recall", rec_k
	mean_ap+=average_precision
	# mean_prec_r+=prec_r
	mean_prec_k+=prec_k
	mean_rec_k+=rec_k
	num_seqs+=1
	print "MAP", mean_ap/float(num_seqs), "MPk", mean_prec_k/float(num_seqs), "MRk", mean_rec_k/float(num_seqs)
	#, "MRP", mean_prec_r/float(num_seqs)
	
	#baseline
	nb_seq_order = nb_seq_order[:N]
	precision_k_nbapp = 0.0
	num_hits_nbapp = 0.0
	for k,p in enumerate(nb_seq_order):
		if p in seq_sample_vocab:
			num_hits_nbapp+=1.0
			precision_k_nbapp += num_hits_nbapp/(k+1.0)
	average_precision_nbapp = precision_k_nbapp/min(M,N)
	# prec_r_nbapp = num_hits_nbapp/M
	prec_k_nbapp = num_hits_nbapp/N
	rec_k_nbapp = num_hits_nbapp/M
	print "Nb_App", "Avg precision", average_precision_nbapp
	# print "Nb_App", "RPrecision", prec_r_nbapp
	print "Nb_App", "Precision", prec_k_nbapp, "Recall", rec_k_nbapp
	mean_ap_nbapp+=average_precision_nbapp
	# mean_prec_r_nbapp+=prec_r_nbapp
	mean_prec_k_nbapp+=prec_k_nbapp
	mean_rec_k_nbapp+=rec_k_nbapp
	print "Nb_App", "MAP", mean_ap_nbapp/float(num_seqs), "MPk", mean_prec_k_nbapp/float(num_seqs), "MRk", mean_rec_k_nbapp/float(num_seqs)
	#, "MRP", mean_prec_r_nbapp/float(num_seqs)
	
	seq_count_limit-=1
	if seq_count_limit==0:
		break
print num_seqs
print "MAP", "user vectors", mean_ap/float(num_seqs), "Nb_App", mean_ap_nbapp/float(num_seqs)
# print "MRP", mean_prec_r/float(num_seqs), mean_prec_r_nbapp/float(num_seqs)
print "MPk", mean_prec_k/float(num_seqs), mean_prec_k_nbapp/float(num_seqs), "MRk", mean_rec_k/float(num_seqs), mean_rec_k_nbapp/float(num_seqs)
#pickle.dump(source_time,open("source_time.pickle","wb"))
