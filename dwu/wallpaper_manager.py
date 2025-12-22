from __future__ import annotations
import os
from urllib.parse import urlparse

import httpx

from selectolax.parser import HTMLParser

import subprocess

import json
from dataclasses import dataclass, asdict
from typing import Optional

class WallpaperError(Exception):
    pass

class ImageDownloadError(WallpaperError):
    pass

class WallpaperSetError(WallpaperError):
    pass
    
    
@dataclass
class WallpaperMetadata:
    img_url: str
    artist: Optional[str] = None
    source: Optional[str] = None
    post_id: Optional[str] = None

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
        meta = self._get_metadata(post_index)
        filename = self._download_image(meta)
        self._set_wallpaper(filename)

    def _get_metadata(self, post_index: int = 0) -> WallpaperMetadata:
        response = self._client.get(self._root_url)
        tree = HTMLParser(response.text)

        posts = tree.css(".post")
        if not posts:
            raise ImageDownloadError("Could not find post")
        if not posts[post_index]:
            raise ImageDownloadError(f"No post at index {post_index}")
            
        post = posts[post_index]
            
        img = post.css_first("img")
        if not img:
            raise ImageDownloadError("No image in post")
            
        img_url = img.attributes.get("data-orig-file")
        if not img_url:
            raise ImageDownloadError("Image source could not be resolved")
            
        artist = None
        source = None
        
        paragraphs = post.css('p')
        for p in paragraphs:
            if "credit" in p.text().lower():
                link = p.css_first("a")
                if not link:
                    print("Could not find link to artist for this wallpaper")
                    break
                artist = link.text().strip()
                source = link.attributes.get("href")
                break
                
        post_id = post.attributes.get('id')
            
        return WallpaperMetadata(
            img_url=img_url,
            artist=artist,
            source=source,
            post_id=post_id
        )

    def _download_image(self, metadata: WallpaperMetadata) -> str:
        cache_dir = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        app_cache = os.path.join(cache_dir, 'dwu')
        os.makedirs(app_cache, exist_ok=True)
        
        img_url = metadata.img_url
        
        ext = self._infer_extension(img_url)
        save_path = os.path.join(app_cache, f"current_wallpaper.{ext}")
        metadata_path = os.path.join(app_cache, "current_wallpaper.json")
        
        response = self._client.get(img_url)
        if response.status_code != 200:
            raise ImageDownloadError(f"Failed to download image ({response.status_code}) from url {img_url}")
            
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        with open(metadata_path, "w") as f:
            json.dump(asdict(metadata), f, indent=4, ensure_ascii=False)
            
        print(f"Wallpaper downloaded successfully to {save_path}")
        
        return save_path
        
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
