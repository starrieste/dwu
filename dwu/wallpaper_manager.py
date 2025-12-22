from __future__ import annotations
import os
from urllib.parse import urlparse

import httpx

from selectolax.parser import HTMLParser

import subprocess

class WallpaperError(Exception):
    pass

class ImageDownloadError(WallpaperError):
    pass

class WallpaperSetError(WallpaperError):
    pass

class WallpaperManager:
    def __init__(self, root_url: str = 'https://wallpaper-a-day.com') -> None:
        self._root_url = root_url
        self._client = httpx.Client(
            follow_redirects=True,
            timeout=10.0,
            headers={
                "User-Agent": "dwu/1.0 (+https://github.com/starrieste/dwu)",
                "Accept": "*/*",
                "Referer": self._root_url
            },
        )

    def update_wallpaper(self, post_index: int = 0) -> None:
        img_url = self._fetch_image_url(post_index)
        filename = self._download_image(img_url)
        self._set_wallpaper(filename)

    def _fetch_image_url(self, post_index: int = 0) -> str:
        response = self._client.get(self._root_url)
        tree = HTMLParser(response.text)

        posts = tree.css(".post")
        if not posts:
            raise ImageDownloadError("No posts found on page")
            
        try:
            post = posts[post_index]
        except IndexError:
            raise ImageDownloadError(f"No post at index {post_index}")
            
        return self._get_img_src(post)

    def _get_img_src(self, post) -> str:
        img_src = post.css_first("img").attributes.get("data-orig-file")
        if not img_src:
            raise ImageDownloadError("Image source could not be resolved")

        return img_src
        
    def _download_image(self, url: str) -> str:
        cache_dir = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        app_cache = os.path.join(cache_dir, 'dwu')
        os.makedirs(app_cache, exist_ok=True)
        
        ext = self._infer_extension(url)
        filename = os.path.join(app_cache, f"current_wallpaper.{ext}")
        
        response = self._client.get(url)
        if response.status_code != 200:
            raise ImageDownloadError(f"Failed to download image ({response.status_code}) from url {url}")
            
        with open(filename, "wb") as f:
            f.write(response.content)
            
        print(f"Wallpaper downloaded successfully to {filename}")
        
        return filename
        
    def _infer_extension(self, url: str) -> str:
        path = urlparse(url).path.lower()
        for ext in ("jpg", "jpeg", "png"):
            if path.endswith("." + ext):
                return ext
        return "png"

    def _set_wallpaper(self, filename: str) -> None:
        if not os.path.isfile(filename):
            raise WallpaperSetError("Wallpaper file not found")
            
        abs_path = os.path.abspath(filename)
        try:
            subprocess.run(
                [
                    "awww", "img", abs_path,
                    "--transition-type", "any",
                    "--transition-step", "63",
                    "--transition-duration", "2",
                    "--transition-fps", "60"
                ],
                check=True,
                capture_output=True,
                text=True
            )
        except FileNotFoundError:
            raise WallpaperSetError("awww command not found. please install awww.")
        except subprocess.CalledProcessError as e:
            raise WallpaperSetError(f"awww failed: {e.stderr}")
