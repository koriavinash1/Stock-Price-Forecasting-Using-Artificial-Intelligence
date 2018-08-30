from models import User
from essentials.views import errorResp
from rest_framework.response import Response
from rest_framework.decorators import api_view
from stock_backend.models import company, predictionData
from realestate.models import rproperty
from banking.models import bankInfoFD
import math

@api_view(['POST'])
def predictPath(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)
	for k in ['amt', 'period', 'risk']:
		if k not in inputDict: 
			return errorResp(406)

	percentage = {'property':0, 'banking':0, 'stocks':0, 'gold': 0}
	
	# TODO: proper study to set these equations using some optimization techniques
	theta1, theta2 = 0.5, 0.3
	k1, k2, k3, k4 = 0.25, 0.25, 0.25, 0.25

	percentage['property'] = k1*inputDict['risk']**theta1*inputDict['period']
	percentage['gold'] = k3*inputDict['period']/inputDict['risk']
	percentage['stocks'] = k2*inputDict['risk'] * inputDict['period']**theta2
	percentage['banking'] = k4*inputDict['period']

	#normalize percentages
	dr = percentage['property']+percentage['gold']+percentage['stocks']+percentage['banking']

	percentage['property'] = 100*percentage['property']//dr
	percentage['stocks'] = 100*percentage['stocks']//dr
	percentage['gold'] = 100*percentage['gold']//dr
	percentage['banking'] = 100*percentage['banking']//dr

	###
	stockamt = percentage['stocks']*inputDict['amt']/(100*10) # min 10 lots
	propamt = percentage['property']*inputDict['amt']/100

	companyList = company.objects.filter(ltp__lte =stockamt)
	bestbanks = bankInfoFD.objects.filter(interestRate__gte = 8.5)# think of it
	propertyList = rproperty.objects.filter(price__lte = propamt)

	### Insert Sorting methods
	complist = []
	for comp in companyList:
		try:
			data = predictionData.objects.get(companyDetails = comp).predictions['stocks']
			if (data[len(data)-2]) > int(data[len(data) - 3]) or (data[len(data)-1]) > int(data[len(data) - 3]):
				complist.append({'name': comp.name,'id':comp.id})
		except: pass
		
	### serialize
	blist = [{'name': bb.name, 'id': bb.id} for bb in bestbanks]
	plist = [{'name': ppt.pid, 'id':ppt.id} for ppt in propertyList]

	return Response({'percentagedistri':percentage, 'stockcompanies': complist, 'propertyList': plist, 'banks': blist})

@api_view(['GET'])
def getDetails(requests):
	(user,inputDict,getParams) = (requests.user,requests.data,requests.GET)

	if 'type' not in getParams:
		return errorResp(406)

	if 'name' not in getParams:
		return errorResp(406)

	if getParams['type'] == 'b': 
		try:
			bank = bankInfoFD.objects.get(id = getParams['name'])
			rinfo = {'name': bank.name, 'group': bank.group, 'period': bank.period, 'taxStatus': bank.taxStatus, 'interestRate': bank.interestRate}
		except:
			return errorResp(406)
	elif getParams['type'] == 's':
		try:
			comp = company.objects.get(id = getParams['name'])
			rinfo = {'name': comp.name, 'last closing price': comp.ltp, 'prediction variance': comp.testMSE}
		except:
			return errorResp(406)
	elif getParams['type'] == 'p':
		try:
			ppty = rproperty.objects.get(id = getParams['name'])
			rinfo = {'pid': ppty.pid, 'LatLng': {'lat': ppty.lat, 'lng': ppty.log}, 'area(insqfeet)': ppty.sqfeet, 'price': ppty.price}
		except:
			return errorResp(406)
	return Response(rinfo)