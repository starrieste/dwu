from __future__ import annotations
import os
import json
import click

from dwu.utils import get_cache_dir

class SkipManager:
    def __init__(self):
        self._cache_dir = get_cache_dir()
        self._skip_file = os.path.join(self._cache_dir, "skipped_wallpapers.json")
        self._skips: set[str] = set()
        self._load()
    
    def _load(self):
        if not os.path.exists(self._skip_file):
            return
        with open(self._skip_file, "r", encoding='utf-8') as f:
            try:
                self._skips = set(json.load(f))
            except Exception:
                self._skips = set()

    def _save(self):
        with open(self._skip_file, "w", encoding='utf-8') as f:
            json.dump(list(self._skips), f, indent=2, ensure_ascii=False)
            
    def is_skipped(self, img_url: str) -> bool:
        return img_url in self._skips
        
    def add(self, url: str | None) -> bool:
        if url is None or self.is_skipped(url):
            return False
        self._skips.add(url)
        self._save()
        return True
    
    def unskip(self, url: str) -> bool:
        if not self.is_skipped(url):
            return False
        
        self._skips.remove(url)
        self._save()
        return True
    
    def unskip_all(self):
        self._skips = set()
        self._save()
