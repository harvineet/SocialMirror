# segment hashtags into words using code by Peter Norvig, removing numbers from tags

from ngrams import *
import re
def seg2(s): return segment2(s)[1]
def seg2num(s): return [",".join(segment2(w)[1]) for w in s]
def num_sep(tag):
	return re.findall(r'[\d.]+|\D+', tag) #[x for x in re.split(r'((\d*\.?\d*)+)',tag) if x is not '']
tag_split_num = []
with open('../tag_freq.csv', 'r') as fr:
	next(fr)
	for line in fr:
		line = line.rstrip()
		u = line.split(',')
		tag = u[0]
		tag_split_num.append((num_sep(tag),int(u[1]),tag)) # extract numbers from tag
		# tag_split_num.append((tag,int(u[1])))#numeric also
tags_sorted = sorted(tag_split_num,key=lambda x: x[1], reverse=True)
with open('../tag_segments.txt', 'w') as fd:
	for (i,_,tag) in tags_sorted:
		fd.write(tag+"\t"+",".join(seg2num(i))+"\n")
		# fd.write(i+"\t"+",".join(seg2(i))+"\n")
	