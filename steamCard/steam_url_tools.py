# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

class SteamUrlTools:
    @classmethod
    def getProfileUrl(steam_id):
        return "http://steamcommunity.com/profiles/%s" % (steam_id,)

    @classmethod
    def getStatUrl(steam_id, app_id):
        return "http://steamcommunity.com/profiles/%s/stats/%d" % (steam_id, app_id)

    @classmethod
    def getStoreUrl(app_id):
        return "http://store.steampowered.com/app/%d" % (app_id)

    @classmethod
    def getAppImgUrl(app_id, img_url):
        return "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (app_id, img_url)

    @classmethod
    def getAppLogoUrl(app_id, logo_url):
        return "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (app_id, logo_url)