#check missing tweets from extracted tweets from tweetfile* for crawl1, for >1500 tweets topics and considering filtered tags
import time
import re
import datetime
import dateutil.tz
import calendar
import sys
import os

def get_unix_time(time_stamp):
	dat = int(time_stamp[8:10])
	mon = int(months[(str(time_stamp[4:7])).lower()])
	yr = int(time_stamp[26:30])
	hr = int(time_stamp[11:13])
	min = int(time_stamp[14:16])
	sec = int(time_stamp[17:19])
	off1= int(time_stamp[21:23])
	off2 = int(time_stamp[23:25])
	a = datetime.datetime(yr, mon, dat, hr, min,sec, tzinfo=dateutil.tz.tzoffset(None, off1*3600 + off2*60))
	unix_time = calendar.timegm(a.utctimetuple())
	return unix_time
	
fr = open("../tweets6_1/filtered.txt",'r')
selected_users = set()
for line in fr:
	line = line.rstrip()
	selected_users.add(int(line))
fr.close()

pred_thr = 1500
tag_selected = dict()
tweets_selected = dict()
with open('../timeline_weng', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		tag = u[0]
		tweets_selected[tag] = []
		for i in range(1,pred_thr+1):
			timestamp = int(u[i][0:u[i].index(',')])
			author = int(u[i][u[i].index(',')+1 : ])
			tweets_selected[tag].append((timestamp,author))
		timestamp = int(u[pred_thr][0:u[pred_thr].index(',')])
		author = int(u[pred_thr][u[pred_thr].index(',')+1 : ])
		tag_selected[tag]=(timestamp,author)

path_tweet_extracts = 'tweet_extracts'
# fd = open("tweets_selected_comb.txt","w")
tags_sel = dict()
for tweet_folder in os.listdir(path_tweet_extracts):
	print "tweets folder", tweet_folder
	path_txtfile = os.path.join(path_tweet_extracts,tweet_folder)
	with open(path_txtfile, 'r') as fr:
		for line in fr:
			line = line.rstrip()
			u = line.split('\t')
			tweet_tag = u[0]
			tweet_text = u[1]
			tweet_author = int(u[2])
			tweet_time = int(u[3])
			if tweet_tag in tags_sel:
				tags_sel[tweet_tag].append((tweet_time,tweet_author))
			else:
				tags_sel[tweet_tag]=[(tweet_time,tweet_author)]
max_min_time = 0
max_time = 0
min_time = 0
for i in tags_sel:
	(max_act,_) = tag_selected[tag]
	if max(tags_sel[i],key=lambda item:item[0])[0] == max_act:
		max_time+=1
	(min_act,_) = tweets_selected[tag][0]
	if min(tags_sel[i],key=lambda item:item[0])[0] == min_act:
		min_time+=1
	if max(tags_sel[i],key=lambda item:item[0])[0] == max_act and min(tags_sel[i],key=lambda item:item[0])[0] == min_act:
		max_min_time+=1
print max_min_time,max_time,min_time
def list_cat(l):
	cat = []
	for x in l:
		cat+=x
	return cat
print len(tweets_selected.keys()),len(list_cat(tweets_selected.values()))
print len(tweets_selected.keys()),len(set(list_cat(tweets_selected.values())))
print len(tags_sel.keys()),len(list_cat(tags_sel.values()))
print len(tags_sel.keys()),len(set(list_cat(tags_sel.values())))
print len(set(list_cat(tweets_selected.values()))-set(list_cat(tags_sel.values())))

missing = set(list_cat(tweets_selected.values()))-set(list_cat(tags_sel.values()))
mis=[]
for (t,_) in missing:
	mis.append(t)
print max(mis),min(mis)
months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

"""path_tweet_extracts = '/mnt/filer01/Crawl1_extracts/comp_extracts'
folder_contents = [ f for f in os.listdir(path_tweet_extracts) if not os.path.isfile(os.path.join(path_tweet_extracts,f)) ]

start = int(sys.argv[1])
end = int(sys.argv[2])
fwritenum = sys.argv[1]

tags_org = set()
fd = open("/twitterSimulations/tweet_text/tweets_selected_tags_crawl1_"+fwritenum+".txt","w")
fd_err = open("/twitterSimulations/tweet_text/error_dump_crawl1_"+fwritenum+".txt","w")
count = 0
for tweet_folder in folder_contents:
	count = count + 1
	if count < start or count >= end:
		continue
	print "tweets folder", tweet_folder
	txtfile_contents = os.listdir(os.path.join(path_tweet_extracts,tweet_folder))
	for txtfile in txtfile_contents:
		if "tweetfile" in txtfile:
			tweetfile = txtfile
	path_txtfile = os.path.join(path_tweet_extracts,tweet_folder,tweetfile)
	even_line_num=0
	with open(path_txtfile, 'r') as fr:
		for line in fr:
			try:
				# line = line.rstrip()
				u = line.split('\t')
				if even_line_num==0 and len(u) == 8:
					tweet_text = u[0]
					tweet_author = int(u[2])
					tweet_time = get_unix_time(u[3])
					if(tweet_time >= 1395858601	 and tweet_time <= 1398796199 and tweet_author in selected_users):
						tweet_tags = set([tag.strip("#") for tag in tweet_text.split() if tag.startswith("#")])
						for tag in tweet_tags:
							tags_org.add(tag) # remove if addition takes time
							tag=tag.lower()
							if tag in tag_selected:
								(thr_timestamp,_) = tag_selected[tag]
								if tweet_time<=thr_timestamp: #tweets before pred thr
									fd.write(tag+"\t"+tweet_text+"\t"+str(tweet_author)+"\t"+str(tweet_time)+"\n")
				# else:
					# lang = u[-1]
					# hashtag = u[0].split(',')[:-1]
			except Exception as e:
				# print e
				# print line
				fd_err.write(line+"\n")
			even_line_num = 1 - even_line_num
fd.close()
fd_err.close()
with open("/twitterSimulations/tweet_text/tags_crawl1_"+fwritenum+".txt","w") as fd_tag:
	for i in tags_org:
		fd_tag.write(i+"\n")"""
