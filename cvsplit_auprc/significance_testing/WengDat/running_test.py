count=0
r=0
with open('fmdump1.txt') as f:
	for line in f:
		line=line.rstrip().split(",")
		u=map(float,line)
		try:
			
			if ((u[1]-u[0]) >= 0.114624505929 or (u[1]-u[0]) <= -0.114624505929):
				print u
				r+=1
			count+=1
		except:
			pass
print count
print r
print float(r)/count