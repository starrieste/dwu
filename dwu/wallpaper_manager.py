from __future__ import annotations
import threading
import os
import ctypes
import time
from typing import Optional
from requests_html import HTMLSession

UPDATE_INTERVAL = 1800
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

class WallpaperError(Exception):
    pass

class ImageDownloadError(WallpaperError):
    pass

class WallpaperSetError(WallpaperError):
    pass

class WallpaperManager:
    def __init__(self, root_url: str = 'https://wallpaper-a-day.com') -> None:
        self._session = HTMLSession()
        self._root_url = root_url
        self._img_src: Optional[str] = None
        self._filename: Optional[str] = None

        self._queued_state: bool = False
        self._in_progress: bool = False
        self._starting_time: float = 0
        self._last_check: float = 0
        self._total_auto_checks: int = 0

    def update_wallpaper(self, post_index: int = 0) -> None:
        threading.Thread(target=self._update_wallpaper, args=(post_index,), daemon=True).start()

    def _update_wallpaper(self, post_index: int = 0) -> None:
        self._fetch_image_source(post_index)
        self._save_wallpaper()
        self._set_wallpaper()

    def start_check_loop(self) -> None:
        if self._in_progress:
            print("Check loop is already running!")
            return
        threading.Thread(target=self._wallpaper_check_loop, daemon=True).start()

    def stop_check_loop(self) -> None:
        self._queued_state = False

    def toggle_check_loop(self) -> None:
        if self._in_progress:
            self._queued_state = False
        elif not self._in_progress:
            threading.Thread(target=self._wallpaper_check_loop, daemon=True).start()

    def _fetch_image_source(self, post_index: int = 0) -> None:
        try:
            response = self._session.get(self._root_url)

            posts = response.html.find('.post')

            if not posts or (post_index >= len(posts)):
                raise ImageDownloadError(f"No post found at index {post_index}")

            link = posts[post_index].find('a')[0].attrs.get('href')
            if not link:
                raise ImageDownloadError("No link found in post")

            # next link
            response = self._session.get(link)
            if link.startswith('https://imgur.com'):
                placeholder = response.html.find('.image-placeholder')
                self._img_src = placeholder[0].attrs['src'] if placeholder else None

            elif link.startswith('https://drive.google.com'):
                self._img_src = f'https://drive.google.com/uc?id={link.split("/")[5]}'

            else: # assume the first image on this site is the right one
                self._img_src = link

        except Exception as e:
            print(f"Failed to fetch image source")
            raise ImageDownloadError(f"Failed to fetch image source: {str(e)}")

    def _save_wallpaper(self) -> None:
        if not self._img_src:
            print(f"No image source available")
            raise ImageDownloadError("No image source available")
        try:
            ext = 'png'
            if self._img_src.lower().endswith(('jpg', 'jpeg', 'png')):
                ext = self._img_src.split('.')[-1]
            self._filename = f'latest_wallpaper.{ext}'
            response = self._session.get(self._img_src)
            if response.status_code != 200:
                raise ImageDownloadError(f"Failed to download image: Status {response.status_code}")
            with open(self._filename, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to save wallpapaer")
            raise ImageDownloadError(f"Failed to save wallpaper: {str(e)}")

    def _set_wallpaper(self) -> None:
        if not self._filename or not os.path.isfile(self._filename):
            raise WallpaperSetError("Wallpaper file not found")
        try:
            abs_path = os.path.abspath(self._filename)
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, abs_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            if not result:
                print("Failed to set wallpaper using Windows API")
                raise WallpaperSetError("Failed to set wallpaper using Windows API")
        except Exception as e:
            print(f"Failed to set wallpaper")
            raise WallpaperSetError(f"Failed to set wallpaper: {str(e)}")

    def _wallpaper_check_loop(self) -> None:
        self._starting_time = time.time()
        self._last_check = 0
        self._total_auto_checks = 0

        self._in_progress = True
        self._queued_state = True
        while self._queued_state:
            current_time = time.time()
            if current_time - self._last_check >= UPDATE_INTERVAL:
                self.update_wallpaper()
                self._last_check = current_time
                self._total_auto_checks += 1
                print("Automatically updated wallpaper!")
            time.sleep(1)

        self._in_progress = False
