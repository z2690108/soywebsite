# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render

def getSteamCard(request):
  if request.method == "GET":
    steam_id = request.GET['id']

    

  



  return render(request, 'index.html', context)
