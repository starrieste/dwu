from dwu.backends.nitrogen import NitrogenBackend
from .awww import AwwwBackend
from .feh import FehBackend
from .swww import SwwwBackend
from .base import WallpaperBackend

WAYLAND_BACKENDS = [
    AwwwBackend(),
    SwwwBackend(),
]

X11_BACKENDS = [
    FehBackend(),
    NitrogenBackend()
]

def get_backend(display_server: str) -> WallpaperBackend | None:
    for backend in (WAYLAND_BACKENDS if display_server == 'wayland' else X11_BACKENDS):
        if backend.is_available():
            return backend
    raise RuntimeError("No supported wallpaper backend found")
