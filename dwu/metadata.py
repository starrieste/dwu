from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
import json
import os
from urllib.parse import urlparse
from pathlib import PurePosixPath

from dwu.utils import get_cache_dir

@dataclass
class WallpaperMetadata:
    img_url: str
    day: int
    add_watermark: bool =  True
    artist: str = ""
    source: str = ""
    post_id: str = ""
    successfully_set: bool = False
    
    @classmethod
    def load(cls) -> Optional[WallpaperMetadata]:
        cache_dir = get_cache_dir()
        metadata_path = os.path.join(cache_dir, 'current_wallpaper.json')
        
        if not os.path.exists(metadata_path):
            return None
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(**data)
    
    def save(self) -> None:
        cache_dir = get_cache_dir()
        metadata_path = os.path.join(cache_dir, 'current_wallpaper.json')
        
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)
    
    def get_img_name(self) -> str:
        path = urlparse(self.img_url).path
        return PurePosixPath(path).name
        
    def __str__(self) -> str:
            lines = [
                f"Day: {self.day}",
                f"Image URL: {self.img_url}",
            ]
    
            if self.artist:
                lines.append(f"Artist: {self.artist}")
            if self.source:
                lines.append(f"Source: {self.source}")
    
            lines.append(
                f"Watermark: {'yes' if self.add_watermark else 'no'}"
            )
            lines.append(
                f"Successfully set: {'yes' if self.successfully_set else 'no'}"
            )
    
            return "\n".join(lines)
