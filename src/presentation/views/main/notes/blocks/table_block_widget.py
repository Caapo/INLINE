# INLINE/src/presentation/views/main/notes/blocks/table_block_widget.py

from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog)
from PySide6.QtCore import Signal


class TableBlockWidget(QFrame):
    """
    Widget de bloc tableau avec en-têtes et lignes dynamiques.
    Permet d'ajouter des lignes et des colonnes dynamiquement.
    Émet changed à chaque modification.
    """

    changed = Signal()

    def __init__(self, block_id: str, data: dict, parent=None):
        super().__init__(parent)
        self.block_id = block_id

        layout  = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        headers = data.get("headers", [])
        rows    = data.get("rows", [])

        self.table = QTableWidget(len(rows), max(len(headers), 1))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(val))

        self.table.cellChanged.connect(lambda r, c: self.changed.emit())
        layout.addWidget(self.table)

        btn_layout  = QHBoxLayout()
        btn_add_row = QPushButton("+ Ligne")
        btn_add_col = QPushButton("+ Colonne")
        btn_add_row.clicked.connect(self._add_row)
        btn_add_col.clicked.connect(self._add_col)
        btn_layout.addWidget(btn_add_row)
        btn_layout.addWidget(btn_add_col)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _add_row(self):
        """Ajoute une ligne vide au tableau."""
        self.table.insertRow(self.table.rowCount())
        self.changed.emit()

    def _add_col(self):
        """Ajoute une colonne avec un nom saisi via dialog."""
        col_name, ok = QInputDialog.getText(self, "Nouvelle colonne", "Nom de la colonne :")
        if ok and col_name:
            idx = self.table.columnCount()
            self.table.insertColumn(idx)
            self.table.setHorizontalHeaderItem(idx, QTableWidgetItem(col_name))
            self.changed.emit()

    def get_data(self) -> dict:
        """Retourne les en-têtes et les lignes du tableau."""
        headers = [
            self.table.horizontalHeaderItem(c).text()
            if self.table.horizontalHeaderItem(c) else ""
            for c in range(self.table.columnCount())
        ]
        rows = []
        for r in range(self.table.rowCount()):
            row = []
            for c in range(self.table.columnCount()):
                item = self.table.item(r, c)
                row.append(item.text() if item else "")
            rows.append(row)
        return {"headers": headers, "rows": rows}