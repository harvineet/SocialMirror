# read dataset in weng format and make cummulative plot for observation time

fr = open('../timeline_weng', 'r')#timeline_tag.anony_modified1.dat
fr_lines = fr.readlines()
fr.close()
numTweets=1500
fd = open("cummObsTime_our.csv", 'w')
fd.write("variable,value\n")
for line in fr_lines:
	line = line.rstrip()
	u = line.split(' ')
	if len(u) <= numTweets:
			continue
	tweets = u[1:]
	timestamp = int(tweets[0][0:tweets[0].index(',')])
	timestamp_n = int(tweets[numTweets-1][0:tweets[numTweets-1].index(',')])
	time_day = float(timestamp_n - timestamp)/(24*3600)
	fd.write("TwitDat,"+str(time_day)+"\n")
	
fd.close()

