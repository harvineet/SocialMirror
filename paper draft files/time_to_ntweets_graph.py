# read dataset in weng format and make avg time taken for n tweets graph

fr = open('timeline_50_fresh.dat', 'r')#dif_timeline1s_weng for all topics
fr_lines = fr.readlines()
fr.close()
fd = open("avgTimeToNtweet.csv", 'w')
fd.write("NumTweets,AvgTime\n")
#for numTweets in range(1,395180):
for numTweets in range(1,363519):#timeline_tag.anony.dat
	avg = 0
	num_topic = 0
	sum_topic = 0
	for line in fr_lines:
		line = line.rstrip()
		u = line.split(' ')
		tweets = u[1:]
		if len(tweets) < numTweets:
			continue
		timestamp = int(tweets[0][0:tweets[0].index(',')])
		timestamp_n = int(tweets[numTweets-1][0:tweets[numTweets-1].index(',')])
		num_topic += 1
		sum_topic += (timestamp_n - timestamp)
	avg = float(sum_topic)/(24*60*60*num_topic)
	fd.write(str(numTweets)+","+str(avg)+"\n")
	
fd.close()

