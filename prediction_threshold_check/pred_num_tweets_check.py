# read weka prediction output and get num of tweets considered for correctly predicted viral topics
# incomplete, not correct
numtweets = []
fr1 = open("feature_1000_5hr.csv", 'r')
next(fr1)
org_class=[]
for line in fr1:
	line=line.rstrip()
	u=line.split(',')
	numtweets.append(int(u[6]))
	org_class.append(int(u[-1]))
fr1.close()

fr = open('pred_output_feature_10000.csv', 'r')
fr_lines = fr.readlines()
fr.close()
pred=dict()

thresh= 0.158
pred_viral_numtweets=[]
for line in fr:
	line = line.rstrip()
	u = line.split(',')
	pred[int(u[6])]=float(u[5])
	if org_class[int(u[6])-1] == 1 and float(u[5])>=thresh:
		pred_viral_numtweets.append(numtweets[int(u[6])-1])
		
print pred_viral_numtweets


