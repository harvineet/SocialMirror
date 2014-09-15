# form index of follower edges files, takes the latter of the follower lists if duplicate entries are there, such as in recrawled, according to order of files in arr
import cPickle as pickle
# pickle number of friends for each node, map
m = dict()
fr = open("graph/map.txt",'rb')
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	m[int(u[0])] = int(u[1])
fr.close()
pickle.dump( m, open( "map_user_index.pickle", "wb" ) )
print 'Map Read\n'

arr = ["user_followers_bigger_graph.txt","user_followers_bigger_graph_2.txt", "user_followers_bigger_graph_i.txt","user_followers_bigger_graph_recrawl_2.txt", "user_followers_bigger_graph_recrawl_3.txt","user_followers_bigger_graph_recrawl.txt"]

## Read in the file once and build a list of line offsets
# line_offset = []
# offset = 0
# for line in file:
    # line_offset.append(offset)
    # offset += len(line)
# file.seek(0)

## Now, to skip to line n (with the first line being line 0), just do
# file.seek(line_offset[n])
file_index=0
line_offset = dict()
fd=open('follower_file_offset','wb')
count=0
dup=set()
dup_file=set()
map_not_found=0
for i in arr:
	fr = open("graph/" + i,'rb')
	offset = 0
	for line_f in fr:
		line = line_f.rstrip()
		u = line.split(' ')
		if(int(u[0]) > 7697889):
			offset += len(line_f)
			continue
		node = int(u[1])
		if(node in line_offset):
			count+=1
			dup.add(node)
			dup_file.add(file_index)
		if(node in m):
			line_offset[m[node]]=(file_index,offset)
			fd.write(str(m[node])+','+str(file_index)+','+str(offset)+'\n') # check file for duplicate follower lists
		else:
			map_not_found+=1
		offset += len(line_f)
	fr.close()
	file_index+=1
	print i
fd.close()
print count
print len(dup)
print dup_file
print map_not_found
pickle.dump( line_offset, open( "follower_file_offset.pickle", "wb" ) )

arr_friend = ["user_friends_bigger_graph.txt","user_friends_bigger_graph_2.txt", "user_friends_bigger_graph_i.txt","user_friends_bigger_graph_recrawl.txt"]
node_nbh = dict()
friend_id_not_found=0
for i in arr_friend:
	with open("graph/" + i,'rb') as fr:
		for line in fr:
			line = line.rstrip()
			u = line.split(' ')
			if(int(u[0]) > 7697889):
				continue
			try:
				node_nbh[m[int(u[1])]] = int(u[0])
			except:
				friend_id_not_found += 1
	print i
pickle.dump( node_nbh, open( "friends_count_user.pickle", "wb" ) )
print friend_id_not_found