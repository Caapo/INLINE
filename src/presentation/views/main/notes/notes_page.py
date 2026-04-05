# ======= INLINE/src/presentation/views/main/notes/notes_page.py =======

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QSplitter, QFrame,
    QInputDialog, QMessageBox, QScrollArea, QSizePolicy,
    QLineEdit, QTextEdit, QCheckBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor
from domain.enums.enums import BlockType


# =============================================================
# Widgets de blocs
# =============================================================

class TitleBlockWidget(QFrame):
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
        self._apply_style(self.level_combo.currentIndex() + 1)
        self.changed.emit()

    def _apply_style(self, level):
        sizes = {1: 20, 2: 16, 3: 13}
        font = QFont()
        font.setBold(True)
        font.setPointSize(sizes.get(level, 16))
        self.edit.setFont(font)

    def get_data(self) -> dict:
        return {"text": self.edit.text(), "level": self.level_combo.currentIndex() + 1}


class TextBlockWidget(QFrame):
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
        # self.edit.textChanged.connect(self.changed.emit)
        self.edit.textChanged.connect(lambda: self.changed.emit())
        layout.addWidget(self.edit)

    def get_data(self) -> dict:
        return {"content": self.edit.toPlainText()}


class ChecklistBlockWidget(QFrame):
    changed = Signal()

    def __init__(self, block_id: str, data: dict, parent=None):
        super().__init__(parent)
        self.block_id = block_id
        self._layout  = QVBoxLayout(self)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._checkboxes = []

        for item in data.get("items", []):
            self._add_item_widget(item["text"], item.get("checked", False))

        btn_add = QPushButton("+ Ajouter un élément")
        btn_add.setStyleSheet("color: #4A90D9; border: none; text-align: left;")
        btn_add.clicked.connect(self._add_new_item)
        self._layout.addWidget(btn_add)

    def _add_item_widget(self, text: str, checked: bool = False):
        row = QHBoxLayout()
        cb  = QCheckBox(text)
        cb.setChecked(checked)
        # cb.stateChanged.connect(lambda _: self.changed.emit)
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
        text, ok = QInputDialog.getText(self, "Nouvel élément", "Texte :")
        if ok and text:
            self._add_item_widget(text, False)
            self.changed.emit()

    def get_data(self) -> dict:
        items = [{"text": cb.text(), "checked": cb.isChecked()} for cb, _, __ in self._checkboxes]
        return {"items": items}


class TableBlockWidget(QFrame):
    changed = Signal()

    def __init__(self, block_id: str, data: dict, parent=None):
        super().__init__(parent)
        self.block_id = block_id
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        headers = data.get("headers", [])
        rows    = data.get("rows", [])

        self.table = QTableWidget(len(rows), max(len(headers), 1))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(val))

        self.table.cellChanged.connect(lambda: self.changed.emit())
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add_row = QPushButton("+ Ligne")
        btn_add_col = QPushButton("+ Colonne")
        btn_add_row.clicked.connect(self._add_row)
        btn_add_col.clicked.connect(self._add_col)
        btn_layout.addWidget(btn_add_row)
        btn_layout.addWidget(btn_add_col)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _add_row(self):
        self.table.insertRow(self.table.rowCount())
        self.changed.emit()

    def _add_col(self):
        col_name, ok = QInputDialog.getText(self, "Nouvelle colonne", "Nom de la colonne :")
        if ok and col_name:
            idx = self.table.columnCount()
            self.table.insertColumn(idx)
            self.table.setHorizontalHeaderItem(idx, QTableWidgetItem(col_name))
            self.changed.emit()

    def get_data(self) -> dict:
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


# =============================================================
# Éditeur de note
# =============================================================

