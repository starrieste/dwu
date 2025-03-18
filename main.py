import os
import sys
import time
import ctypes
import logging
import threading
from requests_html import HTMLSession

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')

class DailyWallpaper:
    def __init__(self, root_url='https://wallpaper-a-day.com'): 
        self.session = HTMLSession()
        self.root_url = root_url
        self.img_src = None
        self.filename = None
        
        self.constant_check = False
        self.last_check = 0
        self.total_auto_checks = 0
        
    def runTerminal(self):
        print('Welcome to DWU (pronounced dee-wu)!\nThe program that brings you a new waifu image every day :3')
        
        # threading.Thread(target=self.wallpaperCheckLoop, daemon=True).start()
        
        while True:
            user_input = input('> ').lower()
            if user_input.isspace() or len(user_input) == 0:
                continue
            elif user_input == 'exit' or user_input == 'e':
                print('Exiting...')
                break
            elif user_input.startswith('set '):
                n = int(user_input.split(' ')[1])
                print(f'Setting to the #{n} most recent wallpaper...')
                self.updateWallpaperImg(n)
                self.setWallpaper()
                print("Successfully set wallpaper!")
            elif user_input.startswith('start'):
                if self.constant_check:
                    print('Auto wallpaper updater is already running!')
                    continue
                threading.Thread(target=self.wallpaperCheckLoop, daemon=True).start()
            elif user_input.startswith('stop'):
                self.constant_check = False
            elif user_input.startswith('last'):
                print(f'The last auto wallpaper update was {round(time.time() - self.last_check, 3)} seconds ago')
                print(f'There have been {self.total_auto_checks} total auto updates')
            else:
                print(f'Unrecognized command or invalid syntax')
    
    def wallpaperCheckLoop(self):
        print('Started auto wallpaper updater in the background')
        self.constant_check = True
        self.last_check = 0
        while self.constant_check:
            if time.time() - self.last_check >= 600:
                self.updateWallpaperImg()
                self.setWallpaper()
                logging.info('Updated wallpaper')
                
                self.last_check = time.time()
                self.total_auto_checks += 1
        
        print('Stopped auto wallpaper updater')

    def updateWallpaperImg(self, n=0):
        # update SRC to the n'th wallpaper
        r = self.session.get(self.root_url)
        
        link = r.html.find('.post')[n].find('a')[0].attrs['href']
        r = self.session.get(link)
        if link.startswith('https://imgur.com'):
            self.img_src = r.html.find('.image-placeholder')[0].attrs['src']
        elif link.startswith('https://drive.google.com'):
            self.img_src = 'https://drive.google.com/uc?id=' + link.split('/')[5]
        else:
            self.img_src = link
        
        if self.img_src == None:
            self.img_src = self.img_src
            
        try:
            filename = 'latest_wallpaper.' + self.img_src.split('/')[-1].split('.')[1]
        except:
            filename = 'latest_wallpaper.png'

        response = self.session.get(self.img_src)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            logging.error(f'Failed to retrieve image. Status code: {response.status_code}')
            
        self.filename = filename

    def setWallpaper(self, path=None):
        if path == None:
            path = self.filename
        
        if not os.path.isfile(path):
            logging.error(f'File not found: {path}')
            return
        abs_path = os.path.abspath(path)

        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02

        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

        logging.info('Wallpaper set successfully!')

if __name__ == '__main__':
    try:
        DailyWallpaper().runTerminal()
    except Exception as e:
        crash=["Error on line {}".format(sys.exc_info()[-1].tb_lineno),"\n",e]
        print(''.join(list(map(str, crash))))
        timeX=str(time.time())
        with open("crashlogs/CRASH-"+timeX+".txt","w") as logfile:
            logfile.write(''.join(list(map(str, crash))))