import re
import subprocess
from .base import WallpaperBackend

class AwwwBackend(WallpaperBackend):
    name = "awww"

    def set_wallpaper(self, path: str) -> None:
        subprocess.run(
            ["awww", "img", path, "--transition-type", "any",
            "--transition-step", "63", "--transition-duration", "2",
            "--transition-fps", "60"],
            check=True
        )

    def get_current_wallpaper(self) -> str | None:
        result = subprocess.run(
            ["awww", "query"],
            capture_output=True,
            text=True
        )
    
        if result.returncode != 0:
            return None
    
        match = re.search(r"image:\s*(.+)$", result.stdout.strip())
        return match.group(1) if match else None
