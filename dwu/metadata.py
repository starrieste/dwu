from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
import json
import os

@dataclass
class WallpaperMetadata:
    img_url: str
    day: int
    add_watermark: bool =  True
    artist: Optional[str] = None
    source: Optional[str] = None
    post_id: Optional[str] = None
    successfully_set: bool = False
    
    @classmethod
    def load_current(cls) -> Optional[WallpaperMetadata]:
        cache_dir = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        metadata_path = os.path.join(cache_dir, 'dwu', 'current_wallpaper.json')
        
        if not os.path.exists(metadata_path):
            return None
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(**data)
    
    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)
