# to find inter tweet time in between 500 and 1000 tweets and choose time step size
import numpy as np
tweet_time = dict()
with open('timeline_weng','r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		tweet_time[u[0]] = []
		for i in range(1, len(u)):
			timestamp = int(u[i][0:u[i].index(',')])
			tweet_time[u[0]].append(timestamp)
avg = 0.0
tags = tweet_time.keys()
inter_tweet = []
for i in tags:
	for j in range(500,999):
		inter_tweet += [tweet_time[i][j] - tweet_time[i][j-1]]
avg = np.mean(inter_tweet)
sd = np.std(inter_tweet)
print avg, sd
with open('inter_tweet_time.txt','wb') as fr:
	for i in inter_tweet:
		fr.write(str(i)+"\n")