#extract tweets from tweets* for twitter November 2013 dataset
# format:
# <text>\t<tweetid>\t<userid>\t<tweettime>\n
import sys
import os
import json
import io

path_tweet_extracts = '/mnt/filer01/tweets_repository/Nov2013/tweet_files/'
folder_contents = os.listdir(path_tweet_extracts)

f1 = io.open("/mnt/filer01/tweets_repository/Nov2013/tweets.txt","w",encoding='utf8')
fe = io.open("/mnt/filer01/tweets_repository/Nov2013/error_dump.txt","w",encoding='utf8')

for tweet_folder in folder_contents:
	print "tweets folder", tweet_folder
	path_txtfile = os.path.join(path_tweet_extracts,tweet_folder)
	with open(path_txtfile, 'r') as fr:
		for line in fr:
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
					f1.write((tweet_data[i]['text'])+'\t'+tweet_data[i]["id_str"]+'\t'+tweet_data[i]["user"]["id_str"]+'\t'+tweet_data[i]["created_at"])
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
					"""for j in range(0,len(tweet_data[i]["entities"]["hashtags"])):
						f1.write(unicode(tweet_data[i]["entities"]["hashtags"][j]["text"])+",")
					f1.write(unicode('\t'))
					if tweet_data[i]["lang"]!=None:   # check language of tweet
						lang=unicode(tweet_data[i]["lang"])  # tweet id of the tweet it is a reply of
						f1.write('lang\t'+lang)
					else:
						f1.write(unicode('und'))   #print  nl if lang undefined"""
					# f1.write(unicode('\n'))
			except Exception as e:
				print e
				fe.write(line+unicode('\n'));
				# continue
f1.close()
fe.close()
