import re
import subprocess
from dwu.backends.base import WallpaperBackend

class SwwwBackend(WallpaperBackend):
    name = "swww"

    def set_wallpaper(self, path: str) -> None:
        subprocess.run(
            ["swww", "img", path, "--transition-type", "any",
            "--transition-step", "63", "--transition-duration", "2",
            "--transition-fps", "60"],
            check=True
        )

    def get_current_wallpaper(self) -> str | None:
        result = subprocess.run(
            ["swww", "query"],
            capture_output=True,
            text=True
        )
    
        if result.returncode != 0:
            return None
    
        match = re.search(r"image:\s*(.+)$", result.stdout.strip())
        return match.group(1) if match else None
