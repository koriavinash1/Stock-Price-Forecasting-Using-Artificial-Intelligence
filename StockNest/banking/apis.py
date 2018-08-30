from models import bankInfoFD
from funcs import csv2json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect,JsonResponse,HttpRequest
import os

path = "/media/koriavinash/New Volume/Research/Deep Learning/hackerearth/StockNest_Dynamic/StockNest/banking/dataset/Bank_interests - Sheet1.csv"

@api_view(['PUT'])
def updateBankDB(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	if 'update' not in inputDict:
		return errorResp(406)

	if not inputDict['update']:
		return Response({})

	data, headers = csv2json(path)
	##['INSTITUTION', 'GROUP', 'INTEREST % p.a', 'PERIOD', 'INVESTMENT (Rs)', 'INVESTOR TYPE', 'TAX STATUS']
	
	for info in data:
		try:
			_ =bankInfoFD.objects.get(name=info[headers[0]], period=info[headers[3]])
		except:
			print ("[{}] updating gold info: {}".format(os.getpid(), info))
			_=bankInfoFD.objects.create(name=info[headers[0]],
							group=info[headers[1]],
							interestRate = info[headers[2]],
							period=info[headers[3]],
							investmentCap=info[headers[4]],
							investorType=info[headers[5]],
							taxStatus=info[headers[6]])
	return Response({'status':True, 'text': 'History Updated'})