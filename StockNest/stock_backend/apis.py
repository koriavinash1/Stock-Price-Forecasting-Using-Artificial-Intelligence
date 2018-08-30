from __future__ import division, print_function
import requests, json
requests.packages.urllib3.disable_warnings()
from nsepy import get_history
from nsetools import Nse
import MySQLdb as mysqldb
import pandas as pd
from StockNest.celery import app 
from models import company, stockData, companyTweets, predictionData,\
						companyNews
from constants import COMPANIES, epochs, batch_size, sequence_length
from datetime import date, timedelta
from essentials.views import errorResp
from rest_framework.response import Response
from rest_framework.decorators import api_view
from funcs import getTrainableFeatures, getOurSelection
from LSTM_model import trainNetwork, build_LSTMmodel, predictOutput, \
						getTweetDetails, getNewsDetails
import os
import numpy as np
from django.http import HttpResponseRedirect,JsonResponse,HttpRequest
from gold_prediction.models import GoldTweets, GoldNews, goldPrices

# startDate = date(1997, 1, 1)
# endDate = date(2010, 1, 1)
# startDate = date(2010, 1, 1)

startDate = date.today() - timedelta(50)
endDate = date.today()
COMP = ['EICHERMOT',  'BOSCHLTD', 'MARUTI', 'ULTRACEMCO', 'HEROMOTOCO',\
		 	'TATAMOTORS', 'BPCL', 'AXISBANK', 'TATASTEEL', 'ZEEL',\
				'CIPLA', 'TATAPOWER', 'BANKBARODA', 'NTPC', 'ONGC']
