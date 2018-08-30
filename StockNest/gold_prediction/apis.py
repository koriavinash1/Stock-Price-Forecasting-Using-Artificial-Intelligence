from models import goldPrices, GoldTweets, GoldNews
from funcs import csv2json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect,JsonResponse,HttpRequest
from stock_backend.funcs import getTrainableFeatures
from stock_backend.LSTM_model import trainNetwork, build_LSTMmodel, predictOutput, \
						getTweetDetails, getNewsDetails
from stock_backend.models import company
import os

@api_view(['PUT'])
def updateGoldDB(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	if 'update' not in inputDict:
		return errorResp(406)

	if not inputDict['update']:
		return Response({})

	path = "/media/koriavinash/New Volume/Research/Deep Learning/hackerearth/StockNest_Dynamic/StockNest/gold_prediction/dataset/goldPrices.csv"
	data = csv2json(path)

	for info in data:
		try:
			_=goldPrices.objects.get(date=info['date'])
		except:
			print ("[{}] updating gold info: {}".format(os.getpid(), info))
			_=goldPrices.objects.create(date=info['date'], price=info['INR/gms'])

	return Response({'status':True, 'text': 'History Updated'})

@api_view(['PUT'])
def trainGoldModel(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	# if user.userType not in [3, 4]:
	# 	return errorResp(401)
	
	if 'update' not in inputDict:
		return errorResp(406)
	
	if not inputDict['update']:
		return Response({})

	if 'plength' not in inputDict: plength = 2
	else: plength = inputDict['plength'] 

	if 'seqlength' not in inputDict: seqlength = 10
	else: seqlength = inputDict['seqlength'] 

	symbol = "goldPrediction"

	try:
		comp = company.objects.get(name=symbol)
	except:
		comp = company.objects.create(name=symbol)

	train_data = goldPrices.objects.all()
	trainX, trainY, testX, testY = getTrainableFeatures(train_data, plength=plength, seqlength=seqlength, mode="train", maxVal = train_data[0], mtype="gold")
	# print (trainX.shape, trainY.shape)
	# assert len(trainX) == len(trainY)
	model = build_LSTMmodel(seqlength, plength)
	model_info, test_mse, test_mae, test_acc, model, pred, tlabels = trainNetwork(trainData = trainX, 
								trainLabels = trainY, 
								testData = testX, 
								testLabels = testY, 
								model = model,
								company=symbol)

	path = "./modelData/final_"+symbol+str(test_acc)+".hdf5"
	model.save(path)
	comp.modelPath = path
	comp.graphData = {'predictions': pred, 'expected': tlabels}
	comp.modelInfo = model_info
	comp.testMSE = test_mse
	comp.testMAE = test_mae
	comp.testAccuracy = test_acc*100
	comp.save()
	return Response({'status':True, 'text':"Training Completed"})