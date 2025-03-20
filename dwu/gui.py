import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from .wallpaper_manager import WallpaperManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0

        self.setWindowTitle("dwu :3")

        self.wallupdate_button = QPushButton("owo")
        self.wallupdate_button.clicked.connect(self.setWallpaper)

        # Set the central widget of the Window.
        self.setCentralWidget(self.wallupdate_button)
        
        self.wallman = WallpaperManager()

    def setWallpaper(self):
        self.wallman.getSaveSet()

def run_gui():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()