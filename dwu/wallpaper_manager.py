from __future__ import annotations

import os
import httpx
import subprocess
import click

from .scraper import WallpaperScraper
from .metadata import WallpaperMetadata
from .skip_manager import SkipManager
from .utils import get_cache_dir, infer_extension, detect_display_server
from .wallresult import WallResult

from PIL import Image, ImageDraw, ImageFont

class WallpaperSetError(Exception):
    pass

class ImageDownloadError(Exception):
    pass
    
class WallpaperManager:
    def __init__(self, root_url: str = 'https://wallpaper-a-day.com') -> None:
        self._scraper = WallpaperScraper()
        self._client = httpx.Client(timeout=30.0)
        self._cache_dir = get_cache_dir()
        self._metadata_path = os.path.join(self._cache_dir, "current_wallpaper.json")
        
    def update_back(self, days: int) -> WallResult:
        meta = self._scraper.get_metadata(days)
        return self._apply_wallpaper(meta)
        
    def update_auto(self) -> WallResult:
        walls = self._scraper.get_all()
        skips = SkipManager()
        
        for i, meta in enumerate(walls):
            if skips.is_skipped(meta.img_url):
                continue
        
            result = self._apply_wallpaper(meta)
            if result == WallResult.ALREADY_SET:
                return result
            return WallResult.TODAY if i == 0 else WallResult.MOST_RECENT
        
        return WallResult.NO_VALID
        
    
    def _apply_wallpaper(self, meta: WallpaperMetadata) -> WallResult:
        old_meta = WallpaperMetadata.load()
        
        if old_meta and old_meta.img_url == meta.img_url:
            if old_meta.successfully_set:
                return WallResult.ALREADY_SET
            
            image_path = self._get_image_path(meta)
            if os.path.exists(image_path):
                self._set_wallpaper(image_path, meta)
                return WallResult.SET
        
        meta.save()
        self._set_wallpaper(self._download_image(meta), meta)
        return WallResult.SET
        
        
    def _watermark_image(self, img_path: str, metadata: WallpaperMetadata) -> None:
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
        ds = detect_display_server()
        
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
                
    def unwatermark(self, metadata: WallpaperMetadata) -> None:
        metadata.add_watermark = False
        metadata.save()
        filename = self._download_image(metadata)
        self._set_wallpaper(filename, metadata)
        
    def _get_image_path(self, metadata: WallpaperMetadata) -> str:
        ext = infer_extension(metadata.img_url)
        return os.path.join(self._cache_dir, f"current_wallpaper.{ext}")

    def _download_image(self, metadata: WallpaperMetadata) -> str:
        ext = infer_extension(metadata.img_url)
        save_path = os.path.join(self._cache_dir, f"current_wallpaper.{ext}")
        
        response = self._client.get(metadata.img_url)
        if response.status_code != 200:
            raise ImageDownloadError(f"Failed to download image ({response.status_code})")
            
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        click.echo(f"Successfully downloaded wallpaper to {save_path}!")
        
        if metadata.add_watermark:
            self._watermark_image(save_path, metadata)
        
        return save_path
        
    def _set_wallpaper(self, filename: str, meta: WallpaperMetadata) -> None:
        if not os.path.isfile(filename):
            raise WallpaperSetError("Wallpaper file not found")
            
        abs_path = os.path.abspath(filename)
        ds = detect_display_server()
        backends = [
            (["awww", "img", abs_path, "--transition-type", "any", 
                "--transition-step", "63", "--transition-duration", "2", 
                "--transition-fps", "60"], "awww"),
            (["swww", "img", abs_path, "--transition-type", "any", 
                "--transition-step", "63", "--transition-duration", "2", 
                "--transition-fps", "60"], "swww"),
        ] if ds == 'wayland' else [ # else assume X11
            (["feh", "--bg-fill", abs_path], "feh"),
            (["nitrogen", "--set-scaled", abs_path], "nitrogen"), 
        ]
            
        for cmd, name in backends:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                meta.successfully_set = True
                meta.save()
                return
            except FileNotFoundError:
                continue
            except subprocess.CalledProcessError:
                continue
        
        click.echo("No supported wallpaper tool found. Please install one.")
        click.echo(f"I think you are using {ds.capitalize()}")
        click.echo(f"Currently supported wallpaper things for {ds.capitalize()} include " + ("awww" if ds == 'wayland' else "feh, nitrogen"))
