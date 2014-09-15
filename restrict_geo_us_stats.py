#restrict hashtags according to adopters in US

user_loc=dict()
not_found=set()
fr = open('known_locations_country.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	user_loc[int(u[0])]=int(u[1])
fr.close()

fr = open('known_locations1_country.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	user_loc[int(u[0])]=int(u[1])
fr.close()

tag_stats = dict() #(us_prop,num_tweets)
with open('timeline_weng', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		us_loc=0.0
		us_loc_set=set()
		loc_set=set()
		count=0
		for i in range(1, len(u)):
			author = int(u[i][u[i].index(',')+1 : ])
			try:
				loc=user_loc[author]
				loc_set.add(author)
				count+=1
				if (loc==39):
					us_loc_set.add(author)
					us_loc+=1
			except:
				not_found.add(author)
		# if count!=0:
		if len(loc_set)!=0:
			# tag_stats[u[0]]=(us_loc/count,len(u)-1)
			tag_stats[u[0]]=(float(len(us_loc_set))/len(loc_set),len(u)-1)
		else:
			print line
with open('geo_us_stats1.csv', 'wb') as fd:
	for i in tag_stats:
		(p,n) = tag_stats[i]
		fd.write(i+","+str(p)+","+str(n)+"\n")
print len(tag_stats), len(not_found)