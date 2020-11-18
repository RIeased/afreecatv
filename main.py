import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
import json
import os
from urllib import urlencode
from urlparse import parse_qsl

_url = sys.argv[0]
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def list_categories():

    xbmcplugin.setPluginCategory(_handle, 'Afreeca TV')
    xbmcplugin.setContent(_handle, 'videos')
    
    list_item = xbmcgui.ListItem(label='Live')
    url = get_url(action='listing', category='Live')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def get_videos(category):

    urlitem = 'http://api.m.afreecatv.com/broad/a/items2'

    Live_lists = []
    reqlist = requests.get(urlitem).json()
    list = reqlist["data"]["groups"]
    for list1 in list:
        list2 = list1["contents"]
        for list3 in list2:
            
            Live_list = dict()
            Live_list['br_no'] = list3["broad_no"]
            Live_list['tit'] = list3["title"]
            Live_list['thumb'] = list3["thumbnail"]
            Live_list['user'] = list3["user_id"]        
        
            headers = {'User-Agent': 'kr.co.nowcom.mobile.afreeca/5.14.0 (Android 9) Afreeca API/5.14.0'}
            data = {'broad_no': Live_list['br_no'],
                    'parent_broad_no': '0', 
                    'origianl_broad_no': Live_list['br_no'],
                    'bj_id': Live_list['user']}
        
            url = 'http://api.m.afreecatv.com/broad/a/watch'
            response = requests.post(url=url, data=data, headers=headers).json()
            ticket = response["data"]["hls_authentication_key"]
        
            urllive = 'http://resourcemanager.afreecatv.com:9090/broad_stream_assign.html?return_type=gs_cdn&use_cors=true&cors_origin_url=m.afreecatv.com&broad_key={0}-common-original-hls'.format(Live_list['br_no'])
            live = requests.get(urllive).json()
            view = live["view_url"]
        
            Live_list['video'] = view + '?aid=' + ticket
            Live_lists.append(Live_list)

    return Live_lists




def list_videos(category):

    xbmcplugin.setPluginCategory(_handle, 'Live')
    xbmcplugin.setContent(_handle, 'videos')

    videos = get_videos(category)
    for video in videos:    
        list_item = xbmcgui.ListItem(label=video['tit'])
        list_item.setInfo('video', {'title': video['tit'],
                                    'mediatype': 'video'})

        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=video['video'])
        is_folder = False
        
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)





def router(paramstring):

    params = dict(parse_qsl(paramstring))

    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])

        elif params['action'] == 'play':
            play_video(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:

        list_categories()


if __name__ == '__main__':

    router(sys.argv[2][1:])