# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render
from .steam_card import SteamCard

def getSteamCard(request):
  context = {}
  if request.method == "GET":
    steam_id = request.GET['id']
    language = request.GET['lang'] if 'lang' in request.GET else 'en'

    m_card = SteamCard(steam_id, language)
    context['info'] = m_card.getSteamCard()

    print "card info: "
    print context['info']

  return render(request, 'steamCard/base.html', context)