class NoteEditor(QWidget):
    def __init__(self, note_service, intention_service, parent=None):
        super().__init__(parent)
        self.note_service      = note_service
        self.intention_service = intention_service
        self.current_note      = None
        self._block_widgets    = []   # list of (block_id, widget)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Header : titre + intention liée
        header = QHBoxLayout()
        self.lbl_title = QLabel("Sélectionnez une note")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #eee;")
        self.btn_rename = QPushButton("✎")
        self.btn_rename.setFixedSize(28, 28)
        self.btn_rename.setToolTip("Renommer la note")
        self.btn_rename.setStyleSheet("background: #2a2a3e; color: white; border-radius: 4px;")
        self.btn_rename.clicked.connect(self._rename_note)
        header.addWidget(self.lbl_title)
        header.addStretch()
        header.addWidget(self.btn_rename)
        layout.addLayout(header)

        # Intention liée
        intention_row = QHBoxLayout()
        self.lbl_intention = QLabel("Intention liée : aucune")
        self.lbl_intention.setStyleSheet("color: #aaa; font-size: 11px;")
        self.btn_link   = QPushButton("🔗 Lier à une intention")
        self.btn_unlink = QPushButton("✕ Délier")
        self.btn_link.setStyleSheet("""
            QPushButton { background: #2a2a3e; color: #4A90D9;
                          border: 1px solid #4A90D9; border-radius: 4px; padding: 2px 8px; }
            QPushButton:hover { background: #3a3a5c; }
        """)
        self.btn_unlink.setStyleSheet("""
            QPushButton { background: #2a2a3e; color: #cc4444;
                          border: 1px solid #cc4444; border-radius: 4px; padding: 2px 8px; }
            QPushButton:hover { background: #3a2020; }
        """)
        self.btn_link.clicked.connect(self._link_intention)
        self.btn_unlink.clicked.connect(self._unlink_intention)
        intention_row.addWidget(self.lbl_intention)
        intention_row.addStretch()
        intention_row.addWidget(self.btn_link)
        intention_row.addWidget(self.btn_unlink)
        layout.addLayout(intention_row)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #444;")
        layout.addWidget(sep)

        # Zone scrollable des blocs
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.blocks_container = QWidget()
        self.blocks_layout    = QVBoxLayout(self.blocks_container)
        self.blocks_layout.setSpacing(8)
        self.blocks_layout.addStretch()
        self.scroll.setWidget(self.blocks_container)
        layout.addWidget(self.scroll, stretch=1)

        # Barre d'ajout de blocs
        add_bar = QHBoxLayout()
        lbl = QLabel("Ajouter :")
        lbl.setStyleSheet("color: #aaa;")
        add_bar.addWidget(lbl)

        for label, btype in [
            ("Titre",      BlockType.TITLE.value),
            ("Texte",      BlockType.TEXT.value),
            ("Checklist",  BlockType.CHECKLIST.value),
            ("Tableau",    BlockType.TABLE.value),
        ]:
            btn = QPushButton(f"+ {label}")
            btn.setStyleSheet("""
                QPushButton { background: #2a2a3e; color: #ccc;
                              border: 1px solid #444; border-radius: 4px; padding: 4px 10px; }
                QPushButton:hover { background: #3a3a5c; }
            """)
            btn.clicked.connect(lambda _, t=btype: self._add_block(t))
            add_bar.addWidget(btn)

        add_bar.addStretch()
        layout.addLayout(add_bar)

        # Bouton sauvegarde
        self.btn_save = QPushButton("💾  Sauvegarder")
        self.btn_save.setStyleSheet("""
            QPushButton { background: #4A90D9; color: white; font-weight: bold;
                          border-radius: 6px; padding: 8px; }
            QPushButton:hover { background: #357abd; }
        """)
        self.btn_save.clicked.connect(self._save_note)
        layout.addWidget(self.btn_save)

        self._set_editor_enabled(False)

    def _set_editor_enabled(self, enabled: bool):
        self.btn_rename.setEnabled(enabled)
        self.btn_link.setEnabled(enabled)
        self.btn_unlink.setEnabled(enabled)
        self.btn_save.setEnabled(enabled)
        self.scroll.setEnabled(enabled)

    def load_note(self, note):
        self.current_note   = note
        self._block_widgets = []
        self.lbl_title.setText(note.title)
        self._set_editor_enabled(True)

        # Intention liée
        if note.intention_id:
            intentions = self.intention_service.get_all_intentions()
            intention  = next((i for i in intentions if i.id == note.intention_id), None)
            self.lbl_intention.setText(f"Intention liée : {intention.title}" if intention else "Intention liée : aucune")
        else:
            self.lbl_intention.setText("Intention liée : aucune")

        # Vide les blocs
        while self.blocks_layout.count() > 1:
            item = self.blocks_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Recharge les blocs
        for block in note.blocks:
            self._insert_block_widget(block.get_id(), block.get_type(), block.get_data())

    def _insert_block_widget(self, block_id: str, block_type: str, data: dict):
        container = QFrame()
        container.setStyleSheet("""
            QFrame { background: #2a2a3e; border-radius: 6px; border: 1px solid #3a3a5c; }
        """)
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(8, 8, 8, 8)
        c_layout.setSpacing(4)

        # Header du bloc : type + bouton supprimer + boutons ordre
        h = QHBoxLayout()
        type_icons = {
            BlockType.TITLE.value:     "📝 Titre",
            BlockType.TEXT.value:      "✏️ Texte",
            BlockType.CHECKLIST.value: "☑️ Checklist",
            BlockType.TABLE.value:     "📊 Tableau",
        }
        lbl_type = QLabel(type_icons.get(block_type, block_type))
        lbl_type.setStyleSheet("color: #888; font-size: 10px;")

        btn_up  = QPushButton("▲")
        btn_dn  = QPushButton("▼")
        btn_del = QPushButton("✕")
        for b in [btn_up, btn_dn, btn_del]:
            b.setFixedSize(22, 22)
            b.setStyleSheet("background: #1e1e2e; color: #ccc; border-radius: 3px; font-size: 10px;")

        btn_del.setStyleSheet("background: #1e1e2e; color: #cc4444; border-radius: 3px; font-size: 10px;")

        h.addWidget(lbl_type)
        h.addStretch()
        h.addWidget(btn_up)
        h.addWidget(btn_dn)
        h.addWidget(btn_del)
        c_layout.addLayout(h)

        # Widget du bloc
        widget_map = {
            BlockType.TITLE.value:     TitleBlockWidget,
            BlockType.TEXT.value:      TextBlockWidget,
            BlockType.CHECKLIST.value: ChecklistBlockWidget,
            BlockType.TABLE.value:     TableBlockWidget,
        }
        WidgetClass = widget_map.get(block_type)
        if not WidgetClass:
            return

        block_widget = WidgetClass(block_id=block_id, data=data)
        block_widget.setStyleSheet("QFrame { border: none; background: transparent; }")
        c_layout.addWidget(block_widget)

        self._block_widgets.append((block_id, block_widget, container))

        # Connexions ordre et suppression
        btn_up.clicked.connect(lambda: self._move_block(block_id, -1))
        btn_dn.clicked.connect(lambda: self._move_block(block_id, +1))
        btn_del.clicked.connect(lambda: self._delete_block(block_id))

        insert_pos = self.blocks_layout.count() - 1
        self.blocks_layout.insertWidget(insert_pos, container)

    def _move_block(self, block_id: str, direction: int):
        if not self.current_note:
            return
        ids = [bid for bid, _, __ in self._block_widgets]
        if block_id not in ids:
            return
        idx     = ids.index(block_id)
        new_idx = idx + direction
        if 0 <= new_idx < len(ids):
            self._save_note(silent=True)
            self.note_service.reorder_blocks(self.current_note.id, idx, new_idx)
            self.current_note = self.note_service.get_note(self.current_note.id)
            self.load_note(self.current_note)

    def _delete_block(self, block_id: str):
        if not self.current_note:
            return
        confirm = QMessageBox.question(
            self, "Supprimer", "Supprimer ce bloc ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self._save_note(silent=True)
            self.note_service.remove_block(self.current_note.id, block_id)
            self.current_note = self.note_service.get_note(self.current_note.id)
            self.load_note(self.current_note)

    def _add_block(self, block_type: str):
        if not self.current_note:
            return
        defaults = {
            BlockType.TITLE.value:     {"text": "",    "level": 1},
            BlockType.TEXT.value:      {"content": ""},
            BlockType.CHECKLIST.value: {"items": []},
            BlockType.TABLE.value:     {"headers": ["Colonne 1"], "rows": []},
        }
        self.note_service.add_block(
            self.current_note.id, block_type, **defaults.get(block_type, {})
        )
        self.current_note = self.note_service.get_note(self.current_note.id)
        self.load_note(self.current_note)

    def _save_note(self, silent=False):
        if not self.current_note:
            return
        for block_id, widget, _ in self._block_widgets:
            data = widget.get_data()
            self.note_service.update_block(self.current_note.id, block_id, data)
        if not silent:
            QMessageBox.information(self, "Sauvegarde", "Note sauvegardée ✓")

    def _rename_note(self):
        if not self.current_note:
            return
        new_title, ok = QInputDialog.getText(
            self, "Renommer", "Nouveau titre :", text=self.current_note.title
        )
        if ok and new_title:
            self.note_service.rename_note(self.current_note.id, new_title)
            self.current_note = self.note_service.get_note(self.current_note.id)
            self.lbl_title.setText(self.current_note.title)

    def _link_intention(self):
        if not self.current_note:
            return
        intentions = self.intention_service.get_all_intentions()
        if not intentions:
            QMessageBox.information(self, "Info", "Aucune intention disponible.")
            return
        choices = [f"{i.title}" for i in intentions]
        choice, ok = QInputDialog.getItem(
            self, "Lier à une intention", "Choisir une intention :", choices, 0, False
        )
        if ok and choice:
            intention = next(i for i in intentions if i.title == choice)
            self.note_service.attach_to_intention(self.current_note.id, intention.id)
            self.current_note = self.note_service.get_note(self.current_note.id)
            self.lbl_intention.setText(f"Intention liée : {intention.title}")

    def _unlink_intention(self):
        if not self.current_note or not self.current_note.intention_id:
            return
        self.note_service.detach_from_intention(self.current_note.id)
        self.current_note = self.note_service.get_note(self.current_note.id)
        self.lbl_intention.setText("Intention liée : aucune")


# =============================================================
# NotesPage
# =============================================================

class NotesPage(QWidget):
    def __init__(self, note_service=None, intention_service=None, parent=None):
        super().__init__(parent)
        self.note_service      = note_service
        self.intention_service = intention_service
        self._init_ui()
        self._subscribe()
        self._load_notes()

    def _init_ui(self):
        self.setStyleSheet("background-color: #13131f;")
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- Panneau gauche : liste des notes ----
        left_panel = QFrame()
        left_panel.setFixedWidth(260)
        left_panel.setStyleSheet("""
            QFrame { background: #1e1e2e; border-right: 1px solid #2a2a3e; }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 16, 12, 12)
        left_layout.setSpacing(8)

        # Titre panneau
        lbl_notes = QLabel("Notes")
        lbl_notes.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(lbl_notes)

        # Filtre par intention
        self.filter_combo = QComboBox()
        self.filter_combo.setStyleSheet("""
            QComboBox { background: #2a2a3e; color: #ccc; border: 1px solid #444;
                        border-radius: 4px; padding: 4px; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background: #2a2a3e; color: white; }
        """)
        self.filter_combo.addItem("Toutes les notes", None)
        self.filter_combo.currentIndexChanged.connect(self._on_filter_changed)
        left_layout.addWidget(self.filter_combo)

        # Barre de recherche
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Rechercher...")
        self.search_bar.setStyleSheet("""
            QLineEdit { background: #2a2a3e; color: white; border: 1px solid #444;
                        border-radius: 4px; padding: 6px; }
        """)
        self.search_bar.textChanged.connect(self._on_search)
        left_layout.addWidget(self.search_bar)

        # Liste
        self.note_list = QListWidget()
        self.note_list.setStyleSheet("""
            QListWidget { background: transparent; border: none; color: white; }
            QListWidget::item { padding: 10px 8px; border-radius: 6px; margin: 2px 0; }
            QListWidget::item:selected { background: #3a3a5c; }
            QListWidget::item:hover { background: #2a2a4a; }
        """)
        self.note_list.currentItemChanged.connect(self._on_note_selected)
        left_layout.addWidget(self.note_list, stretch=1)

        # Boutons bas du panneau
        btn_new = QPushButton("+ Nouvelle note")
        btn_new.setStyleSheet("""
            QPushButton { background: #4A90D9; color: white; font-weight: bold;
                          border-radius: 6px; padding: 8px; }
            QPushButton:hover { background: #357abd; }
        """)
        btn_new.clicked.connect(self._create_note)
        left_layout.addWidget(btn_new)

        btn_delete = QPushButton("🗑 Supprimer la note")
        btn_delete.setStyleSheet("""
            QPushButton { background: #2a2a3e; color: #cc4444;
                          border: 1px solid #cc4444; border-radius: 6px; padding: 6px; }
            QPushButton:hover { background: #3a2020; }
        """)
        btn_delete.clicked.connect(self._delete_note)
        left_layout.addWidget(btn_delete)

        # ---- Panneau droit : éditeur ----
        self.editor = NoteEditor(
            note_service=self.note_service,
            intention_service=self.intention_service
        )
        self.editor.setStyleSheet("background: #13131f;")

        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.editor)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background: #2a2a3e; }")

        main_layout.addWidget(splitter)

    def _subscribe(self):
        if self.note_service:
            self.note_service.subscribe("note_created", self._on_note_changed)
            self.note_service.subscribe("note_updated", self._on_note_updated)
            self.note_service.subscribe("note_deleted", self._on_note_changed)
            self.note_service.subscribe("note_linked",  self._on_note_changed)

    def _on_note_changed(self, payload):
        self._load_notes()

    def _on_note_updated(self, note):
        # Met à jour le titre dans la liste sans tout recharger
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if item.data(Qt.UserRole) == note.id:
                suffix = f" 🔗" if note.intention_id else ""
                item.setText(f"{note.title}{suffix}")
                break

    def _load_notes(self):
        self.note_list.clear()
        if not self.note_service:
            return

        # Recharge le filtre par intention
        current_filter = self.filter_combo.currentData()
        self.filter_combo.blockSignals(True)
        self.filter_combo.clear()
        self.filter_combo.addItem("Toutes les notes", None)
        if self.intention_service:
            for intention in self.intention_service.get_all_intentions():
                self.filter_combo.addItem(f"📌 {intention.title}", intention.id)
        self.filter_combo.blockSignals(False)

        # Restaure le filtre si possible
        for i in range(self.filter_combo.count()):
            if self.filter_combo.itemData(i) == current_filter:
                self.filter_combo.setCurrentIndex(i)
                break

        self._apply_filter()

    def _apply_filter(self):
        self.note_list.clear()
        if not self.note_service:
            return

        intention_id = self.filter_combo.currentData()
        if intention_id:
            notes = self.note_service.get_notes_for_intention(intention_id)
        else:
            notes = self.note_service.get_notes_for_user("1")

        search = self.search_bar.text().strip().lower()
        for note in notes:
            if search and search not in note.title.lower():
                continue
            suffix = " 🔗" if note.intention_id else ""
            item   = QListWidgetItem(f"{note.title}{suffix}")
            item.setData(Qt.UserRole, note.id)
            if note.intention_id:
                item.setForeground(QColor("#4A90D9"))
            self.note_list.addItem(item)

    def _on_filter_changed(self, _):
        self._apply_filter()

    def _on_search(self, _):
        self._apply_filter()

    def _on_note_selected(self, item):
        if not item:
            return
        note_id = item.data(Qt.UserRole)
        note    = self.note_service.get_note(note_id)
        if note:
            self.editor.load_note(note)

    def _create_note(self):
        title, ok = QInputDialog.getText(self, "Nouvelle note", "Titre de la note :")
        if ok and title:
            self.note_service.create_note(owner_id="1", title=title)
            # self._load_notes()

    def _delete_note(self):
        item = self.note_list.currentItem()
        if not item:
            return
        note_id   = item.data(Qt.UserRole)
        note      = self.note_service.get_note(note_id)
        if not note:
            return
        confirm = QMessageBox.question(
            self, "Supprimer",
            f"Supprimer la note « {note.title} » ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.note_service.delete_note(note_id)
            self.editor.current_note = None
            self.editor.lbl_title.setText("Sélectionnez une note")
            self.editor._set_editor_enabled(False)