from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("INLINE - Test UI")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Bienvenue dans INLINE", self)
        label.move(75, 50)


