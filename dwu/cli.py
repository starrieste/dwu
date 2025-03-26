import threading
import time
from .wallpaper_manager import WallpaperManager

def run_cli():
    print('Welcome to DWU (pronounced dee-wu)!\nThe program that brings you a new waifu image every day :3')
    wallman = WallpaperManager()

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
                wallman.huntSRC(n)
                wallman.saveWallpaper()
                wallman.setWallpaper()
                print('Successfully set wallpaper!')
            except ValueError:
                print('Invalid command format. Try: set <number>')
            except IndexError:
                print('This tool can\'t get that index of wallpaper yet!')

        elif user_input.startswith('start'):
            if wallman.constant_check:
                print('Auto wallpaper updater is already running!')
                continue
            threading.Thread(target=wallman.wallpaperCheckLoop, daemon=True).start()

        elif user_input.startswith('stop'):
            wallman.constant_check = False
            
        elif user_input.startswith('last'):
            if not wallman.constant_check:
                print('Constant check loop is not running!')
                continue
            
            elapsed = round(time.time() - wallman.last_check, 2)
            tot = round(time.time() - wallman.starting_time, 2)
            print(f'The last auto wallpaper update was {elapsed} seconds ago' if wallman.last_check != 0 else 'There hasn\'t been a check yet!')
            print(f'There have been {wallman.total_auto_checks} total auto updates over {tot} seconds')

        else:
            print('Unrecognized command or invalid syntax')
