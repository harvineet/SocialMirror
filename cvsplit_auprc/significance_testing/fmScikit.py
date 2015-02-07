#calculate fmeasure given the prediction probability and true label for classification runs on the dataset after cross validation using CGNP features on TweetDat
#
import numpy as np
from sklearn.metrics import precision_recall_fscore_support,f1_score
import random

y_true_ec = []
y_true_enc = []
y_predp_ec = []
y_predp_enc = []
fd=open('fmdump.txt','wb')
with open('WengDat/ec.csv') as fw, open('WengDat/cgnp_enc.csv') as fc:
	next(fw)
	next(fc)
	for line in fw:
		line=line.rstrip()
		u=line.split(',')
		y_true_ec.append(int(u[1][-1]))
		y_predp_ec.append(float(u[5].replace("*","")))
	for line in fc:
		line=line.rstrip()
		u=line.split(',')
		y_true_enc.append(int(u[1][-1]))
		y_predp_enc.append(float(u[5].replace("*","")))
		
# print sum(y_true_ec),len(y_true_ec)
# print sum(y_true_enc),len(y_true_enc)
y_pred_ec=[1 if x>0.444 else 0 for x in y_predp_ec]
y_pred_enc=[1 if x>0.482 else 0 for x in y_predp_enc]
# from sklearn import metrics
# print 'AUC: ',  metrics.roc_auc_score(np.array(y_true), np.array(y_pred))
# print  "----------------------------"
# print 'AUPRC: ',  metrics.average_precision_score(np.array(y_true), np.array(y_pred), average=None)

# _,_,ec_org,_= precision_recall_fscore_support(np.array(y_true_ec), np.array(y_pred_ec))
# _,_,enc_org,_= precision_recall_fscore_support(np.array(y_true_enc), np.array(y_pred_enc))
# print ec_org[1],enc_org[1]
ec_org = f1_score(np.array(y_true_ec), np.array(y_pred_ec), pos_label=1)
enc_org = f1_score(np.array(y_true_enc), np.array(y_pred_enc), pos_label=1)
print ec_org,enc_org

diff_org=enc_org-ec_org
print diff_org

if len(y_predp_ec)!=len(y_predp_enc):
	print "error example numbers"
	
runs = 100000
diff_runs=[]
r=0
for i in range(runs):
	a_run=y_predp_ec
	b_run=y_predp_enc
	for example in range(len(y_predp_ec)):
		if(random.random()<=0.5):
			a_run[example],b_run[example]=b_run[example],a_run[example]
	a_pred=[1 if x>0.444 else 0 for x in a_run]
	b_pred=[1 if x>0.482 else 0 for x in b_run]
	a_sw= f1_score(np.array(y_true_ec), np.array(a_pred), pos_label=1)
	b_sw= f1_score(np.array(y_true_enc), np.array(b_pred), pos_label=1)
	fd.write(str(a_sw)+","+str(b_sw)+"\n")
	diff_sw=b_sw-a_sw
	if (diff_sw>diff_org or diff_sw< -1*diff_org):
		r+=1
print r
print float(r)/runs
fd.close()