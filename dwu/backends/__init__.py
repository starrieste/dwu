from dwu.backends.nitrogen import NitrogenBackend
from dwu.backends.awww import AwwwBackend
from dwu.backends.feh import FehBackend
from dwu.backends.swww import SwwwBackend
from dwu.backends.base import WallpaperBackend

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
