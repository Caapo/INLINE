# INLINE/src/presentation/views/main/notes/blocks/title_block_widget.py

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QComboBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont


class TitleBlockWidget(QFrame):
    """
    Widget de bloc titre avec niveau hiérarchique (H1, H2, H3).
    Émet changed à chaque modification pour signaler
    que la note doit être sauvegardée.
    """

    changed = Signal()

    def __init__(self, block_id: str, data: dict, parent=None):
        super().__init__(parent)
        self.block_id = block_id

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.level_combo = QComboBox()
        self.level_combo.addItems(["H1", "H2", "H3"])
        self.level_combo.setCurrentIndex(data.get("level", 1) - 1)
        self.level_combo.setFixedWidth(50)

        self.edit = QLineEdit(data.get("text", ""))
        self.edit.setPlaceholderText("Titre...")
        self._apply_style(data.get("level", 1))

        layout.addWidget(self.level_combo)
        layout.addWidget(self.edit)

        self.level_combo.currentIndexChanged.connect(lambda _: self._on_level_changed())
        self.edit.textChanged.connect(lambda _: self.changed.emit())

    def _on_level_changed(self):
        """Met à jour le style de la police selon le niveau sélectionné."""
        self._apply_style(self.level_combo.currentIndex() + 1)
        self.changed.emit()

    def _apply_style(self, level: int):
        """Applique la taille de police correspondant au niveau de titre."""
        sizes = {1: 20, 2: 16, 3: 13}
        font  = QFont("Courier New", sizes.get(level, 16))
        font.setBold(True)
        self.edit.setFont(font)

    def get_data(self) -> dict:
        """Retourne les données du bloc sous forme de dictionnaire."""
        return {
            "text":  self.edit.text(),
            "level": self.level_combo.currentIndex() + 1
        }