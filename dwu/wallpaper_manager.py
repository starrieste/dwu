from __future__ import annotations
import threading
from typing import Optional

import os
import ctypes
import time
from pathlib import Path
from requests_html import HTMLSession

UPDATE_INTERVAL = 600  # 10 minutes
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

class WallpaperError(Exception):
    """Base exception for wallpaper-related errors."""
    pass

class ImageDownloadError(WallpaperError):
    """Raised when image download fails."""
    pass

class WallpaperSetError(WallpaperError):
    """Raised when setting wallpaper fails."""
    pass

class WallpaperManager:
    """Manages wallpaper downloading and setting functionality."""

    def __init__(self, root_url: str = 'https://wallpaper-a-day.com') -> None:
        """
        Initialize WallpaperManager.
        Args:
            root_url: Base URL for wallpaper source
        """
        self.session = HTMLSession()
        self.root_url = root_url
        self.img_src: Optional[str] = None
        self.filename: Optional[str] = None
        self.constant_check: bool = False
        self.starting_time: float = 0
        self._last_check: float = 0
        self._total_auto_checks: int = 0

    def update_wallpaper(self, post_index: int = 0) -> None:
        """
        Update wallpaper from specified post index.

        Args:
            post_index: Index of the post to fetch from

        Raises:
            WallpaperError: If any step of the update process fails
        """
        try:
            self._fetch_image_source(post_index)
            if not self.img_src:
                raise ImageDownloadError("No image source found")
            self._save_wallpaper()
            self._set_wallpaper()
        except Exception as e:
            raise WallpaperError(f"Failed to update wallpaper: {str(e)}")
    
    def start_check_loop(self) -> None:
        """Start the wallpaper check loop."""
        threading.Thread(target=self._wallpaper_check_loop, daemon=True).start()
        
    
    def stop_check_loop(self) -> None:
        """Stop the wallpaper check loop."""
        self.constant_check = False

    def _fetch_image_source(self, post_index: int = 0) -> None:
        """
        Fetch image source URL from website.

        Args:
            post_index: Index of the post to fetch from

        Raises:
            ImageDownloadError: If image source cannot be fetched
        """
        try:
            response = self.session.get(self.root_url)
            posts = response.html.find('.post')

            if not posts or (post_index >= len(posts)):
                raise ImageDownloadError(f"No post found at index {post_index}")

            link = posts[post_index].find('a')[0].attrs.get('href')
            if not link:
                raise ImageDownloadError("No link found in post")

            response = self.session.get(link)

            if link.startswith('https://imgur.com'):
                placeholder = response.html.find('.image-placeholder')
                self.img_src = placeholder[0].attrs['src'] if placeholder else None
            elif link.startswith('https://drive.google.com'):
                self.img_src = f'https://drive.google.com/uc?id={link.split("/")[5]}'
            else:
                self.img_src = link

        except Exception as e:
            raise ImageDownloadError(f"Failed to fetch image source: {str(e)}")

    def _save_wallpaper(self) -> None:
        """
        Save wallpaper image to local file.

        Raises:
            ImageDownloadError: If saving the image fails
        """
        if not self.img_src:
            raise ImageDownloadError("No image source available")

        try:
            ext = 'png'
            if self.img_src.lower().endswith(('jpg', 'jpeg', 'png')):
                ext = self.img_src.split('.')[-1]

            self.filename = f'latest_wallpaper.{ext}'

            response = self.session.get(self.img_src)
            if response.status_code != 200:
                raise ImageDownloadError(f"Failed to download image: Status {response.status_code}")

            with open(self.filename, 'wb') as f:
                f.write(response.content)

        except Exception as e:
            raise ImageDownloadError(f"Failed to save wallpaper: {str(e)}")

    def _set_wallpaper(self) -> None:
        """
        Set the wallpaper using Windows API.

        Raises:
            WallpaperSetError: If setting the wallpaper fails
        """
        if not self.filename or not os.path.isfile(self.filename):
            raise WallpaperSetError("Wallpaper file not found")

        try:
            abs_path = os.path.abspath(self.filename)
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, abs_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )

            if not result:
                raise WallpaperSetError("Failed to set wallpaper using Windows API")

        except Exception as e:
            raise WallpaperSetError(f"Failed to set wallpaper: {str(e)}")
    
    def _wallpaper_check_loop(self) -> None:
        """Continuous wallpaper check loop."""
        self.constant_check = True
        self.starting_time = time.time()
        self._last_check = 0
        self._total_auto_checks = 0

        while self.constant_check:
            current_time = time.time()
            if current_time - self._last_check >= UPDATE_INTERVAL:
                self.update_wallpaper()
                self._last_check = current_time
                self._total_auto_checks += 1
                time.sleep(60)  # Sleep for a minute before next check