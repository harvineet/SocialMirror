from heapq import nsmallest
from math import sqrt
vec = [(1,1),(4,2),(2,2),(3,2),(3,3),(4,4),(2,3)]
for i in range(0,7):
    a,b=vec[i]
    l=float(sqrt(a**2+b**2))
    vec[i]=(a/l,b/l)
vocab = [1,2,3,4,5,6,7]
dim = 2
par_m = 2
vocab_index=dict()
for i in xrange(0,len(vocab)):
	vocab_index[vocab[i]]=i
query_set = [4,5]
N=6

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
	print query_set_ind
	for i in xrange(0,len(vec)):
		if i in query_set_ind:
			continue
		pres_word = vocab[i]
		pres_vec = vec[i]
		dist_k = [0.0]*set_size
		k=0
		for voc_ind in query_set_ind:
			user_vec = vec[voc_ind]
			#Euclidean distance, cosine similarity user_vec[x]*pres_vec[x], change to decreasing order of distance in sorted,distN
			print user_vec,pres_vec
			dist = 1- sum((user_vec[x]*pres_vec[x]) for x in xrange(0,dim))
			dist_k[k]=sqrt(float(2*dist))
			k+=1
			# dist = 0.0
			# for x in xrange(0,dim):
			# 	dist+=(user_vec[x]-pres_vec[x])**2 
		#distance of a point from a set
		# dist_k_sorted = sorted(dist_k)
		print i,dist_k
		nearest_k = min(dist_k) # dist_k_sorted[0] #  if sorted not needed
		if nearest_k!=0.0:
			dist_set=sum( (nearest_k/dist_k[p])**(par_m) for p in xrange(0,set_size) )
			dist_set = nearest_k * (dist_set)**(1.0/set_size)
		else:
			dist_set=0.0
		print i,dist_set
		dist_total.append((pres_word,dist_set))
		# for j in xrange(0,N):
		# 	if dist>distN[j]:
		# 		for k in xrange(N-1,j,-1):
		# 			distN[k] = distN[k-1]
		# 			wordN[k] = wordN[k-1]
		# 		distN[j] = dist
		# 		wordN[j] = pres_word
		# 		break
	print dist_total
	wordN = [w for w,_ in nsmallest(N,dist_total,key=lambda x: x[1])]
	return wordN #zip(wordN,distN)

print get_Nranked_list(query_set,N)
