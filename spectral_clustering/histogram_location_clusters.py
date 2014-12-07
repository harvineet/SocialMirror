#create file for histograms of number of locations in clusters and fraction of viral topics in each cluster

from collections import defaultdict
with open('feature_clusters_loc_rbf_10_second.csv','rb') as fr, open('hist_location_clusters.csv','wb') as fd:
	num_loc_clusters = dict()
	num_viral_cluster = defaultdict(int)
	num_nviral_cluster = defaultdict(int)
	total_viral = 0
	total_nviral = 0
	next(fr)
	for line in fr:
		line=line.rstrip().split(',')
		num_loc_clusters[line[27]]=line[29]
		if int(line[31])==1:
			total_viral+=1
			if line[27] not in num_viral_cluster:
				num_viral_cluster[line[27]]=0
			num_viral_cluster[line[27]]+=1
		else:
			total_nviral+=1
			if line[27] not in num_nviral_cluster:
				num_nviral_cluster[line[27]]=0
			num_nviral_cluster[line[27]]+=1
	print num_viral_cluster.keys()
	print num_nviral_cluster.keys()
	print num_loc_clusters.keys()
	for clus in num_viral_cluster:
		num_viral_cluster[clus] = float(num_viral_cluster[clus])/total_viral
	for clus in num_nviral_cluster:
		num_nviral_cluster[clus] = float(num_nviral_cluster[clus])/total_nviral
	fd.write('ClusterNumb,NumLocations,FractionViral,FractionNonViral\n')
	for c in num_loc_clusters:
		fd.write(c+","+num_loc_clusters[c]+","+str(num_viral_cluster[c])+","+str(num_nviral_cluster[c])+"\n")
		