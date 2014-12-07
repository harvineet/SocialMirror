#This script labels topics belonging to each region in details (it uses thresholds to label a topic to one or more countries and number of users is considered)

m = dict()
fr = open("/twitterSimulations/graph/map.txt",'r')
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	m[int(u[0])] = int(u[1])
fr.close()

print 'Map Read\n'
author_dict = [-1] * 7697889
fr = open('../../known_locations_country.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	#print m[int(u[0])]
	try:
		author_dict[m[int(u[0])]] = int(u[1])
	except:
		a = 1
fr.close()

fr = open('../../known_locations1_country.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	#print m[int(u[0])]
	try:
		author_dict[m[int(u[0])]] = int(u[1])
	except:
		a = 1
fr.close()

print 'Location Read\n'
"""fk1=open('../../known_locations_country.txt','r')
fk2=open('../../known_locations1_country.txt','r')
author_dict=dict()
for line in fk1:
	l=line.rstrip().split('\t')
	author=l[0]
	loc=l[1]
	author_dict[author]=loc
for line in fk2:
	l=line.rstrip().split('\t')
	author=l[0]
	loc=l[1]
	author_dict[author]=loc
print "Authors' location dictionary created"+'\n'
#print author_dict['24117254']
	
fk1.close()
fk2.close()
"""

ft=open('text1_country.txt','r')
#Dictionary locdic stores the ID,location name pair
locdic=dict()
for line in ft:
	l=line.rstrip().split('\t')
	ID=int(l[0])
	loc=l[1]
	locdic[ID]=loc
print "Location ID dictionary created\n"
ft.close()

fin=open('../timeline_weng','r')
#ht_dict is a dictionary of location lists - each of its entry is a list of size 93
ht_dict=dict()
author_set=dict()
for i in range(0,93):
	author_set[i]=set()
for line in fin:
	auth_seen = set()
	numTweets = 0
	l=line.rstrip().split(' ')
	ht=l[0]
	if len(l)<=1500:
		continue
	ht_dict[ht]=[0]*93
	for i in range(1,len(l)):
		numTweets = i
		if(numTweets > 1500):
				break
		#if flag==1:
		#	print "Continuing inner loop from exception\n"
		#	flag=0
		author = int(l[i][l[i].index(',')+1 : ])
		author = m[author]
		# try:
		loc=author_dict[author]
	#	print loc
		author_set[int(loc)].add(author)	#an author is added only if he is not present in the set (unique)
		if author not in auth_seen:
		#	print "Author found for "+ht+" at loc "+loc
			ht_dict[ht][int(loc)]+=1
		auth_seen.add(author)
		"""except:
		#	flag=1
		#	print "Author "+author+" not present in known_locations*.txt\n"
			continue"""
print "Hashtag dictionary initialized with [0]*93\n"
print "Hashtag dictionary created successfully\n"	

fin.close()
#author_set=dict()
#for i in range(0,93):
#	author_set[i]=set()
'''
fin=open('timeline_weng_complete','r')
author_set=dict()
for i in range(0,93):
	author_set[i]=set()
for line in fin:
	l=line.rstrip().split(' ')
	ht=l[0]
#	flag=0
	for i in range(1,len(l)):
		#if flag==1:
		#	print "Continuing inner loop from exception\n"
		#	flag=0
		author=l[i].rstrip().split(',')[1]	 
		try:
			loc=author_dict[author]
			author_set[int(loc)].add(author)	#an author is added only if he is not present in the set (unique)
			ht_dict[ht][int(loc)]+=1
		except:
		#	flag=1
		#	print "Author "+author+" not present in known_locations*.txt\n"
			continue
fin.close()
'''
#print "India=\n"
#print author_set[19]
#print "Hashtag dictionary created successfully\n"
#print ht_dict['000000out']
#ht_prob stores the (num of regional tweets on the ht/total number of tweets in that region) quantity for each hashtag against each location
ht_prob=dict()
#fin=open('timeline_weng_complete','r')
#List of all hashtags
ht_list=ht_dict.keys()

for ht in ht_list:
	ht_prob[ht]=[0]*93
#fin.close()



#This list stores the total number of tweets in each country
num_of_tweets_country=[0]*93

for j in range(0,93):
	num_of_tweets_country[j]=len(author_set[j])
#	if j==19:
#		print "India has: "+str(num_of_tweets_country[j])+" users\n"
print "Total number of tweets for each region calculated\n"

for i in ht_list:
	for j in range(0,93):
		ht_prob[i][j]=float(ht_dict[i][j])/num_of_tweets_country[j]
		
print "Probability dictionary (containing probability of each hashtag in each country) built\n"
fout=open("hashtags_label_multiple.txt",'w')
#print ht_prob["100bookstoread"]
#print ht_list
for i in ht_list:
	loc_list=[]
	for j in range(0,93):
		if ht_prob[i][j]>0.005:
			loc_list.append(locdic[j])
	if len(loc_list)>0:
		#for m in loc_list:
		fout.write(i+'\t'+''+str(loc_list)[1:len(str(loc_list))-1]+'\n')	

print "Multiple label file created successfully\n"
fout.close()
