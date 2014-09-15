# read hashtag dataset and split hashtag into candidate words to look up in dictionary

# check capitalised version of hashtag #incomplete
tag_split = dict()
tag_words = set()
with open('tag_freq.csv', 'r') as fr:
	next(fr)
	for line in fr:
		line = line.rstrip()
		u = line.split(',')
		tag = u[0]
		tag_split[tag]=[]
		# extract numbers from tag
		for i in range(0,len(tag)):
			if tag[i] #int
		tag_words.add()#non-numeric

fr.close()
cand = set()
for tag in tag_words:
	for i in range(0,len(tag)):
		cand.add(tag[0:i+1]) #2 word partition
		cand.add(tag[i+1:])

