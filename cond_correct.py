# file to create the features for different prediction threshold, virality threshold and set of topics remains same, adding std of conductance features
import json
import sys
import time
import datetime
import dateutil.tz
import calendar
import math
from os import listdir
from os.path import isfile, join

id_not_found = 0

def average(s): return sum(s) * 1.0 / len(s)

def stdev(s):
	avg = average(s)
	variance = map(lambda x: (x - avg)**2, s)
	return math.sqrt(average(variance))
	
for pred_thr in [200,250,500,750,1000]:#200,250,500,750,1000,
	fr = open('timeline_weng', 'r')
	fd=open("./conductance_std_features/time_divide/feature_"+str(pred_thr)+"_no5hr.csv",'w')
	fr1=open("./conductance_std_features/feature_"+str(pred_thr)+"_no5hr.csv",'rb')
	_=fr1.readline()
	fd_cond=open("./conductance_std_features/cond_values_all/feature_"+str(pred_thr)+"_no5hr.csv",'rb')
	_=fd_cond.readline()
	fd.write("RatioSecondtoFirst,RatioSelfInitCommu,RatioCrossGeoEdges,#globalAdoptersFollowers,#globalAdopters,#heavyusers,Density,LargestSize,NumEdges,Conduct1,Conduct2,Conduct3,Conduct4,Conduct2d,NumTweets,TimeFirst1000,NoOfAdopters,Conductance,RatioOfSingletons,RatioOfConnectedComponents,InfectedCommunities,UsageEntropy,NumOfRT,NumOfMention,IntraRT,IntraMen,Conduct1_std,Conduct2_std,Conduct3_std,Conduct4_std,Conduct2d_std,Conductance_std,Class\n")
	for line in fr:
		line = line.rstrip()
		u = line.split(' ')
		if len(u) <= pred_thr:
			continue
		timestamp = 0
		numTweets = 0
		timestamp_col = []
		numTweets1 = 0
		for i in range(1, len(u)):
			timestamp = int(u[i][0:u[i].index(',')])
			numTweets1 = i
			if(numTweets1 > pred_thr): #timestamp - int(u[1][0:u[1].index(',')]) > 18000 and 
				break
			if(timestamp - int(u[1][0:u[1].index(',')]) < 18000):
				numTweets = i
			timestamp_col.append(timestamp)
		
		features_line=fr1.readline()
		features_line=features_line.rstrip()
		features = features_line.split(',')
		cond_all_line = fd_cond.readline()
		cond_all_line=cond_all_line.rstrip()
		expose_col = [float(x) for x in cond_all_line.split(',')[1:-1]]
		
		l = len(expose_col) - 1
		expose1 = 0
		expose2 = 0
		expose3 = 0
		expose4 = 0
		#expose5 = 0
		expose2d = 0
		# c_expose1 = []
		# c_expose2 = []
		# c_expose3 = []
		# c_expose4 = []
		## c_expose5 = []
		# c_expose2d = []
		# c_cond = expose_col[-10:]
		
		# for i in reversed(range(10)):
			# try:
				# expose1 = (expose_col[l-i] - expose_col[l-i-20])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-20])
				# c_expose1.append(expose1)
				# expose2 = (expose_col[l-i] - expose_col[l-i-50])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-50])
				# c_expose2.append(expose2)
				# expose3 = (expose_col[l-i] - expose_col[l-i-100])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-100])
				# c_expose3.append(expose3)
				# if(pred_thr==200 or pred_thr==250):
					# expose4 = (expose_col[l-i] - expose_col[0])*36000000/(timestamp_col[l-i] - timestamp_col[0]) # 250 not correct, changes for different i
					# c_expose4.append(expose4)
				# else:
					# expose4 = (expose_col[l-i] - expose_col[l-i-250])*36000000/(timestamp_col[l-i] - timestamp_col[l-i-250])
					# c_expose4.append(expose4)
				## expose5 = (expose_col[l] - expose_col[l-500])*36000000/(timestamp_col[l] - timestamp_col[l-500])
				# pexpose2 = (expose_col[l-i-50] - expose_col[l-i-100])*36000000/(timestamp_col[l-i-50] - timestamp_col[l-i-100])
				# expose2d = (expose2 - pexpose2)*36000000/(timestamp_col[l-i] - timestamp_col[l-i-50])
				# c_expose2d.append(expose2d)
			# except:
				# print u[0], i
		try:
			expose1 = (expose_col[l] - expose_col[l-20])*36000000/(timestamp_col[l] - timestamp_col[l-20])
			expose2 = (expose_col[l] - expose_col[l-50])*36000000/(timestamp_col[l] - timestamp_col[l-50])
			expose3 = (expose_col[l] - expose_col[l-100])*36000000/(timestamp_col[l] - timestamp_col[l-100])
			expose4 = (expose_col[l] - expose_col[l-250])*36000000/(timestamp_col[l] - timestamp_col[l-250])
			#expose5 = (expose_col[l] - expose_col[l-500])*36000000/(timestamp_col[l] - timestamp_col[l-500])
			pexpose2 = (expose_col[l-50] - expose_col[l-100])*36000000/(timestamp_col[l-50] - timestamp_col[l-100])
			expose2d = (expose2 - pexpose2)*36000000/(timestamp_col[l] - timestamp_col[l-50])
		except Exception as e:
			print u[0]
			print e
		if len(u) > 10000:
			'''fdtemp = open('dumpviral/'+u[0], 'w')
			for i in range(0, len(timestamp_col)):
				fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
			fdtemp.close()'''
			fd.write(','.join(features[1:10])+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+','.join(features[15:18])+','+str(expose_col[-1])+','+','.join(features[19:27])+',1\n')
			
		else:
			'''fdtemp = open('dumpnviral/'+u[0], 'w')
			for i in range(0, len(timestamp_col)):
				fdtemp.write(str(timestamp_col[i]) + ' ' + str(expose_col[i]) + '\n')
			fdtemp.close()'''
			fd.write(','.join(features[1:10])+',' + str(expose1)+','+str(expose2)+','+str(expose3)+','+str(expose4)+','+str(expose2d)+','+','.join(features[15:18])+','+str(expose_col[-1])+','+','.join(features[19:27])+',0\n')
			
	fd.close()
	fd_cond.close()
	fr1.close()

print id_not_found
