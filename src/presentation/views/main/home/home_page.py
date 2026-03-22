# ======= home_page.py =======
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class HomePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Ceci est la page Accueil !!", self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)