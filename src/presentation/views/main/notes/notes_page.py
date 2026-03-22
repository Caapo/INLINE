# ======= notes_page.py =======
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class NotesPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Ceci est la page Notes !!", self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)