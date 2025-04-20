import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from .wallpaper_manager import WallpaperManager

app = QApplication(sys.argv) 

class GUI(QWidget):
    def __init__(self, st):
        super().__init__()

        self.setWindowTitle("Wallpaper Manager")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        btn1 = QPushButton("Update Wallpaper")
        btn2 = QPushButton("Start check loop")
        btn3 = QPushButton("Stop check loop")

        btn1.clicked.connect(st.wallman.update_wallpaper)
        btn2.clicked.connect(st.wallman.start_check_loop)
        btn3.clicked.connect(st.wallman.stop_check_loop)

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        self.setLayout(layout)
        self.show()

    def hide_gui(self):
        self.hide()

    def show_gui(self):
        self.show()
        
    def quit(self):
        self.close()
        QApplication.quit()