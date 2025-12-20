from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon

class GUI(QMainWindow):
    show_signal = pyqtSignal()
    hide_signal = pyqtSignal()
    
    def __init__(self, st):
        super().__init__()
        
        self.st = st
        self.setWindowTitle("DWU :3")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(300, 300, 300, 70)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.btn1 = QPushButton("Update Wallpaper")
        self.btn2 = QPushButton("Start check loop")
        self._btn2() # Start by default

        self.btn1.clicked.connect(self.st.wallman.update_wallpaper)
        self.btn2.clicked.connect(self._btn2)

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        central_widget.setLayout(layout)

        self.show_signal.connect(self.show)
        self.hide_signal.connect(self.hide)

        self.hide()

    def _btn2(self):
        self.st.wallman.toggle_check_loop()
        if self.st.wallman._queued_state:
            self.btn2.setText("Stop check loop")
        else:
            self.btn2.setText("Start check loop")

    def hide_gui(self):
        self.hide_signal.emit()

    def show_gui(self):
        self.show_signal.emit()

    def closeEvent(self, event):
        self.hide()
        event.ignore()