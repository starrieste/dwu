import subprocess
import os

from .base import WallpaperBackend

class NitrogenBackend(WallpaperBackend):
    name = "nitrogen"

    def set_wallpaper(self, path: str) -> None:
        subprocess.run(
            ["nitrogen", "--set-scaled", path],
            check=True
        )

    def get_current_wallpaper(self) -> str | None:
        with open(
            os.path.expanduser("~/.config/nitrogen/bg-saved.cfg"),
            "r",
            encoding="utf-8"
        ) as f:
            for line in f:
                if line.startswith("file="):
                    return line.removeprefix("file=").strip()
