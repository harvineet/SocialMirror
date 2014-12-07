#This script labels topics belonging to each region in details (it uses thresholds to label a topic to one or more countries and number of users is considered)
fk1=open('../../known_locations_country.txt','r')
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

ft=open('text1_country.txt','r')
#Dictionary locdic stores the ID,location name pair
locdic=dict()
for line in ft:
	l=line.rstrip().split('\t')
	ID=int(l[0])
	loc=l[1]
	locdic[ID]=loc
print "Location ID dictionary created\n"


fin=open('../timeline_weng','r')
#ht_dict is a dictionary of location lists - each of its entry is a list of size 94
ht_dict=dict()
ht_total_tweets=dict()
# author_set=dict()
# for i in range(0,94):
	# author_set[i]=set()
for line in fin:
	l=line.rstrip().split(' ')
	ht=l[0]
	if len(l)<=1500:
		continue
	ht_dict[ht]=[0]*94
	ht_total_tweets[ht]=0
	# author_seen=set()
	#if len(l)<=1500:
	#	continue
	# if len(l)>1500:
		#print "Right ht found"
	for i in range(1,1501):
		#print "Am here"
		#if flag==1:
		#	print "Continuing inner loop from exception\n"
		#	flag=0
		#print i
		author=l[i].rstrip().split(',')[1]
		#author_seen.add(author)
		#print "Author="+author	 
		# try:
		if author in author_dict:
			loc=author_dict[author]
		else:
			loc='93' #unknown location: 93
		ht_total_tweets[ht]+=1
		# author_set[int(loc)].add(author)	#an author is added only if he is not present in the set (unique)
		# if author not in author_seen:		#take only a single occurrence of author if he has tweeted multiple times on that ht
			# author_seen.add(author)
		ht_dict[ht][int(loc)]+=1
			#print "Incremented author count for ht="+ht+" at loc "+loc 
		"""except:
		#	flag=1
		#	print "Author "+author+" not present in known_locations*.txt\n"
			continue"""
print "Hashtag dictionary initialized with [0]*94\n"
print "Hashtag dictionary created successfully\n"	
#print ht_dict
fin.close()
#author_set=dict()
#for i in range(0,94):
#	author_set[i]=set()

ht_prob=dict()
fin=open('../timeline_weng','r')
#List of all hashtags that have more than 1500 tweets
ht_list=[]
for ht in ht_dict.keys():
	ht_list.append(ht)
	ht_prob[ht]=[0]*94
'''
for line in fin:
	l=line.rstrip().split(' ')
	ht=l[0]
	ht_list.append(ht)
	ht_prob[ht]=[0]*94
fin.close()
'''


#This list stores the total number of tweets in each country
# num_of_tweets_country=[0]*94

'''
for j in range(0,94):
	s=0
	for i in ht_list:
		try:
			s+=int(ht_dict[i][j])
		except:
			continue
	num_of_tweets_country[j]=s
'''
#Finding all authors (unique) in country j
# for j in range(0,94):
	# num_of_tweets_country[j]=len(author_set[j])
#	if j==19:
#		print "India has: "+str(num_of_tweets_country[j])+" users\n"
print "Total number of tweets for each region calculated\n"

for i in ht_list:
	for j in range(0,94):
		ht_prob[i][j]=float(ht_dict[i][j])/ht_total_tweets[i] #ht_dict[i][j]

# print ht_prob[ht_prob.keys()[0]]
fout3=open('ht_loc_matrix.txt','w')
#for i in range(0,94):
#	fout3.write(str(i)+'\t')
#fout3.write('\n')
for i in ht_list:
	fout3.write(i)
	for j in range(0,94):
		fout3.write('\t'+str(ht_prob[i][j]))
	fout3.write('\n')
fout3.close()
'''
print "Probability dictionary (containing probability of each hashtag in each country) built\n"
fout=open("hashtags_label_multiple.txt",'w')
'''
#print ht_prob["100bookstoread"]
'''
f1=open('timeline_weng_india','r')
ht_list_india=[]

for line in f1:
	l=line.rstrip().split(' ')
	ht=l[0]
	ht_list_india.append(ht)
f1.close()
'''

#Create the country dictionary
'''
country_dict=dict()
f1=open('text1_country.txt','r')
for line in f1:
	l=line.rstrip().split('\t')
	num=l[0]
	country=l[1]
	country_dict[int(num)]=country
'''
'''
for i in ht_list:
	loc_list=[]
	for j in range(0,94):
		if ht_prob[i][j]>0.005:
			loc_list.append(locdic[j])
	if len(loc_list)>0:
		#for m in loc_list:
		fout.write(i+'\t'+''+str(loc_list)[1:len(str(loc_list))-1]+'\n')	

print "Multiple label file created successfully\n"
'''
'''
fin2=open("timeline_weng_india",'r')
fout=open("hashtags_india_label_detail.txt",'w')
for line in fin2:
	l=line.rstrip().split(' ')
	ht=l[0]
	loc=19	#For India
	max_prob=max(ht_prob[ht])
	country=ht_prob[ht].index(max_prob)
	fout.write(ht+'\t'+str(country)+'\n')

fin2.close()
fout.close()
'''	

