import sys
import xbmcgui
import xbmcplugin
import requests
import json
import urlparse
import urllib
import xbmc

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'videos')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def live_videos():

    urlitem = 'http://api.m.afreecatv.com/broad/a/items2'

    Lives = []
    reqlist = requests.get(urlitem).json()
    list = reqlist["data"]["groups"]
    for list1 in list:
        list2 = list1["contents"]
        for list3 in list2:
            
            Live = dict()
            Live['br_no'] = list3["broad_no"]
            Live['title'] = list3["title"]
            Live['thumb'] = list3["thumbnail"]
            Live['user'] = list3["user_id"]        
        
            headers = {'User-Agent': 'kr.co.nowcom.mobile.afreeca/5.14.0 (Android 9) Afreeca API/5.14.0'}
            data = {'broad_no': Live['br_no'],
                    'parent_broad_no': '0', 
                    'origianl_broad_no': Live['br_no'],
                    'bj_id': Live['user']}
        
            url = 'http://api.m.afreecatv.com/broad/a/watch'
            response = requests.post(url=url, data=data, headers=headers).json()
            ticket = response["data"]["hls_authentication_key"]
        
            urllive = 'http://resourcemanager.afreecatv.com:9090/broad_stream_assign.html?return_type=gs_cdn&use_cors=true&cors_origin_url=m.afreecatv.com&broad_key={0}-common-original-hls'.format(Live['br_no'])
            live = requests.get(urllive).json()
            view = live["view_url"]
        
            Live['play'] = view + '?aid=' + ticket
            
            li = xbmcgui.ListItem(Live["title"], iconImage=Live["thumb"])
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=Live["play"], listitem=li, isFolder=False)
            Lives.append(Live)
        
    return Lives

def Search_videos():
    
    kb = xbmc.Keyboard('default', 'heading', True)
    kb.setDefault('') # optional
    kb.setHeading('Search') # optional
    kb.setHiddenInput(False) # optional
    kb.doModal()
    if kb.isConfirmed():

        Search = kb.getText()

        urlsrh = 'http://sch.afreecatv.com/api.php'
        data = {'v': '1.0',
            'm': 'liveSearch',
            'w': 'webm',
            'isMobile': '1',
            'szKeyword': Search,
            'szOrder': 'accur',
            'nListCnt': '6',
            'nPageNo': '1'}

        req = requests.post(url=urlsrh, data=data).json()
        search = req["data"]["groups"]
        for s in search:
            e = s["contents"]

            try:
                for searchls in e:

                    br_no = searchls["broad_no"]
                    title = searchls["title"]
                    thumb = searchls["thumbnail"]
                    user = searchls["user_id"]        
        
                    headers = {'User-Agent': 'kr.co.nowcom.mobile.afreeca/5.14.0 (Android 9) Afreeca API/5.14.0'}
                    data = {'broad_no': br_no,
                            'parent_broad_no': '0', 
                            'origianl_broad_no': br_no,
                            'bj_id': user}
        
                    url = 'http://api.m.afreecatv.com/broad/a/watch'
                    response = requests.post(url=url, data=data, headers=headers).json()
                    ticket = response["data"]["hls_authentication_key"]
        
                    urllive = 'http://resourcemanager.afreecatv.com:9090/broad_stream_assign.html?return_type=gs_cdn&use_cors=true&cors_origin_url=m.afreecatv.com&broad_key={0}-common-original-hls'.format(br_no)
                    live = requests.get(urllive).json()
                    view = live["view_url"]
        
                    play = view + '?aid=' + ticket
                
                    li = xbmcgui.ListItem(title, iconImage=thumb)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=play, listitem=li, isFolder=False)
    
            except ValueError:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Kodi', 'There was an error.')
                if mode is None:
                    url = build_url({'mode': 'SEARCH', 'foldername': 'SEARCH'})
                    li = xbmcgui.ListItem('SEARCH', iconImage='DefaultFolder.png')
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                            listitem=li, isFolder=True)

                    url = build_url({'mode': 'LIVE', 'foldername': 'LIVE'})
                    li = xbmcgui.ListItem('LIVE', iconImage='DefaultFolder.png')
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                            listitem=li, isFolder=True)
    
                    xbmcplugin.endOfDirectory(addon_handle)
        





mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'SEARCH', 'foldername': 'SEARCH'})
    li = xbmcgui.ListItem('SEARCH', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'LIVE_top20', 'foldername': 'LIVE_top20'})
    li = xbmcgui.ListItem('LIVE_top20', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'SEARCH':
    foldername = args['foldername'][0]
    Search_videos()
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'LIVE_top20':
    foldername = args['foldername'][0]
    live_videos()
    xbmcplugin.endOfDirectory(addon_handle)
