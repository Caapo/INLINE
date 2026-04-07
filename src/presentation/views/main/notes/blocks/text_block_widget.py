# INLINE/src/presentation/views/main/notes/blocks/text_block_widget.py

from PySide6.QtWidgets import QFrame, QVBoxLayout, QTextEdit, QSizePolicy
from PySide6.QtCore import Signal


class TextBlockWidget(QFrame):
    """
    Widget de bloc texte libre multi-lignes.
    Émet changed à chaque modification du contenu.
    """

    changed = Signal()

    def __init__(self, block_id: str, data: dict, parent=None):
        super().__init__(parent)
        self.block_id = block_id

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.edit = QTextEdit()
        self.edit.setPlaceholderText("Écrivez votre texte ici...")
        self.edit.setText(data.get("content", ""))
        self.edit.setMinimumHeight(80)
        self.edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.edit.textChanged.connect(lambda: self.changed.emit())
        layout.addWidget(self.edit)

    def get_data(self) -> dict:
        """Retourne le contenu textuel du bloc."""
        return {"content": self.edit.toPlainText()}