from __future__ import annotations
import os
from urllib.parse import urlparse

import click

from .wallresult import WallResult

def get_cache_dir() -> str:
    cache_dir = os.environ.get(
        "XDG_CACHE_HOME",
        os.path.expanduser("~/.cache")
    )
    path = os.path.join(cache_dir, "dwu")
    os.makedirs(path, exist_ok=True)
    return path

def infer_extension(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in ("jpg", "jpeg", "png"):
        if path.endswith("." + ext):
            return ext
    return "png"

        
def detect_display_server() -> str:
    if os.environ.get('WAYLAND_DISPLAY'):
        return 'wayland'
    elif os.environ.get('DISPLAY'):
        return 'x11'
    return 'unknown'

def print_wall_feedback(result: WallResult) -> None:
    match result:
        case WallResult.TODAY:
            click.echo("Updated to today's wallpaper!")
        case WallResult.MOST_RECENT:
            click.echo("Updated to most recent unskipped wallpaper!")
        case WallResult.ALREADY_SET:
            click.echo("Already using this wallpaper.")
        case WallResult.SET:
            click.echo("Wallpaper set successfully!")
        case WallResult.NO_VALID:
            click.echo("No valid wallpapers available.")
