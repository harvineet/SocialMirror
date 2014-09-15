#Python file to create the spread of topics according to parameters alpha and beta and using time decay diffusion of influence model
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
import math
import random
from os import listdir
from os.path import isfile, join
#from decimal import *
#getcontext().prec = 28

buckets = [-1] * 7697889

numOfSets = 0
pset = []
setSize = []
id_not_found = 0
def initSet(n):
	global pset
	pset = [0]*n
	global setSize
	setSize = [1]*n
	global numOfSets
	numOfSets = n
	for i in range(0, n):
		pset[i] = i

def findSet(a):
	global pset
	if pset[a] == a:
		return a
	else:		
		pset[a] = findSet(pset[a])
		return pset[a]

def isSameSet(a, b):
	if findSet(a) == findSet(b):
		return True
	else:
		return False

def MergeSet(a, b):
	if not isSameSet(a,b):
		global numOfSets
		numOfSets = numOfSets - 1
		global setSize
		setSize[findSet(b)] = setSize[findSet(b)] + setSize[findSet(a)]
		setSize[findSet(a)] = 0
		global pset		
		pset[findSet(a)] = findSet(b)

arr = ["user_followers_bigger_graph.txt","user_followers_bigger_graph_2.txt", "user_followers_bigger_graph_i.txt","user_followers_bigger_graph_recrawl_2.txt", "user_followers_bigger_graph_recrawl_3.txt","user_followers_bigger_graph_recrawl.txt"]

arr_friend = ["user_friends_bigger_graph.txt","user_friends_bigger_graph_2.txt", "user_friends_bigger_graph_i.txt","user_friends_bigger_graph_recrawl.txt"]
#arr = ["user_followers_bigger_graph_i.txt"]

node_selected = random.sample(range(0, 7697889),300000)
node_selected = set(node_selected)
with open('sample/sample_nodes.txt','wb') as fd:
	for i in node_selected:
		fd.write(str(i)+"\n")

m = dict()
fr = open("graph/map.txt")
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	m[int(u[0])] = int(u[1])
fr.close()

print 'Map Read\n'

fd = open('sample/sample_followers.txt','wb')
for i in arr:
	fr = open("graph/" + i,'r')
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		sel = []
		if(int(u[0]) > 7697889):
			continue
		if m[int(u[1])] in node_selected:
			fd.write(line+"\n")
		# if m[int(u[1])] in node_selected:
			# for j in range(2,len(u)):
				# if m[int(u[j])] in node_selected:
					# sel.append(m[int(u[j])])
			# fd.write(u[0]+" "+u[1]+" "+" ".join(sel)+"\n")
	fr.close()
	print i
fd.close()
fd = open('sample/sample_friends.txt','wb')
for i in arr_friend:
	fr = open("graph/" + i,'r')
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		try:
			if m[int(u[1])] in node_selected:
				fd.write(line+"\n")
		except:
			id_not_found+=1
	fr.close()
	print i
fd.close()
fd = open('timeline_data/sample_timeline_weng','wb')
fr = open('timeline_data/timeline_weng','r')
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	sel = []
	for i in range(1, len(u)):
		timestamp = int(u[i][0:u[i].index(',')])
		author = int(u[i][u[i].index(',')+1 : ])
		author = m[author]
		if author in node_selected:
			sel.append(u[i])
	fd.write(u[0]+" "+" ".join(sel)+"\n")
fr.close()
fd.close()
print id_not_found