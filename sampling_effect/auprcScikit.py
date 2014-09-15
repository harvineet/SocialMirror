#calculate auprc and auroc given the prediction probability and true label for test sets combined for different folds, ( )+ to ,; ,\n, to \n; ,+, to ,; empty line at the eof
import numpy as np

comb_y_test = []
comb_pred_test = []
with open('predProb.txt') as f: #predProb_nosamp.txt
	next(f)
	for line in f:
		line=line.rstrip()
		u=line.split(',')
		if len(u)!=4:
			print "Error", line
		comb_y_test.append(int(u[1][-1]))
		if (int(u[2][-1]) == 0):
			comb_pred_test.append(1-float(u[3]))
		else:
			comb_pred_test.append(float(u[3]))
		
from sklearn import metrics
print 'AUC: ',  metrics.roc_auc_score(np.array(comb_y_test), np.array(comb_pred_test))
print  "----------------------------"
print 'AUPRC: ',  metrics.average_precision_score(np.array(comb_y_test), np.array(comb_pred_test), average=None)