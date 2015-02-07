count=0
r=0
with open('fmdump.txt') as f:
	for line in f:
		line=line.rstrip().split(",")
		u=map(float,line)
		try:
			
			if ((u[1]-u[0]) >= 0.05952 or (u[1]-u[0]) <= -0.05952):
				# print u
				r+=1
			count+=1
		except:
			pass
print count
print r
print float(r)/count