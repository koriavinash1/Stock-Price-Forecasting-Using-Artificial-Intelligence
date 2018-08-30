import pandas as pd
import numpy as np
import math
import os

from constants import batch_size, sequence_length, prediction_length, IS_FIRST_RUN

path2gainers = "./csv-data/gainers"
path2loosers = "./csv-data/loosers"

max_values = {}

if not os.path.exists(path2loosers) or not os.path.exists(path2gainers):
    print "Given directories does not exist"

# { 0: Date,	1:Open, 	2:High,	 3:Low, 	4:Close, 	5:Adj Close,	6:Volume}

def extract_csv2object(path, file_name):
	"""
	using pandas framework for extracting data from file to pandas object
	"""
	return pd.read_csv(path + "/" + file_name + ".NS.csv")

def data_normalization(data, company):
	"""
	normalization technique followed: data.Object/ data.Object[0] -1
	max_values json array for all max values used in denormalizing the data
	"""	
	data.drop(data.columns[[5, 6, 2, 4, 3]], axis=1, inplace=True)
	# max_values = {'Open': data[1].astype("float")[0],\
	# 			  'Close': data[4].astype("float")[0],\
	# 			  'Low': data[3].astype("float")[0],\
	# 			  'High': data[2].astype("float")[0]}
	max_values = {'Close': data[1].astype("float")[0]}

	if IS_FIRST_RUN:
		file = open("max_vals.py", "a")
		file.write(company + "_NORM_VAL = " + str(data[1].astype("float")[0]))
		file.write("\n")
		file.write(company + "_MAX_VAL = " + str(max(data[1].astype("float"))))
		file.write("\n")
		file.close()
		jsfile = open("../graphdata/max_vals.js", "a")
		jsfile.write("val " + company + "_NORM_VAL = " + str(data[1].astype("float")[0]))
		jsfile.write("\n")
		jsfile.write("val " + company + "_MAX_VAL = " + str(max(data[1].astype("float"))))
		jsfile.write("\n")
		jsfile.close()
	data[1] = data[1].astype("float") / data[1].astype("float")[0] - 1
	# data[4] = data[4].astype("float") / data[4].astype("float")[0] - 1
	# data[3] = data[3].astype("float") / data[3].astype("float")[0] - 1
	# data[2] = data[2].astype("float") / data[2].astype("float")[0] - 1
	return data, max_values

def pdobject2array(objects):
	"""
	This function helps in converting pandas object to numpy array
	"""
	return objects.values

def remove_emptyblock(pdobject):
	"""
	This helps in removing 'null' blocks from the data and also helps in arranging the data
	"""
	array = pdobject.values
	return pd.DataFrame(np.delete(array, np.where(array == 'null')[0].tolist(), 0))

def construct_seq_data(array, sequence_length, prediction_length):
    """
    convert an array to sequencial data for feeding to lstm cell
    one month data as one sequence
    """
    sequence_length = sequence_length + prediction_length
    return_data = np.array([ array[i: i+sequence_length] for i in range(array.shape[0]  - sequence_length)], ndmin=3)
    return return_data

def split_database(array):
	"""
	splits the data into train validation and test data for model training
	"""
	train_data = array[:int(math.floor(len(array) * 0.9))]
	# validation_data = array[int(math.floor(len(array) * 0.7)):int(math.floor(len(array) * 0.9))]
	test_data = array[int(math.floor(len(array) * 0.9)):]
	return (train_data[:, : -1*prediction_length], \
			train_data[:, -1*prediction_length:]),\
			(test_data[:, : -1*prediction_length],\
			test_data[:, -1*prediction_length:])

def data_denormalization(pred, company):
	import max_vals
	maxval = 0
	if company == "VEDL":
		maxval = max_vals.VEDL_NORM_VAL
	elif company == "BPCL":
		maxval = max_vals.BPCL_NORM_VAL
	elif company == "RELIANCE":
		maxval = max_vals.RELIANCE_NORM_VAL
	elif company == "HINDALCO":
		maxval = max_vals.HINDALCO_NORM_VAL
	elif company == "YESBANK":
		maxval = max_vals.YESBANK_NORM_VAL
	"""
	needs the data in json format for open, high, low, close
	return json data same as input format
	"""
	return (np.array(pred) + 1)*maxval

	# (np.array(labels) + 1)*maxval

class DataSet(object):
	def __init__(self, data, labels):
		self._labels = labels
		self._data = data
		self._epochs_completed = 0
		self._index_in_epoch = 0

	@property
	def data(self):
		return self._data

	@property
	def labels(self):
		return self._labels

	@property
	def epochs_completed(self):
		return self._epochs_completed

	def next_batch(self):
		"""
		Technically entire data is one single time series
		data but for computational convenience
		we take one month data as one time sequence

		shuffling the data doesn't make sense
		think of it....
		"""
		if self._index_in_epoch > self._data.shape[0] - batch_size:
			self._epochs_completed += 1
			self._index_in_epoch = 0
			# np.random.shuffle(self._data)
		
		start = self._index_in_epoch
		self._index_in_epoch += batch_size
		end = self._index_in_epoch
		# np.random.shuffle(self._data[start:end])
		return (np.reshape(self._data[start: end], (batch_size, sequence_length, 2)), self._labels[start: end])

def load_data(company="VEDL", company_type = 'g'):
	"""
	Default company is VEDL
	Default type is gainers
	"""
	class DataSets(object):
		pass
	data_sets = DataSets()
	path = path2gainers

	if company_type == 'l':
		path = path2loosers

	global max_values

	data = extract_csv2object(path, company)
	rdata = remove_emptyblock(data)
	ndata, max_values = data_normalization(rdata, company)
	adata = pdobject2array(ndata)
	sdata = construct_seq_data(adata, sequence_length, prediction_length)
	(train_data, train_labels), (test_data, test_labels) = split_database(sdata)
	# (train_data, train_labels), test_data = split_database(sdata)
	# test_labels = []
	print "Data extraction completed successfully!!"
	data_sets.train = DataSet(train_data, train_labels)
	data_sets.test = DataSet(test_data, test_labels)
	return data_sets