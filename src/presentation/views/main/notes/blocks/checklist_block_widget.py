# INLINE/src/presentation/views/main/notes/blocks/checklist_block_widget.py

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QInputDialog
)
from PySide6.QtCore import Signal


class ChecklistBlockWidget(QFrame):
    """
    Widget de bloc checklist avec cases à cocher.
    Permet d'ajouter, cocher et supprimer des items.
    Émet changed à chaque modification.
    """

    changed = Signal()

    def __init__(self, block_id: str, data: dict, parent=None):
        super().__init__(parent)
        self.block_id    = block_id
        self._layout     = QVBoxLayout(self)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._checkboxes = []

        for item in data.get("items", []):
            self._add_item_widget(item["text"], item.get("checked", False))

        btn_add = QPushButton("+ Ajouter un élément")
        btn_add.setStyleSheet("color: #4A90D9; border: none; text-align: left;")
        btn_add.clicked.connect(self._add_new_item)
        self._layout.addWidget(btn_add)

    def _add_item_widget(self, text: str, checked: bool = False):
        """Ajoute un item avec sa case à cocher et son bouton de suppression."""
        row    = QHBoxLayout()
        cb     = QCheckBox(text)
        cb.setChecked(checked)
        cb.stateChanged.connect(lambda _: self.changed.emit())

        btn_del = QPushButton("✕")
        btn_del.setFixedSize(20, 20)
        btn_del.setStyleSheet("color: #cc4444; border: none; font-size: 10px;")

        def remove():
            self._checkboxes.remove((cb, btn_del, row))
            cb.setParent(None)
            btn_del.setParent(None)
            self.changed.emit()

        btn_del.clicked.connect(remove)
        row.addWidget(cb)
        row.addWidget(btn_del)
        row.addStretch()

        insert_pos = self._layout.count() - 1
        self._layout.insertLayout(insert_pos, row)
        self._checkboxes.append((cb, btn_del, row))

    def _add_new_item(self):
        """Ouvre un dialog pour saisir le texte d'un nouvel item."""
        text, ok = QInputDialog.getText(self, "Nouvel élément", "Texte :")
        if ok and text:
            self._add_item_widget(text, False)
            self.changed.emit()

    def get_data(self) -> dict:
        """Retourne la liste des items avec leur état coché."""
        items = [
            {"text": cb.text(), "checked": cb.isChecked()}
            for cb, _, __ in self._checkboxes
        ]
        return {"items": items}