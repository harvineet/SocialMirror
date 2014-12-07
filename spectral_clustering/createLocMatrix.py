#This script takes the hashtags_label_multiple.txt file and creates a 94*94 matrix for clustering purpose
#ft=open('text1_country.txt','r')
import numpy as np
#ht_list stores only those hashtags that cross the prediction threshold
ht_list=[]
f1=open('../timeline_weng','r')
for line in f1:
	l=line.rstrip().split(' ')
	ht=l[0]
	if len(l)>=1501:
		ht_list.append(ht)
f1.close()
ft=open('text1_country.txt','r')
locdic=dict()
locdic['Unknown'] = 93
for line in ft:
	l=line.rstrip().split('\t')
	ID=l[0]
	loc=l[1];
	locdic[loc]=int(ID)
ft.close()
print "Location ID dictionary created\n"

fin=open('hashtags_label_multiple.txt','r')
matrix=np.array([[0]*94]*94)

def populateMatrix(loclist):
	for i in range(0,len(loclist)):
		location=loclist[i].replace("'","")	#Removing useless single quotes
#		print "Current loc="+location
		ID1=locdic[location]
		for j in range(0,len(loclist)):
			location2=loclist[j].replace("'","")
			ID2=locdic[location2]
			matrix[ID1][ID2]+=1
			#print "updating "+str(i)+" "+str(j)+'\n'
for line in fin:
	l=line.rstrip().split('\t')
	ht=l[0]
	loclist=l[1].split(', ')
	#if ht in ht_list:
	populateMatrix(loclist)
fin.close()
#fout=open("matrix1.txt","w")
np.savetxt('matrix_loc.txt',matrix,delimiter=' ')
'''
for i in range(0,6):
	for j in range(0,6):
		fout.write(array_str(matrix[i][j])+" ")
	fout.write("\n")
fout.write(matrix)
'''
#fout.close()	
