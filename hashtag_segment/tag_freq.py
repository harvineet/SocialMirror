# read hashtag dataset in weng format and extract hashtag with corresponding tweet counts

fr = open('../timeline_weng', 'r')
fr_lines = fr.readlines()
fr.close()
# numTweets=1500
fd = open("tag_freq.csv", 'w')
fd.write("tag,count\n")
for line in fr_lines:
	line = line.rstrip()
	u = line.split(' ')
	fd.write(str(u[0])+","+str(len(u)-1)+"\n")
fd.close()

