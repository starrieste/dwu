from __future__ import annotations
import httpx
from selectolax.parser import HTMLParser

from .metadata import WallpaperMetadata

class ImageDownloadError(Exception):
    pass

class WallpaperScraper:
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
    
    def get_metadata(self, post_index: int = 0) -> WallpaperMetadata:
        response = self._client.get(self._root_url)
        tree = HTMLParser(response.text)

        posts = tree.css(".post")
        if not posts:
            raise ImageDownloadError("Could not find post")
        
        try:
            post = posts[post_index]
        except IndexError:
            raise ImageDownloadError(f"No post at index {post_index}")
            
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
                if link:
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
