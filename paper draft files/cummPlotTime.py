# read dataset in weng format and make cummulative plot for observation time

fr = open('timeline_50_fresh.dat', 'r')#dif_timeline1s_weng for all topics
fr_lines = fr.readlines()
fr.close()
numTweets=50
fd = open("cummObsTime_weng.csv", 'w')
fd.write("topic,time\n")
for line in fr_lines:
	line = line.rstrip()
	u = line.split(' ')
	tweets = u[1:]
	timestamp = int(tweets[0][0:tweets[0].index(',')])
	timestamp_n = int(tweets[numTweets-1][0:tweets[numTweets-1].index(',')])
	time_day = float(timestamp_n - timestamp)/(24*3600)
fd.write(str(time_day)+"\n")
	
fd.close()

