import xbmc, xbmcgui, os, xbmcaddon, xbmcplugin, requests,json

def main():
    __settings__ = xbmcaddon.Addon()
    home = __settings__.getAddonInfo('path')
    addon_handle = int(sys.argv[1])
    icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

    urlitem = 'http://api.m.afreecatv.com/broad/a/items2'

    reqlist = requests.get(urlitem).json()
    list = reqlist["data"]["groups"]
    for list1 in list:
        list2 = list1["contents"]
        for list3 in list2:

            br_no = list3["broad_no"]
            tit = list3["title"]
            thum = list3["thumbnail"]
            user = list3["user_id"]

            li = xbmcgui.ListItem(tit)
            li.setThumbnailImage(thum)        
        
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
            data = {'broad_no': br_no,
                    'parent_broad_no': '0', 
                    'origianl_broad_no': br_no,
                    'bj_id': user}
        
            url = 'http://api.m.afreecatv.com/broad/a/watch?bjid=y1026'
            response = requests.post(url=url, data=data, headers=headers).json()
            ticket = response["data"]["hls_authentication_key"]
        
            urllive = 'http://resourcemanager.afreecatv.com:9090/broad_stream_assign.html?return_type=gs_cdn_mobile_web&use_cors=true&cors_origin_url=m.afreecatv.com&broad_key={0}-mobileweb-hd-hls'.format(br_no)
            live = requests.get(urllive).json()
            view = live["view_url"]
        
            afreeca = view + '?aid=' + ticket
            
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=afreeca, listitem=li, isFolder=False)

        
    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == '__main__':
    main()
