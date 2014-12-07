# read hashtag dataset in weng format and extract hashtag with corresponding tweet counts

fr = open('timeline_weng_fresh', 'r')
fr_lines = fr.readlines()
fr.close()
numTweets=5000
fd = open("tag_freq_5000.csv", 'w')
fd.write("tag,count\n")
for line in fr_lines:
	line = line.rstrip()
	u = line.split(' ')
	if len(u) <= numTweets:
			continue
	fd.write(str(u[0])+","+str(len(u)-1)+"\n")
fd.close()

