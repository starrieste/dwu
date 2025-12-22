from __future__ import annotations
import os
from urllib.parse import urlparse
import httpx
import subprocess

from .scraper import WallpaperScraper
from .metadata import WallpaperMetadata

class WallpaperSetError(Exception):
    pass

class ImageDownloadError(Exception):
    pass
    
class WallpaperManager:
    def __init__(self, root_url: str = 'https://wallpaper-a-day.com') -> None:
        self._scraper = WallpaperScraper()
        self._client = httpx.Client(timeout=30.0)
        self._cache_dir = self._get_cache_dir()
    
    def _get_cache_dir(self) -> str:
        cache_dir = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        app_cache = os.path.join(cache_dir, 'dwu')
        os.makedirs(app_cache, exist_ok=True)
        return app_cache

    def update_wallpaper(self, post_index: int = 0) -> None:
        meta = self._scraper.get_metadata(post_index)
        filename = self._download_image(meta)
        self._set_wallpaper(filename)
        self._send_notification(meta)

    def _download_image(self, metadata: WallpaperMetadata) -> str:
        ext = self._infer_extension(metadata.img_url)
        save_path = os.path.join(self._cache_dir, f"current_wallpaper.{ext}")
        metadata_path = os.path.join(self._cache_dir, "current_wallpaper.json")
        
        response = self._client.get(metadata.img_url)
        if response.status_code != 200:
            raise ImageDownloadError(f"Failed to download image ({response.status_code})")
            
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        metadata.save(metadata_path)
        
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
            raise WallpaperSetError("awww command not found. please install awww-git from the AUR.")
        except subprocess.CalledProcessError as e:
            raise WallpaperSetError(f"awww failed: {e.stderr}")
            
    def _send_notification(self, metadata: WallpaperMetadata):
        subprocess.run(
            [
                "notify-send", 
                f"Day {metadata.day}",
                f"Artist: {metadata.artist}"
            ],
            check=True,
            capture_output=True,
            text=True
        )
