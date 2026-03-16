from __future__ import annotations
import os
import subprocess
from urllib.parse import urlparse

import click

from dwu.wallresult import WallResult

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
    
def get_display_resolution() -> tuple:
    ds = detect_display_server()
    
    try:
        if ds == 'wayland':
            result = subprocess.run(
                'wlr-randr | grep current',
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            res = result.stdout.strip().split(" ")[0]
            
        elif ds == 'x11':
            result = subprocess.run(
                ['xrandr'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n'):
                if '*' in line:
                    res = line.split()[0]
                    break
            else:
                return (1920, 1080)
        else:
            return (1920, 1080)
        
        return tuple(map(int, res.split('x')))
        
    except Exception as e:
        click.echo(f"Could not detect resolution: {e}")
        return (1920, 1080)
                

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
