# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render
from .steam_card import SteamCard

def getSteamCard(request):
  context = {}
  if request.method == "GET":
    steam_id = request.GET['id']

    m_card = SteamCard(steam_id)
    context['info'] = m_card.getSteamCard()

  return render(request, 'steamCard/base.html', context)
