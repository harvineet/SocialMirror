#ft=open('text1_country.txt','r')
fk1=open('../known_locations_country.txt','r')
fk2=open('../known_locations1_country.txt','r')
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


fin=open('../timeline_weng','r')
c=0
c2=0
h=[]
h2=[]
for line in fin:
	l=line.rstrip().split(' ')
	ht=l[0]
	h.append(ht)
	if len(l)>1500:
		h2.append(ht)
		c2+=1
		for i in range(1,1501):
			#print "Am here"
			llist=l[i].split(',')
			author=llist[1]
			#print author
			try:
				if author_dict[author]=='39':
					c+=1
			except Exception as e:
			#	print e
				continue

print c
print c2
print len(h),len(set(h))
print len(h2),len(set(h2))
fin.close()
