import pystray
import PIL.Image

from dwu.wallpaper_manager import WallpaperManager

from .gui import GUI

class TrayIcon():
    def __init__(self):
        self.image = PIL.Image.open("icon.png")
        self.icon = pystray.Icon("test_icon", self.image, menu=pystray.Menu(
            pystray.MenuItem("Open GUI", self._on_clicked),
            pystray.MenuItem("Close GUI", self._on_clicked),
            pystray.MenuItem("Exit", self._on_clicked)
        ))
        
        self.wallman = WallpaperManager()
        self.gui = GUI(self)
    
    def _on_clicked(self, icon, item) -> None:
        if str(item) == "Exit":
            self._quit()
        elif str(item) == "Open GUI":
            self.gui.show_gui()
        elif str(item) == "Close GUI":
            self.gui.hide_gui()
    
    def run(self):
        self.icon.run()
        
    def _quit(self):
        self.wallman.stop_check_loop()
        self.gui.quit()
        self.icon.stop()