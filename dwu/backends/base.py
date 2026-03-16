from __future__ import annotations
from typing import Optional
import shutil

class WallpaperBackend:
    name: str

    def is_available(self) -> bool:
        return shutil.which(self.name) is not None

    def set_wallpaper(self, path: str) -> None:
        raise NotImplementedError

    def get_current_wallpaper(self) -> Optional[str]:
        return None
