import os
import ctypes
import logging
import time
from requests_html import HTMLSession

class WallpaperManager:
    def __init__(self, root_url='https://wallpaper-a-day.com'): 
        self.session = HTMLSession()
        self.root_url = root_url
        self.img_src = None
        self.filename = None
        
        self.constant_check = False
        
    def wallpaperCheckLoop(self):
        self.constant_check = True
        self.starting_time = time.time()
        self.last_check = 0
        self.total_auto_checks = 0
        
        while self.constant_check:
            if time.time() - self.last_check >= 600:
                self.huntSRC()
                self.saveWallpaper()
                self.setWallpaper()
                self.last_check = time.time()
                self.total_auto_checks += 1
                
    def getSaveSet(self, n=0):
        self.huntSRC(n)
        self.saveWallpaper()
        self.setWallpaper()

    def huntSRC(self, n=0):
        r = self.session.get(self.root_url)
        link = r.html.find('.post')[n].find('a')[0].attrs['href']
        r = self.session.get(link)
        if link.startswith('https://imgur.com'):
            self.img_src = r.html.find('.image-placeholder')[0].attrs['src']
        elif link.startswith('https://drive.google.com'):
            self.img_src = 'https://drive.google.com/uc?id=' + link.split('/')[5]
        else:
            self.img_src = link

    def saveWallpaper(self, src=None):
        if src is None:
            src = self.img_src

        if src.endswith(('png', 'jpg', 'jpeg')):
            ext = src.split('/')[-1].split('.')[-1]
            filename = f'latest_wallpaper.{ext}'
        else:
            filename = 'latest_wallpaper.png'

        response = self.session.get(src)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            logging.error(f'Failed to retrieve image. Status code: {response.status_code}')
            
        self.filename = filename

    def setWallpaper(self, path=None):
        path = path or self.filename
        if not os.path.isfile(path):
            logging.error(f'File not found: {path}')
            return
        abs_path = os.path.abspath(path)
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02

        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, abs_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)