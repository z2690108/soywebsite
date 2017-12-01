# -*- coding: utf-8 -*-

# ---------------------------------------------------------------
#
# check steam web API from: https://developer.valvesoftware.com
#
# ---------------------------------------------------------------

from __future__ import unicode_literals

import requests

class SteamCard:
    def __init__(self, steam_id):
        self.key = "CC65C7020A23B7096D1327D991D5080A"
        # self.steam_id = steam_id
        self.steam_id = '76561198096800938'

    def _getBasicInfo(self):
        try:
            param = {'key':self.key, 'steamids':self.steam_id}
            r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params = param)
            player = r.json()['response']['players']

            return player

        except Exception, e:
            print 'Get basic info from steam failed. steamid: ', self.steam_id, ' Exception: ', e
            return {}

    def _getOwnedGames(self, order_by_playtime_2weeks=True):
        try:
            param = {'key':self.key, 'steamid':self.steam_id, 'include_played_free_games':1, 'include_appinfo':1, 'format':'json'}
            r = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params = param)

            game_count = r.json()['response']['game_count']
            games = r.json()['response']['games']

            def w2cmp(g1, g2):
                ftime1 = g1['playtime_forever'] if 'playtime_forever' in g1 else 0
                ftime2 = g2['playtime_forever'] if 'playtime_forever' in g2 else 0

                wtime1 = g1['playtime_2weeks'] if 'playtime_2weeks' in g1 else 0
                wtime2 = g2['playtime_2weeks'] if 'playtime_2weeks' in g2 else 0

                return cmp(ftime1, ftime2) if cmp(wtime1, wtime2) == 0 else cmp(wtime1, wtime2)

            if order_by_playtime_2weeks:
                games = sorted(games, cmp=w2cmp, reverse=True)
            else:
                games = sorted(games, key=lambda g:g['playtime_forever'] if 'playtime_forever' in g else 0, reverse=True)

            for game in games:
                game['img_icon_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_icon_url'])
                game['img_logo_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_logo_url'])

                if game['has_community_visible_stats']:
                    game['stats_url'] = "http://steamcommunity.com/profiles/%s/stats/%d" % (self.steam_id, game['appid'])
                # if no stats page, return store page.
                else:
                    game['stats_url'] = "http://store.steampowered.com/app/%d" % (game['appid'],)
                
                game['store_url'] = "http://store.steampowered.com/app/%d" % (game['appid'],)

            return games

        except Exception, e:
            print 'Get owned games of ', self.steam_id, ' failed. Exception: ', e
            return {}

    def _getRecentlyGames(self):
        try:
            param = {'key':self.key, 'steamid':self.steam_id, 'count':30, 'format':'json'}
            r = requests.get('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/', params = param)

            total_count = r.json()['response']['total_count']
            games = r.json()['response']['games']

            games = sorted(games, key=lambda g:g['playtime_2weeks'] if 'playtime_2weeks' in g else 0, reverse=True)

            for game in games:
                game['img_icon_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_icon_url'])
                game['img_logo_url'] = "http://media.steampowered.com/steamcommunity/public/images/apps/%d/%s.jpg" % (game['appid'], game['img_logo_url'])

                game['stats_url'] = "http://steamcommunity.com/profiles/%s/stats/%d" % (self.steam_id, game['appid'])
                game['store_url'] = "http://store.steampowered.com/app/%d" % (game['appid'],)

            return games

        except Exception, e:
            print 'Get recently played games of ', self.steam_id, ' failed. Exception: ', e
            return {}

    def _getAchievement(self):
        try:
            param = {'key':self.key, 'steamids':self.steam_id}
            r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params = param)
            player = r.json()['response']['players']

        except Exception, e:
            print 'Get basic info from steam failed. Exception: ', e
            return {}
       

    def getSteamCard(self):
