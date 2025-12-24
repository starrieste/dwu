from __future__ import annotations

import os
import httpx
import subprocess
import click

from urllib.parse import urlparse
from .scraper import WallpaperScraper
from .metadata import WallpaperMetadata

from PIL import Image, ImageDraw, ImageFont

class WallpaperSetError(Exception):
    pass

class ImageDownloadError(Exception):
    pass
    
class WallpaperManager:
    def __init__(self, root_url: str = 'https://wallpaper-a-day.com') -> None:
        self._scraper = WallpaperScraper()
        self._client = httpx.Client(timeout=30.0)
        self._cache_dir = self._get_cache_dir()
        self._metadata_path = os.path.join(self._cache_dir, "current_wallpaper.json")
    
    def _get_cache_dir(self) -> str:
        cache_dir = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        app_cache = os.path.join(cache_dir, 'dwu')
        os.makedirs(app_cache, exist_ok=True)
        return app_cache

    def update_wallpaper(self, post_index: int = 0) -> int:
        meta = self._scraper.get_metadata(post_index)
        if os.path.exists(self._metadata_path):
            old_meta = WallpaperMetadata.load_current()
            if old_meta is not None and meta.img_url == old_meta.img_url:
                image_path = self._get_image_path(meta)
                if os.path.exists(image_path):
                    if old_meta.successfully_set:
                        click.echo("Already using this wallpaper")
                        return False
                    else:
                        return self._set_wallpaper(image_path, meta)

        meta.save(self._metadata_path)
        filename = self._download_image(meta)
        return self._set_wallpaper(filename, meta)
        
    def _watermark_image(self, img_path: str, metadata: WallpaperMetadata):
        img = Image.open(img_path)
        w, h = img.size
        dw, dh = self._get_display_resolution()
        
        target_ratio = dw/dh
        difx, dify = 0, 0
        if (w / h) > target_ratio: # image is too wide
            nw = int(target_ratio * h)
            difx = (nw - w)//2
        else: # image is too tall
            nh = int(w / target_ratio)
            dify = (nh - h)//2
            
            
        font_size = int(min(w, h) * 0.02)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", font_size, index=0)
        except Exception as e:
            click.echo(e)
            try:
                font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", font_size)
            except Exception as ee:
                font = ImageFont.load_default()
                click.echo(ee)
        
        draw = ImageDraw.Draw(img)
        
        text = f"{metadata.artist}" if metadata.artist else ""
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        padding = int(min(w, h) * 0.015) 
        
        x = w - text_width - padding + difx
        y = h - text_height - padding + dify
        
        draw.text(
            (x, y),
            text,
            fill="white",
            font=font,
            stroke_width=1,
            stroke_fill="black",
        )
        
        img.save(img_path)   
        
    def _get_display_resolution(self) -> tuple:
        ds = self._detect_display_server()
        
        try:
            if ds == 'wayland':
                result = subprocess.run(
                    'wlr-randr | grep current',
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=True
                )
                res = result.stdout.strip().split(" ")[0]
                
            elif ds == 'x11':
                result = subprocess.run(
                    ['xrandr'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                for line in result.stdout.split('\n'):
                    if '*' in line:
                        res = line.split()[0]
                        break
                else:
                    return (1920, 1080)
            else:
                return (1920, 1080)
            
            return tuple(map(int, res.split('x')))
            
        except Exception as e:
            click.echo(f"Could not detect resolution: {e}")
            return (1920, 1080)
                
    def unwatermark(self, metadata: WallpaperMetadata):
        metadata.add_watermark = False
        metadata.save(self._metadata_path)
        filename = self._download_image(metadata)
        self._set_wallpaper(filename, metadata)
        
    def _get_image_path(self, metadata: WallpaperMetadata) -> str:
        """Get the path where the image should be saved, based on metadata."""
        ext = self._infer_extension(metadata.img_url)
        return os.path.join(self._cache_dir, f"current_wallpaper.{ext}")

    def _download_image(self, metadata: WallpaperMetadata) -> str:
        """Download the image using img_url from given metadata"""
        ext = self._infer_extension(metadata.img_url)
        save_path = os.path.join(self._cache_dir, f"current_wallpaper.{ext}")
        
        response = self._client.get(metadata.img_url)
        if response.status_code != 200:
            raise ImageDownloadError(f"Failed to download image ({response.status_code})")
            
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        if metadata.add_watermark:
            self._watermark_image(save_path, metadata)
        
        return save_path
        
    def _infer_extension(self, url: str) -> str:
        path = urlparse(url).path.lower()
        for ext in ("jpg", "jpeg", "png"):
            if path.endswith("." + ext):
                return ext
        return "png"

    def _set_wallpaper(self, filename: str, meta: WallpaperMetadata) -> bool:
        if not os.path.isfile(filename):
            raise WallpaperSetError("Wallpaper file not found")
            
        abs_path = os.path.abspath(filename)
        ds = self._detect_display_server()
        backends = [
            (["awww", "img", abs_path, "--transition-type", "any", 
                "--transition-step", "63", "--transition-duration", "2", 
                "--transition-fps", "60"], "awww"),
        ] if ds == 'wayland' else [ # else assume X11
            (["feh", "--bg-fill", abs_path], "feh"),
            (["nitrogen", "--set-scaled", abs_path], "nitrogen"), 
        ]
            
        for cmd, name in backends:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                self._send_notification(meta)
                return True
            except FileNotFoundError:
                continue
            except subprocess.CalledProcessError:
                continue
        
        click.echo("No supported wallpaper tool found. Please install one.")
        click.echo(f"I think you are using {ds.capitalize()}")
        click.echo(f"Currently supported wallpaper things for {ds.capitalize()} include " + ("awww" if ds == 'wayland' else "feh, nitrogen"))
        
        return False
        
    def _detect_display_server(self) -> str:
        if os.environ.get('WAYLAND_DISPLAY'):
            return 'wayland'
        elif os.environ.get('DISPLAY'):
            return 'x11'
        return 'unknown'
            
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
