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
            pystray.MenuItem("Exit", self._on_clicked)
        ))
        
        self.wallman = WallpaperManager()
        self.gui = GUI(self)
    
    def _on_clicked(self, icon, label) -> None:
        if str(label) == "Exit":
            self._quit()
        elif str(label) == "Open GUI":
            self.gui.show_gui()
    
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