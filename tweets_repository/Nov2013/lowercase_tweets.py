# convert processed tweet text to lowercase and remove punctuations
import sys
# from string import punctuation
with open(sys.argv[1]) as fr, open(sys.argv[2],'wb') as fd:
	for line in fr:
		line = line.rstrip()
		# line = line.rstrip().split(" ")
		# lw = []
		# for word in line:
			# word = word.lower()
			# for p in list(punctuation):
				# word=word.replace(p,'')
			# if word=='':
				# continue
			# lw.append(word)
		# fd.write(" ".join(lw)+"\n")
		fd.write(line.lower()+"\n")