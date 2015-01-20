#compute fraction of tweets in each sentiment category and write to feature file. aggregate sentiment for consecutive tweets and count number of flips of sentiment feature.

import os, sys, io
from collections import Counter

filepath_write = 'tweet_sentiment.tsv'
fr = io.open(filepath_write,'r',encoding='utf8')

tags_sel = []
pred_thr = 1500
tags_viral = set()
avg_inter_tweet_time=dict()

tag_senti_seq = dict()
tag_senti_seq_aggr = dict()
tag_senti_flips = dict()
num_consecutive_tweets = 50

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
	
	if tag not in tag_senti_seq:
		tag_senti_seq[tag]=[]
	tag_senti_seq[tag].append(polarity)
	
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

for t in tag_senti_seq:
	tag_seq = tag_senti_seq[t]
	window_count=0
	num_flips = 0
	prev_s = '0'
	seq_aggr = []
	for j in range(0,len(tag_seq),num_consecutive_tweets):
		window_count+=1
		pol_count = Counter(tag_seq[j:j+num_consecutive_tweets])
		
		if pol_count['-1']>=pol_count['1'] and pol_count['-1']>=pol_count['0']:
			max_tw = '-1'
		elif pol_count['1']>=pol_count['-1'] and pol_count['1']>=pol_count['0']:
			max_tw = '1'
		else:
			max_tw = '0'
		#neglecting neutral sentiment
		# if pol_count['-1']>pol_count['1']:
			# max_tw = '-1'
		# elif pol_count['1']>pol_count['-1']:
			# max_tw = '1'
		# else:
			# max_tw = '0'
		
		seq_aggr.append(max_tw)
		if max_tw!=prev_s:
			# if max_tw!='0' and prev_s!='0':
				# num_flips+=2
			# else:
				# num_flips+=1
			num_flips+=1
		prev_s = max_tw
	tag_senti_flips[t] = float(num_flips)/window_count
	tag_senti_seq_aggr[t] = seq_aggr
path_output_file = 'sentiment_feature.csv'
with open(path_output_file,'wb') as fd:
	fd.write("TagName,PosPercentage,NeuPercentage,NegPercentage,PosNeuRatio,NumOfFlips\n")
	for ht in tags_sel:
		if ht in set(tags_sel)-tags_found:
			fd.write(ht+","+str(0)+","+str(1)+","+str(0)+","+str(0)+","+str(0)+"\n")
		else:
			if tag_sent[ht]['0']!=0:
				fd.write(ht+","+str(tag_sent[ht]['1'])+","+str(tag_sent[ht]['0'])+","+str(tag_sent[ht]['-1'])+","+str(tag_sent[ht]['1']/tag_sent[ht]['0'])+","+str(tag_senti_flips[ht])+"\n")
			else:
				fd.write(ht+","+str(tag_sent[ht]['1'])+","+str(tag_sent[ht]['0'])+","+str(tag_sent[ht]['-1'])+","+str(1)+","+str(tag_senti_flips[ht])+"\n")