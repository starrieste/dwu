from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget
)

class GUI(QMainWindow):
    def __init__(self, st):
        super().__init__()
        
        self.st = st
        self.setWindowTitle("Wallpaper Manager")
        self.setGeometry(300, 300, 300, 150)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.btn1 = QPushButton("Update Wallpaper")
        self.btn2 = QPushButton("Start check loop")
        self.btn3 = QPushButton("Stop check loop")

        self.btn1.clicked.connect(self.st.wallman.update_wallpaper)
        self.btn2.clicked.connect(self.st.wallman.start_check_loop)
        self.btn3.clicked.connect(self.st.wallman.stop_check_loop)

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)

        central_widget.setLayout(layout)

        self.show()

    def hide_gui(self):
        self.hide()

    def show_gui(self):
        self.show()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        self.hide()
        event.ignore()