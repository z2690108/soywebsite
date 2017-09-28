#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

def home(request):
  context = {}
  context['words'] = 'Shirai Kuroko'
  context['bg_url'] = 'http://59.110.139.107:8080/images/109951162874623951.jpg'
  return render(request, 'index.html', context)

