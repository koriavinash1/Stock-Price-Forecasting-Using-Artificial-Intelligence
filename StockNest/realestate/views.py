# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def aboutModelRealestate(requests):
	pass

def predictRealestate(requests):
	pass

def compareRealestate(requests):
	pass

def hypothesisRealestate(requests):
	pass

def newsRealestate(requests):
	pass

def realestatePage(requests):
	return render(requests, 'realestate.html',{})