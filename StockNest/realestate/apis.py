from ML_model import mainNetwork
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import rproperty, rprediction 
import numpy as np
import os
from funcs import csv2json, logerror2price

@api_view(['POST'])
def trainRealestateModel(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	if 'update' not in inputDict:
		return errorResp(406)

	if not inputDict['update']:
		return Response({})

	GBScore, RFScore, ENScore = mainNetwork()
	print (GBScore, RFScore, ENScore)
	return  Response({})

@api_view(['PUT'])
def updateRealestateDB(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	if 'update' not in inputDict:
		return errorResp(406)

	if not inputDict['update']:
		return Response({})

	path = "/media/koriavinash/New Volume/Research/Deep Learning/hackerearth/StockNest_Dynamic/StockNest/realestate/dataset/modified.csv"
	data = csv2json(path)

	for info in data:
		try:
			_=rproperty.objects.get(pid=info['pid'])
		except:
			print ("[{}] updating restate DB: {}".format(os.getpid(), info))
			price = info['sqfeet'] * np.random.normal(200, 50, 1)
			_=rproperty.objects.create(pid=info['pid'], lat=info['lat'], log=info['log'], rid=info['rid'], sqfeet=info['sqfeet'], price=price)

	return Response({'status':True, 'text': 'History Updated'})

@api_view(['PUT'])
def updateRealestatePrediction(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	if 'update' not in inputDict:
		return errorResp(406)

	if not inputDict['update']:
		return Response({})

	path = "/media/koriavinash/New Volume/Research/Deep Learning/hackerearth/StockNest_Dynamic/StockNest/realestate/dataset/submissions.csv"

	for ppty in rproperty.objects.all():
		try:
			t=rprediction.objects.get(pid=ppt.pid)

		except:
			print ("[{}] updating restate DB: {}".format(os.getpid(), info))
			price = info['sqfeet'] * np.random.normal(200, 50, 1)
			_=rproperty.objects.create(pid=info['pid'], lat=info['lat'], log=info['log'], rid=info['rid'], sqfeet=info['sqfeet'], price=price)

	return Response({'status':True, 'text': 'History Updated'})