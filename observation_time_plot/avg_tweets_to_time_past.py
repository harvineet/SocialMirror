# read dataset in weng format and make avg num of tweets for time since start

fr = open('timeline_tag.anony_modified1.dat', 'r')#../paper draft files/community based prediction/virality2013/timeline_tag.anony.dat
fr_lines = fr.readlines()
fr.close()
fd = open("avgTweetToTime.csv", 'w')
fd.write("Time,AvgNumTweets\n")
numTweetsThreshold=50
for time_elapsed in range(5,10):
	avg = 0
	num_tweets = 0
	num_topics = 0
	for line in fr_lines:
		line = line.rstrip()
		u = line.split(' ')
		tweets = u[1:]
		if len(tweets) < numTweetsThreshold:
			continue
		for numTweets in range(0,len(tweets)):
			timestamp = int(tweets[0][0:tweets[0].index(',')])
			timestamp_n = int(tweets[numTweets][0:tweets[numTweets].index(',')])
			if (timestamp_n-timestamp) > time_elapsed*24*3600:
				break
			num_tweets += 1
		num_topics += 1
	print num_topics
	avg = float(num_tweets)/num_topics
	fd.write(str(time_elapsed)+","+str(avg)+"\n")
	
fd.close()

