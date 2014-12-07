import numpy as np
from pandas import *
from sklearn.ensemble import RandomForestClassifier

def read_arff(f):
	from scipy.io import arff
	data, meta = arff.loadarff(f) 
	return DataFrame(data)

def kfold(clr,X,y,folds=10):
	from sklearn.cross_validation import StratifiedKFold
	from sklearn import metrics
	auc_sum=0
	comb_y_test = []
	comb_pred_test = []
	kf = StratifiedKFold(y, folds)
	for train_index, test_index in kf:
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]
		clr.fit(X_train, y_train)
		pred_test = clr.predict_proba(X_test)[:, 1]
		print metrics.roc_auc_score(y_test,pred_test)
		comb_y_test+=y_test.tolist()
		comb_pred_test+=pred_test.tolist()
		auc_sum+=metrics.roc_auc_score(y_test,pred_test)

	print 'AUC: ',  auc_sum/folds
	print  "----------------------------" 
	print 'AUC: ',  metrics.roc_auc_score(np.array(comb_y_test), np.array(comb_pred_test))
	print  "----------------------------"
	print 'AUPRC: ',  metrics.average_precision_score(np.array(comb_y_test), np.array(comb_pred_test), average=None)
	print  "----------------------------" 
	print clr.feature_importances_
	 



#read the dataset
X=read_arff('feature_name.arff')
y=X['Class']
y=np.array(y)
y = y.astype(int)
del X['Class']
print np.shape(X)
#changes N, and Y to 0, and 1 respectively

#initialize random forests (by defualt it is set to 10 trees)
rf=RandomForestClassifier(n_estimators=500, criterion='gini',oob_score=False,compute_importances=True)

#run algorithm
kfold(rf,np.array(X),y)
