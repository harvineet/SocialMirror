#extract tweets from tweetfile* for round2, for >1500 tweets topics and considering time_overlap
import time
import re
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
	
store = dict()
fr = open('/twitterSimulations/time_overlap.txt', 'r')
for i in fr:
	i = i.rstrip()
	u = i.split('\t')
	store[long(u[0])] = long(u[1])
fr.close()

print "Overlap Read\n"

rev_map_id = dict()
fr = open("/twitterSimulations/graph/map.txt")
for line in fr:
	line = line.rstrip()
	u = line.split(' ')
	rev_map_id[int(u[1])] = int(u[0])
fr.close()

pred_thr = 1500
tag_selected = dict()
with open('/twitterSimulations/timeline_data/timeline_weng', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		timestamp = int(u[pred_thr][0:u[pred_thr].index(',')])
		author = int(u[pred_thr][u[pred_thr].index(',')+1 : ])
		tag = u[0]
		tag_selected[tag]=(timestamp,author)

tags_org = set()
fd = open("/twitterSimulations/tweet_text/tweets_selected_tags.txt","w")

months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

path_tweet_extracts = '/mnt/filer01/Crawl1_extracts/comp_extracts'
folder_contents = os.listdir(path_tweet_extracts)
for tweet_folder in folder_contents:
		print "tweets folder", tweet_folder
		txtfile_contents = os.listdir(os.path.join(path_tweet_extracts,tweet_folder))
		for txtfile in txtfile_contents:
			if "tweetfile" in txtfile:
				tweetfile = txtfile
		path_txtfile = os.path.join(path_tweet_extracts,tweet_folder,tweetfile)
		even_line_num=0
		with open(path_txtfile, 'r') as fr:
			for line in fr:
				line = line.rstrip()
				u = line.split('\t')
				if even_line_num==0:
					tweet_text = u[0]
					if(long(u[2]) in store):
						tweettime_author = store[long(u[2])]
					else:
						tweettime_author = 0
					tweet_tags = set([tag.strip("#") for tag in tweet_text.split() if tag.startswith("#")])
					for tag in tweet_tags:
						tags_org.add(tag) # remove if addition takes time
						tag=tag.lower()
						if tag in tag_selected:
							(thr_timestamp,_) = tag_selected[tag]
							if get_unix_time(u[3])>tweettime_author:
								if get_unix_time(u[3])<=thr_timestamp:
									fd.write(tweet_text+"\n")
				# else:
					# lang = u[-1]
					# hashtag = u[0].split(',')[:-1]
				even_line_num = 1 - even_line_num
fd.close()
with open("/twitterSimulations/tweet_text/tweet_tags.txt","w") as fd_tag:
	for i in tags_org:
		fd_tag.write(i+"\n")
