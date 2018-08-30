import tensorflow as tf
import numpy as np

def defineVariables(shape, name): 
    initializer = tf.contrib.layers.variance_scaling_initializer()
    return tf.get_variable(name, shape, initializer=initializer, dtype=tf.float32)

def preActivation(x, w, b):
    return tf.add(tf.matmul(x, w), b)

def activation(x):
    return tf.nn.sigmoid(x)

def save(list2save, directory):
	np.save(directory, list2save)
	pass

def dataNormalization(data, maxVal):
	return np.divide(data, maxVal)

def dataDenormalization():
	pass

def construct_seq_data(array, sequence_length, prediction_length):
    """
    convert an array to sequencial data for feeding to lstm cell
    one month data as one sequence
    """
    sequence_length = sequence_length + prediction_length
    return_data = np.array([ array[i: i+sequence_length] for i in range(len(array) - sequence_length + 1)], ndmin=3)
    return return_data.T.swapaxes(0,1)

def split_database(seq_data, prediction_length):
	"""
	splits the data into feature and label
	"""
	return (seq_data[:, : -1*prediction_length], \
			seq_data[:, -1*prediction_length:])

def  getTrainableFeatures(data, maxVal, plength=2, seqlength=10, mode="train", mtype="stock"):
	# mainFeatures: closePrice
	# prediction length = plength, used to format data accordingly for training
	if mode == "train":
		if mtype=="stock":
			data = [d.closePrice for d in data]
			maxVal = maxVal.closePrice
		elif mtype == "gold":
			data = [d.price for d in data]
			maxVal = maxVal.price
		data = dataNormalization(data, maxVal)

		train_data = data[500:]
		test_data = data[:500]
		seq_data = construct_seq_data(train_data, seqlength, plength)
		trainX, trainY = split_database(seq_data, plength)

		seq_data = construct_seq_data(test_data, seqlength, plength)
		testX, testY = split_database(seq_data, plength)
		return trainX, trainY.T.swapaxes(1,2)[0], testX, testY.T.swapaxes(1,2)[0]
	elif mode == "eval":
		print seqlength, plength
		if mtype=="stock":
			data = [d.closePrice for d in data]
			maxVal = maxVal.closePrice
		elif mtype == "gold":
			data = [d.price for d in data]
			maxVal = maxVal.price
		data = dataNormalization(data, maxVal)
		seq_data = construct_seq_data(data, seqlength, 0)
		print(seq_data)
		return seq_data
	pass

def getOurSelection(pred1, pred2, 
			tcomp1, tcomp2, 
			ncomp1, ncomp2, 
			comp1, comp2, 
			compStock1, compStock2,
			seqlength=10, plength=2):
	#TODO: to set Dynamic seqlength and prediction length
	#    to find optimal weight distribution
	# 
	# current:-----
	# MainSlp: 50%, Volatility: 20%, Tweets: 15%, News: 15%

	weights = {'mainSlp': 0.25, 'turnOver/volume': 0.1, 'debt': 0.1, 'volSlp': 0.2, 'tweets': 0.05, 'news': 0.05}

	print (pred1)

	pred1Slp = [pred1[i+1] - pred1[i] for i in range(len(pred1) -1)]
	pred2Slp = [pred2[i+1] - pred2[i] for i in range(len(pred2) -1)]

	# predicted slps
	Slp1 = sum(pred1Slp)
	Slp2 = sum(pred2Slp)
	
	# predicted slps
	mainSlp1 = sum([pred1Slp[len(pred1Slp)-i-1]  for i in range(plength)])
	mainSlp2 = sum([pred2Slp[len(pred2Slp)-i-1] for i in range(plength)])

	# main tweets company one
	tcomp1Sub = np.array([d.sentimentSubjectivity for d in tcomp1])
	tcomp1Pol = np.array([d.sentimentPolarity for d in tcomp1] )
	tcomp1measure = np.dot(tcomp1Sub, tcomp1Pol)

	# main tweets company two
	tcomp2Sub = np.array([d.sentimentSubjectivity for d in tcomp2])
	tcomp2Pol = np.array([d.sentimentPolarity for d in tcomp2]) 
	tcomp2measure = np.dot(tcomp2Sub, tcomp2Pol)

	# main tweets company one
	ncomp1Sub = np.array([d.sentimentSubjectivity for d in ncomp1])
	ncomp1Pol = np.array([d.sentimentPolarity for d in ncomp1] )
	ncomp1measure = np.dot(ncomp1Sub, ncomp1Pol)

	# main tweets company two
	ncomp2Sub = np.array([d.sentimentSubjectivity for d in ncomp2])
	ncomp2Pol = np.array([d.sentimentPolarity for d in ncomp2]) 
	ncomp2measure = np.dot(ncomp2Sub, ncomp2Pol)

	netmeasureComp1 = Slp1*weights['volSlp']  + mainSlp1*weights['mainSlp'] / (comp1.testMAE+comp1.testMSE) +\
				float(compStock1.turnover)/compStock1.volume*weights['turnOver/volume'] +\
				tcomp1measure*weights['tweets'] + ncomp1measure*weights['news'] + comp1.debt*weights['debt']
	netmeasureComp2 = Slp2*weights['volSlp']  + mainSlp2*weights['mainSlp'] / (comp2.testMAE+comp2.testMSE)+ \
				float(compStock2.turnover)/compStock1.volume*weights['turnOver/volume'] +\
				tcomp2measure*weights['tweets'] + ncomp2measure*weights['news'] + comp2.debt*weights['debt']

	if netmeasureComp1 >netmeasureComp2: 
		return {'comp1':{'volIndex': Slp1, 'marketSent': tcomp1measure+ncomp1measure, 'turnover': float(compStock1.turnover), 'volume':compStock1.volume, 'mainMeasure': netmeasureComp1}, 'comp2':{'volIndex': Slp2, 'marketSent': tcomp2measure+ncomp2measure, 'turnover': float(compStock2.turnover), 'volume':compStock2.volume, 'mainMeasure': netmeasureComp2}, 'ourSuggestion':comp1.name}
	elif netmeasureComp1< netmeasureComp2: 
		return {'comp1':{'volIndex': Slp1, 'marketSent': tcomp1measure+ncomp1measure, 'turnover': float(compStock1.turnover), 'volume':compStock1.volume, 'mainMeasure': netmeasureComp1}, 'comp2':{'volIndex': Slp2, 'marketSent': tcomp2measure+ncomp2measure, 'turnover': float(compStock2.turnover), 'volume':compStock2.volume, 'mainMeasure': netmeasureComp2}, 'ourSuggestion':comp2.name}
