# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.

def indexPage(request):
    return render(request, 'index.html',{})

def loginPage(request):
    return render(request, 'login.html',{})