import xbmc, xbmcgui, os, xbmcaddon, xbmcplugin, requests,json

def main():
    __settings__ = xbmcaddon.Addon()
    home = __settings__.getAddonInfo('path')
    addon_handle = int(sys.argv[1])
    icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

    url = 'http://api.m.afreecatv.com/broad/a/items2'

    req = requests.get(url=url).json()
    real = req["data"]["groups"]

    for contents in real:
        list = contents["contents"]

        for a in list:
            id = a["user_id"]
            tit = a["title"]
            no = a["broad_no"]
            thn = a["thumbnail"]

            li = xbmcgui.ListItem(tit)
            li.setThumbnailImage(thn)

            url2 = "http://webtool.cusis.net/wp-pages/download-afreecatv-video/video-live.php"
            rell = 'https://player.afreecatv.com/{0}/{1}'.format(id, no)

            data = {'inputUrl': rell,
                    }

            req = requests.post(url2, data=json.dumps(data)).json()
            live = req["file"]
            for a in live:
                b = a.split(';')
                livelist = b[5]

            
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=livelist, listitem=li, isFolder=False)

        
    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == '__main__':
    main()
