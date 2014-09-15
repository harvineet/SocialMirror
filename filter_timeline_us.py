#restrict hashtags according to adopters in US

tag=set()
fr = open('tag_plot.txt', 'r')
for line in fr:
	line = line.rstrip()
	tag.add(line.replace('"',''))
fr.close()

count=0
with open('timeline_weng', 'r')as fr, open('timeline_weng_tag_plot','wb') as fd:
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if u[0] in tag: 
			fd.write(line+"\n")
			count+=1
print count