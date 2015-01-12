#writes file to plot sentiment of tweets along with the class

import os, sys, io

filepath_write = 'tweet_sentiment.tsv'
fr = io.open(filepath_write,'r',encoding='utf8')

fw=open('tag_sentiment.tsv','wb')
fw.write('TweetNum\tTagName\tPolarity\tClass\n')

tags_sel = set()
pred_thr = 1500
tags_viral = set()
with open('../timeline_weng', 'r') as f1:
	for line in f1:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tags_sel.add(u[0])
		if len(u) > 10000:
			tags_viral.add(u[0])
found=set()
tags_found=set()
count=1
prev=''
tag_sent=dict()
tag_count=dict()
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	tag=u[0]
	if tag!=prev:
		count=1
		prev=tag
	if tag not in tags_sel:
		continue
	tags_found.add(tag)
	text=u[1]
	polarity=str(int((int(u[2])-2)/2.0))
	if tag not in tag_sent:
		tag_sent[tag]={'-1':0,'0':0,'1':0}
	tag_sent[tag][polarity]+=1
	if tag not in tag_count:
		tag_count[tag]=0
	tag_count[tag]+=1
	if tag in tags_viral:
		found.add(tag)
		fw.write(str(count)+'\t'+tag+'\t'+polarity+'\t1'+'\n')
	else:
		fw.write(str(count)+'\t'+tag+'\t'+polarity+'\t0'+'\n')
	count+=1
for t in tag_sent:
	for p in tag_sent[t]:
		tag_sent[t][p]=float(tag_sent[t][p])/tag_count[t]
aggr={'-1':0,'0':0,'1':0}
c1=0
for t in tag_sent:
	c1+=1
	for p in ['-1','0','1']:
		aggr[p]+=tag_sent[t][p]
for p in ['-1','0','1']:
	aggr[p]=aggr[p]/c1
print aggr
print c1
print len(tags_viral), len(tags_sel)
print len(found), len(tags_found)
# print tags_sel-tags_found
fr.close()
fw.close()