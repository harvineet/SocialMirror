#!/usr/bin/python
import time
import sys
import io
import json
import os
tic1 = time.clock()
folder = sys.argv[1];
folder_contents = os.listdir(folder)
file_paths = []
if folder_contents==['mnt']:
	print 'mnt in', folder
	txtfile = "tweets"+folder.split('_')[0]+".txt";
	path = folder+"/mnt/"+txtfile;
	file_paths.append(path)
else:
	for txtfile in folder_contents:
		print "tweets_portion in", txtfile
		path = "/mnt/filer01/Crawl1_extracts/TweetExtracts/"+folder+"/"+txtfile;
		file_paths.append(path)
# fu = io.open("/mnt/filer01/Crawl1_extracts/TweetExtracts/"+folder+"/userfile_"+folder+".txt",'w',encoding='utf8')
fe = io.open(folder+"/errorfile_"+folder+".txt",'w',encoding='utf8')
f1 = io.open(folder+"/tweetfile_"+folder+".txt",'w',encoding='utf8')
for path in file_paths:
	with open(path,'r') as fp:
		for line in fp:
			try:
				data = json.loads(line);
				tweet_data=data['tweets']
				"""fu.write(unicode(data['author'])+'\t') #user id of the author of tweet
				fu.write(unicode(tweet_data[0]['user']['screen_name']+'\t'))
				fu.write(unicode(tweet_data[0]['user']['followers_count'])+'\t')
				fu.write(unicode(tweet_data[0]['user']['friends_count'])+'\t')
				fu.write(unicode(tweet_data[0]['user']['listed_count'])+'\t')
				fu.write(unicode(tweet_data[0]['user']['statuses_count'])+'\t')
				fu.write(unicode(tweet_data[0]['user']['statuses_count'])+'\t')
				if tweet_data[0]['user']['time_zone']!=None:
					fu.write(unicode(tweet_data[0]['user']['time_zone']))
				else:
					fu.write(unicode('nt'))
				fu.write(unicode('\n'));"""
				for i in range(0,len(tweet_data)):
					f1.write((tweet_data[i]['text'])+'\t'+tweet_data[i]["id_str"]+'\t'+tweet_data[i]["user"]["id_str"]+'\t'+tweet_data[i]["created_at"]+'\t'+ unicode(tweet_data[i]["favorited"])+'\t'+unicode(tweet_data[i]["favorite_count"])+'\t'+unicode(tweet_data[i]["retweet_count"])+'\t')
					# for j in range(0,len(tweet_data[i]["entities"]["user_mentions"])): # checking length of users mentioned
						# s1=unicode(tweet_data[i]["entities"]["user_mentions"][j-1]["id"])			
						# f1.write(s1+',') # writing list of users mentioned seperated by comma
					# if tweet_data[i]['coordinates']!=None:
						# f1.write(unicode(tweet_data[i]['coordinates']['coordinates'][0])+','+unicode(tweet_data[i]['coordinates']['coordinates'][1]))
					# else:
						# f1.write(unicode('nc')) # print nc if no cordinates arre given
					f1.write(unicode('\n'))
					# if 'retweeted_status' in tweet_data[i]:  # check whether a retweet or not
						# retweet_id=unicode(tweet_data[i]['retweeted_status']['id'])  #tweet id of the original tweeter
						# retweet_user_id=unicode(tweet_data[i]['retweeted_status']['user']['id']) #user id of the original tweeter
						# retweet_created_at=unicode(tweet_data[i]['retweeted_status']['created_at']) # time of the original tweet
						# f1.write('ret\t'+retweet_id+'\t'+ retweet_user_id+'\t'+retweet_created_at+'\t') # original tweet detail
					# else:
						# f1.write(unicode('f\t'))
					# if tweet_data[i]["in_reply_to_status_id"]!=None:   # check whether a reply
						# reply_status_id=unicode(tweet_data[i]["in_reply_to_status_id"])  # tweet id of the tweet it is a reply of
						# reply_user_id=unicode(tweet_data[i]["in_reply_to_user_id"])      # user id of the tweet it is a reply of
						# f1.write('rep\t'+reply_status_id+'\t'+reply_user_id+'\t')
					# else:
						# f1.write(unicode('nr\t'))   #print  nr if not a reply
					for j in range(0,len(tweet_data[i]["entities"]["hashtags"])):
						f1.write(unicode(tweet_data[i]["entities"]["hashtags"][j]["text"])+",")
					f1.write(unicode('\t'))
					if tweet_data[i]["lang"]!=None:   # check language of tweet
						lang=unicode(tweet_data[i]["lang"])  # tweet id of the tweet it is a reply of
						f1.write('lang\t'+lang)
					else:
						f1.write(unicode('und'))   #print  nl if lang undefined
					f1.write(unicode('\n'))
			except:
				fe.write(line+unicode('\n'));
				continue
f1.close();
fe.close();
# fu.close();
toc1 = time.clock()
print "initial real spread9", (toc1-tic1)*1000