#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

def home(request):
    context = {}
    context['words'] =  'こどものうた - 高橋優'

    context['page_info'] = {}
    context['page_info']['title'] = '異議あり!'
    context['page_info']['toggle'] = 'home_page'

    return render(request, 'index.html', context)

