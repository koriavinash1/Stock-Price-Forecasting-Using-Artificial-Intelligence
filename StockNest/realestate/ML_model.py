
import numpy as np
import pandas as pd
import gc
import xgboost as xgb
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier,\
				VotingClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz


def mainNetwork():
	print('Loading data ...')

	base_path = '/media/koriavinash/New Volume/Research/Deep Learning/hackerearth/StockNest_Dynamic/StockNest/realestate/'
	train = pd.read_csv( base_path + 'dataset/train_2016_v2.csv/train_2016_v2.csv')
	prop = pd.read_csv(base_path+ 'dataset/properties_2016.csv/properties_2016.csv')
	# sample = pd.read_csv(base_path + 'dataset/sample_submission.csv')

	print('Creating training set ...')

	df_train = train.merge(prop, how='left', on='parcelid')

	x_train = df_train.drop(['parcelid', 'logerror', 'transactiondate', 'propertyzoningdesc', 'propertycountylandusecode'], axis=1)
	y_train = df_train['logerror'].values
	print(x_train.shape, y_train.shape)

	train_columns = x_train.columns

	for c in x_train.dtypes[x_train.dtypes == object].index.values:
	    x_train[c] = (x_train[c] == True)

	del df_train; gc.collect()

	split = 80000
	x_train, y_train, x_valid, y_valid = x_train[:split], y_train[:split], x_train[split:], y_train[split:]

	print('Building DMatrix...')

	d_train = xgb.DMatrix(x_train, label=y_train)
	d_valid = xgb.DMatrix(x_valid, label=y_valid)

	del x_train, x_valid; gc.collect()

	print('Training ...')

	params = {}
	params['eta'] = 0.002
	params['objective'] = 'reg:linear'
	params['eval_metric'] = 'mae'
	params['max_depth'] = 10
	params['silent'] = 1

	watchlist = [(d_train, 'train'), (d_valid, 'valid')]
	clf = xgb.train(params, d_train, 10000, watchlist, early_stopping_rounds=100, verbose_eval=10)

	del d_train, d_valid

	clf.save_model('0001.model')
	# xgb.plot_importance(clf)
	# xgb.plot_tree(clf, num_trees=4)
	
	# clf1 = GradientBoostingClassifier(n_estimators=100, learning_rate=0.001, max_depth=4, random_state=0)
	# clf2 = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=0)
	# # del x_train, x_valid; gc.collect()
	# eclf = VotingClassifier(estimators=[('rf', clf2), ('gb', clf1)], voting='soft')
	# print('Training voting classifiers')

	# for clf, label in zip([clf1, clf2, eclf], ['Random Forest', 'Gradient Boosting', 'Ensemble']):
	# 	scores = cross_val_score(clf, x_train, y_train, cv=5, scoring='accuracy')
	# 	print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))



	# # test scores.............
	# GBscore = clf1.score(x_valid, y_valid)
	# RFscore = clf2.score(x_valid, y_valid)
	# ENscore = eclf.score(x_valid, y_valid)
	# print ("Score by Gradient Boosting Algo: {}".format(GBscore))
	# print ("Score by Random Forest Algo: {}".format(RFscore))
	# print ("Score by Ensembled Algo: {}".format(ENscore))

	return  1, 1, 1


# print('Building test set ...')

# sample['parcelid'] = sample['ParcelId']
# df_test = sample.merge(prop, on='parcelid', how='left')

# del prop; gc.collect()

# x_test = df_test[train_columns]
# for c in x_test.dtypes[x_test.dtypes == object].index.values:
#     x_test[c] = (x_test[c] == True)

# del df_test, sample; gc.collect()

# d_test = xgb.DMatrix(x_test)

# del x_test; gc.collect()

# print('Predicting on test ...')

# p_test = clf.predict(d_test)

# del d_test; gc.collect()

# sub = pd.read_csv('../input/sample_submission.csv')
# for c in sub.columns[sub.columns != 'ParcelId']:
#     sub[c] = p_test

# print('Writing csv ...')
# sub.to_csv('xgb_starter.csv', index=False, float_format='%.4f')