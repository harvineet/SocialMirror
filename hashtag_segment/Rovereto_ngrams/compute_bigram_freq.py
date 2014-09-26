# read twitter corpus and extract word with corresponding freq occurrence counts
import gzip
count=0
with gzip.open('en.2grams.gz', 'r') as fr, open("freq_2gram.txt", 'wb') as fd:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		freq = sum(map(int,u[1::2]))
		if freq>1000:
			fd.write(u[0].lower()+"\t"+str(freq)+"\n")
			count+=freq
print count

#remove duplicates introduced due to converting to lower case and #,@,& characters
'''import re
words = dict()
pattern = re.compile('[\W_]+')
with open('freq_1gram_100.txt', 'r') as fr:
	for line in fr:
		line = line.rstrip()
		u = line.split('\t')
		word=u[0]
		bigram=word.split(' ')
		# for i in set(['#','@','&']):	
			# word = word.replace(i,'')
		word1 = pattern.sub('', bigram[0])
		word2 = pattern.sub('', bigram[1])
		if word1=='' or word2=='':
			continue
		if word not in words:
			words[word]=int(u[1])
		else:
			words[word]+=int(u[1])
with open("twitter_1w.txt", 'wb') as fd:
	for i in words.keys():
		fd.write(i+"\t"+str(words[i])+"\n")'''