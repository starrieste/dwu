import os
import sys
import threading
import pystray
import PIL.Image

from dwu.wallpaper_manager import WallpaperManager
from .gui import GUI
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

class App():
    def __init__(self):
        self.image = PIL.Image.open("icon.png")
        self.icon = pystray.Icon("test_icon", self.image, menu=pystray.Menu(
            pystray.MenuItem("Open GUI", self._on_clicked),
            pystray.MenuItem("Run at Startup", self._toggle_startup, checked=self._is_startup_enabled),
            pystray.MenuItem("Exit", self._on_clicked)
        ))
        
        self.wallman = WallpaperManager()
        self.gui = GUI(self)
    
    def _on_clicked(self, icon, label) -> None:
        if str(label) == "Open GUI":
            self.gui.show_gui()
        elif str(label) == "Exit":
            self._quit()
        
    def _toggle_startup(self, icon, label) -> None:
        from win32com.client import Dispatch

        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\dwu.lnk')
        
        if self._is_startup_enabled():
            os.remove(startup_path)
        else:
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(startup_path)
            # Use the actual exe path instead of Python interpreter
            exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
            shortcut.Targetpath = exe_path
            shortcut.WorkingDirectory = os.path.dirname(exe_path)
            # No need for additional arguments when it's a compiled exe
            if not getattr(sys, 'frozen', False):
                shortcut.Arguments = f'"{os.path.abspath(sys.argv[0])}"'
            shortcut.save()

    def _is_startup_enabled(self, x=None) -> bool:
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\dwu.lnk')
        return os.path.exists(startup_path)
    
    def _quit(self):
        self.wallman.stop_check_loop()
        QTimer.singleShot(0, self.gui.close)
        self.icon.stop()
        QTimer.singleShot(0, QApplication.quit)
        os._exit(0)

def run_app():
    qapp = QApplication(sys.argv)
    app = App()
    threading.Thread(target=app.icon.run, daemon=True).start()
    sys.exit(qapp.exec())