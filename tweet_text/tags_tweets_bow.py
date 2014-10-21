#extract tags and words from tweets from combined crawl files to preprocess and form bag of words for clustering
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
		
class Tseg(dict):
    "Segmentation of hashtags read from datafile."
    def __init__(self, data=[]):
        for key,seg in data:
            self[key] = seg
def datafile(name, sep='\t'):
    "Read key,value pairs from file."
    for line in file(name):
        yield line.split(sep)
tag_segment  = Tseg(datafile('tag_segments.txt'))

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
pred_thr = 1500
tag_selected = dict()
with open('../timeline_weng', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		timestamp = int(u[pred_thr][0:u[pred_thr].index(',')])
		author = int(u[pred_thr][u[pred_thr].index(',')+1 : ])
		tag = u[0]
		tag_selected[tag]=(timestamp,author)

path_tweet_extracts = 'tweet_extracts'
fd = open("tweets.txt","wb")
tags_sel = dict()
for tweet_folder in os.listdir(path_tweet_extracts):
	print "tweets folder", tweet_folder
	path_txtfile = os.path.join(path_tweet_extracts,tweet_folder)
	with open(path_txtfile, 'rb') as fr:
		for line in fr:
			try:
				line = line.rstrip()
				u = line.split('\t')
				tweet_tag = u[0]
				tweet_text = u[1].replace("\n","").replace("\r","") # \r present within tweets
				# tweet_author = int(u[2])
				# tweet_time = int(u[3])
				if tweet_tag in tags_sel:
					tags_sel[tweet_tag].append(tweet_text)
				else:
					tags_sel[tweet_tag] = [tweet_text]
				# fd.write(tweet_preprocess(tweet_text)+"\n")
				fd.write(tweet_text+"\n")
				# if(tweet_time >= 1395858601	 and tweet_time <= 1398796199 and tweet_author in selected_users):
						# tweet_tags = set([tag.strip("#") for tag in tweet_text.split() if tag.startswith("#")])
						# for tag in tweet_tags:
							# tags_org.add(tag) # remove if addition takes time
							# tag=tag.lower()
							# if tag in tag_selected:
								# (thr_timestamp,_) = tag_selected[tag]
								# if tweet_time<=thr_timestamp: #tweets before pred thr
									# fd.write(tag+"\t"+tweet_text+"\t"+str(tweet_author)+"\t"+str(tweet_time)+"\n")
			except Exception as e:
				print e
				# print line
fd.close()

# fd1 = open("tag_tweets_bow_lfrem.txt","wb")
# for i in tags_sel:
	# fd1.write(i+"\t"+" ".join(tags_sel[i])+"\n")
# fd1.close()
print len(tags_sel), len(tag_selected)
for i in tag_selected:
	if (i not in tags_sel):
		print i

"unique tags with capitalisation"
# path_tag_extracts = 'tag_extracts'
# tags_org = set()
# for tag_folder in os.listdir(path_tag_extracts):
	# print "tags folder", tag_folder
	# path_txtfile = os.path.join(path_tag_extracts,tag_folder)
	# with open(path_txtfile, 'r') as fr:
		# for line in fr:
			# line = line.rstrip()
			# tags_org.add(line)
# with open("tags_comb.txt","w") as fd_tag:
	# for i in tags_org:
		# fd_tag.write(i+"\n")
