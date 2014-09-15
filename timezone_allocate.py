#python code to evaluate the location data of users
import json
from os import listdir
from os.path import isfile, join

buckets = [-1] * 7697889

confusion = []
for i in range(0, 141):
	confusion.append([])
	for j in range(0, 141):
		confusion[i].append(0)

allot = set()
fr = open("unknown2.txt",'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	allot.add(u[0])
fr.close()

m = dict()
fr = open("graph/map.txt")
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	m[int(u[0])] = int(u[1])
fr.close()

print 'Map Read\n'

fr = open('known_locations.txt', 'r')
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	#print m[int(u[0])]
	try:
		buckets[m[int(u[0])]] = int(u[1])
	except:
		a = 1
fr.close()

print 'Location Read\n'

fd = open('known_locations1.txt', 'w')
count1 = 0
arr = ["user_followers_bigger_graph.txt","user_followers_bigger_graph_2.txt", "user_followers_bigger_graph_i.txt","user_followers_bigger_graph_recrawl_2.txt", "user_followers_bigger_graph_recrawl_3.txt","user_followers_bigger_graph_recrawl.txt"]
#arr = ["user_followers_bigger_graph_i.txt"]
for i in arr:
	fr = open("graph/" + i,'r')
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if(int(u[0]) > 7697889) or (u[1] not in allot):
			continue
		if len(u) > 2:
			count = [0]*141
			for j in range(2,len(u)):
				temp1 = 0
				try:
					temp1 = m[int(u[j])]
				except:
					continue
				if(buckets[temp1] != -1):
					count[buckets[temp1]] = count[buckets[temp1]] + 1
			if(max(count) > 0):
				fd.write(u[1] + '\t' + str(count.index(max(count))) + '\n')
		else:
			count1 = count1 + 1
	fr.close()
	print i

print count1
fd.close()
