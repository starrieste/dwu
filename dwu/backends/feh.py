import subprocess
import shutil
from .base import WallpaperBackend

class FehBackend(WallpaperBackend):
    name = "feh"

    def is_available(self) -> bool:
        return shutil.which("feh") is not None

    def set_wallpaper(self, path: str) -> None:
        subprocess.run(
            ["feh", "--bg-fill", path],
            check=True,
            capture_output=True,
            text=True,
        )
