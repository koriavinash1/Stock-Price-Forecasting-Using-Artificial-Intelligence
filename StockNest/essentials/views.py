from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
import random
import copy
import datetime
import requests
import logging
from django.core.paginator import Paginator,EmptyPage
from rest_framework.views import exception_handler
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied

#context processor for configuring topnav variable in template
def randomString(length=20,method=1):
    if method:
        base_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    else:
        base_string = '0123456789'
    token = ''.join(random.choice(base_string) for i in range(length))
    return token

def getCurrentTime():
    return datetime.datetime.now()#timezone unaware

def errorResp(status_code=400,readable_error="",extra_data={}):
    err_dict = {'error':{'text':'','readable':readable_error}}
    msg = ''
    c = status_code
    if c == 401:
        msg = 'Unauthorized'
    elif c == 406 :
        msg = 'Data not acceptible'
    elif c == 409:
        msg = 'Conflicting data'
    elif c== 404:
        msg = 'Object not found'
    elif c == 403:
        msg = 'Forbidden'
    else :
        c = status_code
    err_dict['error']['text'] = msg
    for key in extra_data:
        err_dict[key] = extra_data[key]
    return JsonResponse(err_dict, status = c)

def customExceptionHandler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        return errorResp(response.status_code)
    return response

def checkCredentials(user,password):
    return check_password(password,user.password)

def getPassword(password):
    return make_password(password,salt=None,hasher='default')

def highlightIndex(inputArray,index):
    tmpArray = copy.deepcopy(inputArray) # important since 2d list
    for i in range(len(tmpArray)):
        if i == index:
            if len(tmpArray[i]) == 5:
                tmpArray[i][4] = 1
            else:
                tmpArray[i].append(1)
        else:
            if len(tmpArray[i]) == 5:
                tmpArray[i][4] = 0
            else:
                tmpArray[i].append(0)
    return tmpArray

def addOffsetToArray(inputArray,offset):
    tmpArray = copy.copy(inputArray)
    for element in tmpArray:
        element[1] += str(offset) + "/"
    return tmpArray

def verifyCaptcha(g_response):
    if len(g_response) < 10:#response is usually a huge string
        return False
    data = {'secret':'6LdMKBMUAAAAAKaNi-ov7TccrJNi2y-n8BOGfofT','response':g_response}
    r = requests.get('https://www.google.com/recaptcha/api/siteverify',params=data)
    if r.status_code == 200:
        responseDict = r.json()
        try:
            return responseDict['success']
        except KeyError:
            return False
    return False 