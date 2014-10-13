#extract tags and tweets from combined crawl files, clean tweets
import time
import re
import sys
import os
# from string import punctuation

# tweet = tweet.replaceAll("\\s*RT\\s*@\\w+:\\s*","");//removes "RT @foobar:"
# tweet = tweet.replaceAll("https?:[^\\s]*",""); //removes "http://foo" "https://bar"
# regHttp = re.compile('(http://)[a-zA-Z0-9]*.[a-zA-Z0-9/]*(.[a-zA-Z0-9]*)?')
# regAt = re.compile('@([a-zA-Z0-9]*[*_/&%#@$]*)*[a-zA-Z0-9]*')
# pattern = re.compile('[\W_]+')
# word = pattern.sub('', word)

def tweet_preprocess(tweet):
	tweet_norm = ""
	for word in tweet_text.split():
		if word.startswith("#"):
			# word = tag_segment[word.strip("#").lower()] # for bag of word; segment on capitalisation not done, RT, @ not removed
			word = word.strip("#").lower() # every tag made lower case, capitalisation in tag not used
		elif word.startswith("http://") or word.startswith("https://"):
			continue
		# else:
			# for p in list(punctuation): # ['#','@','&','?','-','.','!']
				# word=word.replace(p,'')
		if word=='':
			continue
		tweet_norm = tweet_norm+ " " + word
	return tweet_norm

fd = open("tweets_old.txt","w")
path_txtfile = 'tweets.txt'
with open(path_txtfile, 'r') as fr:
	for line in fr:
		try:
			line = line.rstrip()
			u = line.split('\t')
			tweet_text = u[0]
			# tweet_author = int(u[2])
			# tweet_time = int(u[3])
			# fd.write(tweet_preprocess(tweet_text)+"\n")
			fd.write(tweet_text+"\n")
		except Exception as e:
			print e
			# print line
fd.close()
