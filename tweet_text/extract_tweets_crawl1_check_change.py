#extract tweets from tweetfile* for crawl1, for >1500 tweets topics and considering filtered tags
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
"""	
fr = open("/twitterSimulations/filtered.txt",'r')
selected_users = set()
for line in fr:
	line = line.rstrip()
	selected_users.add(int(line))
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
		tag_selected[tag]=(timestamp,author)"""

months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

path_tweet_extracts = '/mnt/filer01/Crawl1_extracts/comp_extracts'
folder_contents = [ f for f in os.listdir(path_tweet_extracts) if not os.path.isfile(os.path.join(path_tweet_extracts,f)) ]

start = int(sys.argv[1])
end = int(sys.argv[2])
fwritenum = sys.argv[1]

tags_org = set()
fd = open("/twitterSimulations/tweet_text/tweet_text_check/tweets_selected_tags_crawl1_"+fwritenum+".txt","w")
fd_err = open("/twitterSimulations/tweet_text/tweet_text_check/error_dump_crawl1_"+fwritenum+".txt","w")
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
		line = fr.readline()
		while line != '':
			# try:
			# line = line.rstrip()
			u = line.split('\t')
			cut_count=0
			while len(u)!=8 and cut_count<20:
				cut_count+=1
				cut_line = fr.readline()
				if cut_line=='':
					break
				print cut_line
				line = line.rstrip()+cut_line.rstrip()
				u = line.split('\t')
			# if even_line_num==0: #and len(u) == 8:
			print "(1)",line
			# last_pos = fr.tell()
			# print next(fr)
			# fr.seek(last_pos)
			
			line = fr.readline()
			print "(2)",line
			line = fr.readline()
			
			tweet_text = u[0]
			tweet_author = int(u[2])
			tweet_time = get_unix_time(u[3])
			"""if(tweet_time >= 1395858601	 and tweet_time <= 1398796199 and tweet_author in selected_users):
				tweet_tags = [tag.strip("#") for tag in tweet_text.split() if tag.startswith("#")]
				for tag in tweet_tags:
					tags_org.add(tag) # remove if addition takes time
					tag=tag.lower()
					if tag in tag_selected:
						(thr_timestamp,_) = tag_selected[tag]
						if tweet_time<=thr_timestamp: #tweets before pred thr
							fd.write(tag+"\t"+tweet_text+"\t"+str(tweet_author)+"\t"+str(tweet_time)+"\n")"""
				# else:
					# lang = u[-1]
					# hashtag = u[0].split(',')[:-1]
			"""except Exception as e:
				# print e
				# print line
				fd_err.write(line+"\n")"""
			# _=next(fr)
			# even_line_num = 1 - even_line_num
fd.close()
fd_err.close()
# with open("/twitterSimulations/tweet_text/tags_crawl1_"+fwritenum+".txt","w") as fd_tag:
	# for i in tags_org:
		# fd_tag.write(i+"\n")
