#reads tweets before prediction threshold extracted from both crawls and stored in pickle file and queries sentiment140 service to classify sentiment contained in tweets
#3663170 unique tweets in timeline_weng not found from crawls

import json
import urllib2, urllib, os, sys, io
import cPickle as pickle

filepath_write = 'tweet_sentiment.tsv'
fw = io.open(filepath_write,'w',encoding='utf8')
fp = open('tweet_sentiment.pickle','wb')
path_tweet_extracts = '/twitterSimulations/tweet_text/tweet_text_check/check1/'
# path_tweet_extracts = 'tweet_text_check/'
# fd = open("tweets_present.txt","wb")
tags_sel = dict()
for tweet_folder in os.listdir(path_tweet_extracts):
	if "tweets" not in tweet_folder:
		continue
	print "tweets folder", tweet_folder
	path_txtfile = os.path.join(path_tweet_extracts,tweet_folder)
	with open(path_txtfile, 'r') as fr:
		try:
			while True:
				u = pickle.load(fr)
				# line = line.rstrip()
				# u = line.split('\t')
				tweet_tag = u[0]
				tweet_text = u[1].replace("\n","").replace("\r","") # \r present within tweets
				# tweet_author = int(u[2])
				tweet_time = int(u[3])
				if tweet_tag in tags_sel:
					tags_sel[tweet_tag].append((tweet_text,tweet_time))
				else:
					tags_sel[tweet_tag] = [(tweet_text,tweet_time)]
				# fd.write(tweet_preprocess(tweet_text)+"\n")
				# fd.write(tweet_text+"\n")
		except EOFError:
			print "EOF"
pickle.dump(tags_sel,open("tag_tweet_time.pickle",'w'))
for i in tags_sel:
	print i
	text=[]
	# max_query=5000
	time_sorted = sorted(tags_sel[i],key=lambda x: x[1])
	for (j,_) in time_sorted[0:1500]:
		text.append({"text":j})	
	
	# try:
	proxy = urllib2.ProxyHandler({'https': '10.10.78.21:3128','http': '10.10.78.21:3128'})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	
	query_args = { 'appid':'hitsugayasquad10@yahoo.com' }
	encoded_args = urllib.urlencode(query_args)
	url = 'http://www.sentiment140.com/api/bulkClassifyJson?' + encoded_args
	
	payload = {"language": "auto", "data": text}
	req = urllib2.Request(url, data=json.dumps(payload))
	url_req = urllib2.urlopen(req)
	json_obj = url_req.read().decode('latin-1')#('utf-8')
	parsed_json = json.loads(json_obj)
	pickle.dump(parsed_json,fp)
	for t in parsed_json["data"]:
		fw.write(unicode(i)+'\t'+unicode(t["text"])+'\t'+str(t["polarity"])+"\n")
	# except Exception as e:
		# print e
		# print json_obj
fw.close()