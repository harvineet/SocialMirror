from math import log
ht_spread = []
ht_map=[]
# path_mat_file = 'tag_clusters/tag_histograms_500.csv'
path_mat_file = 'tag_histograms_1000_new.csv'
with open(path_mat_file, 'rb') as fr:
	next(fr)
	for line in fr:
		line = line.rstrip()
		u = line.split(',')
		if len(u) != 1001:
			print "vector length error"
		ht_map.append(u[0])
		vec = map(float,u[1:])
		if sum(vec) < 0.999 or sum(vec) > 1.0001:
			print "vector value error",sum(vec)
		spread=0
		for d in range(0,len(vec)):
			if vec[d]>0.0:
				# spread+= -1*vec[d]*log(vec[d],2)
				spread+= 1
		ht_spread.append(spread)
path_output_file = 'tag_spread.csv'
with open('../timeline_weng', 'rb') as fr, open(path_output_file,'wb') as fd:
	fd.write("TagName,Spread\n")
	for ht in range(0,len(ht_spread)):
		fd.write(ht_map[ht]+","+str(ht_spread[ht])+"\n")
