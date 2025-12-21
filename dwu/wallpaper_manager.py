from __future__ import annotations
import os
from urllib.parse import urlparse

import httpx
from selectolax.parser import HTMLParser

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
            
        link = self._extract_post_link(post)
        return self._resolve_image_url(link)

    def _extract_post_link(self, post) -> str:
        anchor = post.css_first("a")
        if not anchor:
            raise ImageDownloadError("Post contains no links")
            
        href = anchor.attributes.get("href")
        if not href:
            raise ImageDownloadError("Link has no href")
            
        return href
        
    def _resolve_image_url(self, link:str) -> str:
        response = self._client.get(link)
        tree = HTMLParser(response.text)
        
        if link.startswith("https://imgur.com"):
            img = tree.css_first(".image-placeholder")
            if not img:
                raise ImageDownloadError("Imgur image not found")
            return img.attributes["src"]
            
        if link.startswith("https://drive.google.com"):
            try:
                file_id = link.split("/")[5]
            except IndexError:
                raise ImageDownloadError("Invalid Google Drive Link")
            return f"https://drive.google.com/uc?id={file_id}"

        return link

    def _download_image(self, url: str) -> str:
        ext = self._infer_extension(url)
        filename = f"current_wallpaper.{ext}"
        
        response = self._client.get(url)
        if response.status_code != 200:
            raise ImageDownloadError(f"Failed to download image ({response.status_code}) from url {url}")
            
        with open(filename, "wb") as f:
            f.write(response.content)
        
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
        print(abs_path)
