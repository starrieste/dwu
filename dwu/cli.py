import threading
import time
from .wallpaper_manager import WallpaperManager

def run_terminal():
    print('Welcome to DWU (pronounced dee-wu)!\nThe program that brings you a new waifu image every day :3')
    dw = WallpaperManager()

    while True:
        user_input = input('> ').lower().strip()

        if not user_input:
            continue
        
        elif user_input in ('exit', 'e'):
            print('Exiting...')
            break
        
        elif user_input.startswith('set '):
            try:
                n = int(user_input.split()[1])
                dw.huntSRC(n)
                dw.saveWallpaper()
                dw.setWallpaper()
                print('Successfully set wallpaper!')
            except ValueError:
                print('Invalid command format. Try: set <number>')
            except IndexError:
                print('This tool can\'t get that index of wallpaper yet!')

        elif user_input.startswith('start'):
            if dw.constant_check:
                print('Auto wallpaper updater is already running!')
                continue
            threading.Thread(target=dw.wallpaperCheckLoop, daemon=True).start()

        elif user_input.startswith('stop'):
            dw.constant_check = False
            
        elif user_input.startswith('last'):
            if not dw.constant_check:
                print('Constant check loop is not running!')
                continue
            
            elapsed = round(time.time() - dw.last_check, 2)
            tot = round(time.time() - dw.starting_time, 2)
            print(f'The last auto wallpaper update was {elapsed} seconds ago' if dw.last_check != 0 else 'There hasn\'t been a check yet!')
            print(f'There have been {dw.total_auto_checks} total auto updates over {tot} seconds')

        else:
            print('Unrecognized command or invalid syntax')
