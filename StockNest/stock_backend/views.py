# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.decorators import api_view
from essentials.views import errorResp
# Create your views here.

def stocksPage(request):
	return render(request, 'stock.html',{})

def stocksAdminPage(request):
	return render(request, 'stockadmin.html',{})
