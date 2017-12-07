# -*- coding: utf-8 -*-

# ---------------------------------------------------------------
#
# check steam web API from: https://developer.valvesoftware.com
#
# ---------------------------------------------------------------

from __future__ import unicode_literals

from lxml import html
import requests

from .steam_url_tools import SteamUrlTools
from .models import SteamKey

class SteamApi:
    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.key = SteamKey.objects.get(admin_id = 1).api_key

        self.profiles_url = SteamUrlTools.getProfileUrl(self.steam_id,)

    '''
        return:
            info: basic information of steam account.
                steam_id: steam id.
                persona_name: name of steam.
                avatar: the URL of avator.
                avatar_m: the URL of mediume size avator.
                avatar_f: the URL of full size avator.
                visibility_state: whether the profile is visible or not. 1 - Private, 3 - Public.
    '''

    def getBasicInfo(self):
        try:
            param = {'key':self.key, 'steamids':self.steam_id}
            r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params = param)
            players = r.json()['response']['players']
            player = players[0] if len(players) else {}

            info = {}
            if player:
                info['steam_id']            = player['steamid'] if 'steamid' in player else None
                info['persona_name']        = player['personaname'] if 'personaname' in player else None
                info['avatar']              = player['avatar'] if 'avatar' in player else None
                info['avatar_m']            = player['avatarmedium'] if 'avatarmedium' in player else None
                info['avatar_f']            = player['avatarfull'] if 'avatarfull' in player else None
                info['visibility_state']    = player['communityvisibilitystate'] if 'communityvisibilitystate' in player else None
            
            return info

        except Exception, e:
            print 'Get basic info from steam failed. steamid: ', self.steam_id, ' Exception: ', e
            return {}

    '''
        return:
            info: profile information of steam account.
                level: steam level.
                desc: profile summary.
                badges_count: the total amount of badges.
                badges_link_total: the URL of badges page of user.
                badges: a list of badge.
                    badge: badge info.
                        desc: description of badge.
                        link: the URL of badge's page.
                        img: the URL of badge image's page.
    '''

    def getProfileInfo(self):
        try:
            r = requests.get(self.profiles_url)
            tree = html.fromstring(r.text)

            level               = tree.xpath('//div[@class="profile_header_badgeinfo_badge_area"]//span[@class="friendPlayerLevelNum"]/text()')
            desc                = tree.xpath('//div[@class="profile_summary"]/text()')
            desc_noexpand       = tree.xpath('//div[@class="profile_summary noexpand"]/text()')
            badges_count        = tree.xpath('//div[@class="profile_badges"]//span[@class="profile_count_link_total"]/text()')
            badges_link_total   = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_count_link ellipsis"]//@href')
            badges_desc_list    = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_badges_badge "]/@data-community-tooltip')
            badges_link_list    = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_badges_badge "]//@href')
            badges_img_list     = tree.xpath('//div[@class="profile_badges"]//div[@class="profile_badges_badge "]//img/@src')

            info = {}
            info['level'] = level[0] if len(level) else None

            def getFrameLevel(level_str):
                if level_str and level_str.isdigit():
                    level = int(level_str)
                    return min(level / 10 * 10 if level < 100 else level / 100 * 100, 3000) if level > 0 else 0
                else:
                    return 0

            info['frame_level'] = getFrameLevel(info['level'])
            info['desc']  = desc[0].strip() if len(desc) else (desc_noexpand[0].strip() if len(desc_noexpand) else None)
            info['badges_count'] = badges_count[0].strip() if len(badges_count) else None
            info['badges_link_total'] = badges_link_total[0] if len(badges_link_total) else None

            info['badges'] = []
            badge = {}
            for i in xrange(len(badges_desc_list)):
                badge['desc'] = badges_desc_list[i] if i < len(badges_desc_list) else None
                badge['link'] = badges_link_list[i] if i < len(badges_link_list) else None
                badge['img']  = badges_img_list[i] if i < len(badges_img_list) else None
                info['badges'].append(badge)

            return info

        except Exception, e:
            print 'Get profile info from steam failed. steamid: ', self.steam_id, ' Exception: ', e
            return {}

    def getOwnedGames(self, order_by_playtime_2weeks=True):
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

    def getRecentlyGames(self):
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
