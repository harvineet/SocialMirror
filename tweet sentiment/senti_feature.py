import os, sys, io

filepath_write = 'tweet_sentiment.tsv'
fr = io.open(filepath_write,'r',encoding='utf8')

tags_sel = []
pred_thr = 1500
tags_viral = set()
with open('../timeline_weng', 'r') as f1:
	for line in f1:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tags_sel.append(u[0])
		if len(u) > 10000:
			tags_viral.add(u[0])
found=set()
tags_found=set()
avg_tweets_found=0
count=1
prev=''
tag_sent=dict()
tag_count=dict()
for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	tag=u[0]
	if tag!=prev:
		avg_tweets_found+=count-1
		count=1
		prev=tag
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
	count+=1
avg_tweets_found+=count-1
for t in tag_sent:
	for p in tag_sent[t]:
		tag_sent[t][p]=float(tag_sent[t][p])/tag_count[t]

print len(tags_viral), len(tags_sel)
print len(found), len(tags_found)
# print set(tags_sel)-tags_found
print float(avg_tweets_found)/len(tags_found)
fr.close()

path_output_file = 'sentiment_feature.csv'
with open(path_output_file,'wb') as fd:
	fd.write("TagName,PosPercentage,NeuPercentage,NegPercentage,PosNeuRatio\n")
	for ht in tags_sel:
		if ht in set(tags_sel)-tags_found:
			fd.write(ht+","+str(0)+","+str(1)+","+str(0)+","+str(0)+"\n")
		else:
			if tag_sent[ht]['0']!=0:
				fd.write(ht+","+str(tag_sent[ht]['1'])+","+str(tag_sent[ht]['0'])+","+str(tag_sent[ht]['-1'])+","+str(tag_sent[ht]['1']/tag_sent[ht]['0'])+"\n")
			else:
				fd.write(ht+","+str(tag_sent[ht]['1'])+","+str(tag_sent[ht]['0'])+","+str(tag_sent[ht]['-1'])+","+str(1)+"\n")