@api_view(['PUT'])
def updateDatabaseHistory(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	if 'update' not in inputDict:
		return errorResp(406)

	if not inputDict['update']:
		return Response({})

	if 'companies' not in inputDict: comp = COMPANIES
	else: comp = inputDict['companies']

	for symbol in comp:
		print("[{}] current company:  {}".format(os.getpid(), symbol))
		data = get_history(symbol = symbol,
					start = startDate,
					end = endDate)
		try:
			comp = company.objects.get(name = symbol)
		except:
			comp = company.objects.create(name = symbol)
		date = list(data.index)
		details = data.as_matrix()
		# compD: [Symbol, Series, Prev Close, Open, High, Low, Last, Close, VWAP, \
		#                       Volume, Turnover, Trades, Deliverable Volume, %Deliverble]
		for dt, compD in zip(date, details):
			comp.ltp = compD[5]
			comp.save()
			try:
				_=stockData.objects.get(companyDetails=comp,
								dateTime=dt)
			except:
				_=stockData.objects.create(companyDetails=comp,
								dateTime=dt,
								openPrice=compD[3],
								previousPrice=compD[2],
								lowPrice=compD[5],
								highPrice=compD[4],
								closePrice=compD[7],
								turnover=compD[10],
								volume=compD[9],
								series=compD[1])
	return Response({'status':True, 'text': 'History Updated'})

@api_view(['PUT'])
def updateDatabaseCurrent(requests):
	(user,inputDict,getParams) = (request.user,request.data,request.GET)
	if user.userType not in [3, 4]:
		return errorResp(401)
	
	if 'update' not in inputDict:
		return errorResp(406)
	
	if not inputDict['update']:
		return Response({})

	nse = Nse()
	for symbol in COMPANIES:
		data = nse.get_quote(symbol)

		try:
			comp = company.objects.get(name = symbol)
		except:
			comp = company.objects.create(name = symbol)

		try:
			_=stockData.objects.get(companyDetails=comp,
							dataTime=data['secDate'])
		except:
			_=stockData.objects.create(companyDetails=comp,
							dateTime=data['secDate'],
							openPrice=data['open'],
							previousPrice=data['previousClose'],
							lowPrice=data['dayLow'],
							highPrice=data['dayHigh'],
							closePrice=data['closePrice'],
							# ltp=data['lastPrice'],
							# trades=data['totalTradedValue'],
							# turnover=data[''],
							volume=data['totalTradedVolume'],
							series=data['series'])

	return Response({'status': True, 'text': "Today's stockdata updated successfully." })

@api_view(['PUT'])
def updateModelPredictions(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	# if user.userType not in [3, 4]:
	# 	return errorResp(401)
	
	if 'update' not in inputDict:
		return errorResp(406)
	
	if not inputDict['update']:
		return Response({})

	if 'seqlength' not in inputDict: seqlength = 30
	else: seqlength = inputDict['seqlength'] 

	if 'plength' not in inputDict: plength = 2
	else: plength = inputDict['plength']

	if 'gold' in inputDict: 	
		print(inputDict['gold'])
		if inputDict['gold']: COMPANIES = ["goldPrediction"]
		else: return Response({'status':True})


	for symbol in COMP:
		print("[{}] current company:  {}, seqlength: {}, plength: {}".format(os.getpid(), symbol, seqlength, plength))
		try:
			comp = company.objects.get(name = symbol)
		except:
			return errorResp(406, readable_error="Compny Doen't exist")

		if 'gold' in inputDict: 
			data = goldPrices.objects.all()
			eval_data = data[len(data) - seqlength: len(data)]
			evaluateX = getTrainableFeatures(eval_data, mode="eval", maxVal=data[0], mtype="gold", seqlength=seqlength, plength=plength)
		else:  
			data = stockData.objects.filter(companyDetails=comp)
			eval_data = data[len(data) - seqlength: len(data)]
			evaluateX = getTrainableFeatures(eval_data, mode="eval", maxVal=data[0], seqlength=seqlength, plength=plength)
		
		predictions = predictOutput(modelpath=comp.modelPath, data=evaluateX)
		# for i in 	range(plength):
		# 	print("hi")
		# 	temp = 0
		# 	if i == 0:
		# 		if predictions[0][i] < np.mean(evaluateX):
		# 			temp = predictions[0][i+1] - predictions[0][i] 
		# 			predictions[0][i] = np.mean(evaluateX) + np.random.normal(0, 0.01, 1)

		# 	else:
		# 		if predictions[0][i] < np.mean(evaluateX):
		# 			predictions[0][i] = predictions[0][i-1] + temp

		save_data = np.concatenate([evaluateX[0],predictions.T],0).reshape(seqlength+plength)
		dates = [str(d.dateTime)[0:10] for d in eval_data]
		dates += ['day +' +str(i+1) for i in range(plength)]
		try:
			pred=predictionData.objects.get(companyDetails=comp, dateTime=date.today())
		except:
			pred = predictionData.objects.create(companyDetails=comp, dateTime=date.today())
		if "gold" in inputDict: pdata = {"price": np.dot(save_data, data[0].price), 'label': dates}
		else: pdata = {'stocks':np.dot(save_data, data[0].closePrice), 'label': dates}
		pred.predictions = pdata
		pred.save()
	return Response({'status':True})

@api_view(['PUT'])
def trainModel(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	# if user.userType not in [3, 4]:
	# 	return errorResp(401)
	
	if 'update' not in inputDict:
		return errorResp(406)
	
	if not inputDict['update']:
		return Response({})

	if 'companies' not in inputDict: compList = COMPANIES
	else: compList = inputDict['companies']

	if 'plength' not in inputDict: plength = 2
	else: plength = inputDict['plength'] 

	if 'seqlength' not in inputDict: seqlength = 30
	else: seqlength = inputDict['seqlength'] 

	for symbol in compList:
		try:
			comp = company.objects.get(name=symbol)
		except:
			return errorResp(406,readable_error="Company Doesn't exist.")

		train_data = stockData.objects.filter(companyDetails=comp) 
		trainX, trainY, testX, testY = getTrainableFeatures(train_data, plength=plength, seqlength=seqlength, mode="train", maxVal = train_data[0])
		# print (trainX.shape, trainY.shape)
		# assert len(trainX) == len(trainY)
		model = build_LSTMmodel(seqlength, plength)
		model_info, test_mse, test_mae, test_acc, model, pred, tlabels = trainNetwork(trainData = trainX, 
									trainLabels = trainY, 
									testData = testX, 
									testLabels = testY, 
									model = model,
									company=symbol)

		path = "./modelData/final_"+symbol+".hdf5"
		model.save(path)
		comp.modelPath = path
		comp.graphData = {'predictions': pred, 'expected': tlabels}
		comp.modelInfo = model_info
		comp.testMSE = test_mse
		comp.testMAE = test_mae
		comp.testAccuracy = test_acc*100
		comp.save()
	return Response({'status':True, 'text':"Training Completed"})

@api_view(['PUT'])
def updateTweets(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	# if user.userType not in [3, 4]:
	# 	return errorResp(401)
	
	if 'update' not in inputDict:
		return errorResp(406)
	
	if not inputDict['update']:
		return Response({})

	if "gold" in inputDict:
		if inputDict['gold']:
			tweet_info, retweet_count, subjectivity, polarity = getTweetDetails(company="gold",
												date=date.today())
			for ti, tr, ts, tp in zip(tweet_info, retweet_count, subjectivity, polarity):
				GoldTweets.objects.create(tweetInfo=ti,
								retweets=tr,
								sentimentPolarity=tp,
								sentimentSubjectivity=ts)

	else:
		for symbol in COMPANIES:
			try:
				comp = company.objects.get(name=symbol)
			except:
				return errorResp(406,readable_error="Company Doesn't exist.")
			tweet_info, retweet_count, subjectivity, polarity = getTweetDetails(company=symbol,
													date=date.today())
			for ti, tr, ts, tp in zip(tweet_info, retweet_count, subjectivity, polarity):
				companyTweets.objects.create(companyDetails=comp,
									tweetInfo=ti,
									retweets=tr,
									sentimentPolarity=tp,
									sentimentSubjectivity=ts)

	return Response({'status':True, 'text':'Tweets updated'})

@api_view(['PUT'])
def updateNews(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	# if user.userType not in [3, 4]:
	# 	return errorResp(401)
	
	if 'update' not in inputDict:
		return errorResp(406)
	
	if not inputDict['update']:
		return Response({})

	if "gold" in inputDict:
		if inputDict['gold']:
			news_info, subjectivity, polarity = getNewsDetails(company="gold",
									date=date.today())
			try:
				comp = company.objects.get(name="goldPrediction")
			except:
				return errorResp(406, readable_error="Company Doesn't exist.")

			for ni, ns, np in zip(news_info, subjectivity, polarity):
				companyNews.objects.create(companyDetails=comp,
								news=ni,
								sentimentPolarity=np,
								sentimentSubjectivity=ns)
	else:
		for symbol in COMPANIES:
			try:
				comp = company.objects.get(name=symbol)
			except:
				return errorResp(406, readable_error="Company Doesn't exist.")
			news_info, subjectivity, polarity = getNewsDetails(company=symbol,
										date=date.today())
			for ni, ns, np in zip(news_info, subjectivity, polarity):
				companyNews.objects.create(companyDetails=comp,
								news=ni,
								sentimentPolarity=np,
								sentimentSubjectivity=ns)

	return Response({'status':True, 'text':'News updated'})

@api_view(['GET'])
def predict(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	# if user.userType not in [3, 4]:
	# 	return errorResp(401)
	
	if 'company' not in getParams: 
		# print("qwertyuiop[")
		return errorResp(406, readable_error="Get Param Not found.")

	cname = getParams['company']
	try:
		comp = company.objects.get(name=cname)
	except:
		# print("Adssadsdasd")
		return errorResp(406, readable_error="Company Doesn't exist.")
	try:
		pred = predictionData.objects.get(companyDetails=comp)
		return_data = {"predictions":pred.predictions}
		# print(return_data)
	except:
		# print("Asdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
		return errorResp(406, readable_error="Prediction Data Doesn't exist.")
	return JsonResponse(return_data)


@api_view(['GET'])
def compare(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	# if user.userType not in [3, 4]:
	# 	return errorResp(401)
	
	if 'company1' and 'company2' not in getParams: return errorResp(406)

	cname1, cname2 = getParams['company1'], getParams['company2']
	try:
		comp1 = company.objects.get(name=cname1)
	except:
		return errorResp(406, readable_error="Company Doesn't exist.")
	try:
		comp2 = company.objects.get(name=cname2)
	except:
		return errorResp(406, readable_error="Company Doesn't exist.")
	try:
		pred1 = predictionData.objects.get(companyDetails=comp1)
	except:
		return errorResp(406)
	try:
		pred2 = predictionData.objects.get(companyDetails=comp2)
	except:
		return errorResp(406)

	tweetComp1 = companyTweets.objects.filter(companyDetails = comp1)
	tweetComp2 = companyTweets.objects.filter(companyDetails = comp2)

	newsComp1 = companyTweets.objects.filter(companyDetails = comp1)
	newsComp2 = companyTweets.objects.filter(companyDetails = comp2)

	stock1 = stockData.objects.filter(companyDetails=comp1)
	stock2 = stockData.objects.filter(companyDetails=comp2)

	stock1 = stock1[len(stock1)-1]
	stock2 = stock2[len(stock2)-1]

	ourCompInfo = getOurSelection(pred1.predictions['stocks'], pred2.predictions['stocks'], tweetComp1, tweetComp2, newsComp1, newsComp2, comp1, comp2, stock1, stock2)

	return_data = {"predictions": {"company1": pred1.predictions['stocks'], "company2": pred2.predictions['stocks'], "labels": pred1.predictions['label']}, "tableInfo": ourCompInfo}

	return JsonResponse(return_data)

@api_view(['GET'])
def actualVspred(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	if 'company' not in getParams: return errorResp(406)
	cname = getParams['company']
	try:
		comp = company.objects.get(name=cname)
	except:
		return errorResp(406)
	# print(np.array(comp.graphData['predictions'])[-50:].shape, np.array(comp.graphData['expected'])[-50:].shape)
	return_data = { "graphData":{"expected": np.array(comp.graphData['expected'])[-300:].flatten().tolist(),"predictions": np.array(comp.graphData['predictions'])[-300:].flatten().tolist(), "labels": np.arange(len(np.array(comp.graphData['expected'])[-300:].flatten().tolist())).tolist()}, "mse": comp.testMSE, "mae": comp.testMAE}
	return JsonResponse(return_data)
	
@api_view(['GET'])
def getCompanyList(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	companyList = company.objects.all()
	return_data = []
	for comp in companyList:
		groupInfo = stockData.objects.filter(companyDetails=comp)
		try: 
			groupInfo = groupInfo[len(groupInfo) - 1]
			return_data.append({"name": comp.name, "debt":comp.debt, "turnoverbyvolume": float(groupInfo.turnover) / (groupInfo.volume*100000)})
		except: pass
	return JsonResponse({'company_data':return_data})