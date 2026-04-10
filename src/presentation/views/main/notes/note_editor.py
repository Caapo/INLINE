# INLINE/src/presentation/views/main/notes/note_editor.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QFrame, QScrollArea, QMessageBox, QInputDialog)
from PySide6.QtCore import Qt

from domain.enums.enums import BlockType
from presentation.views.main.notes.blocks.title_block_widget import TitleBlockWidget
from presentation.views.main.notes.blocks.text_block_widget import TextBlockWidget
from presentation.views.main.notes.blocks.checklist_block_widget import ChecklistBlockWidget
from presentation.views.main.notes.blocks.table_block_widget import TableBlockWidget


class NoteEditor(QWidget):
    """
    Éditeur de note principal.
    Affiche le contenu d'une note sous forme de blocs empilés.
    Permet d'ajouter, supprimer, réordonner les blocs,
    de renommer la note et de gérer le lien avec une intention.
    """

    def __init__(self, note_service, intention_service, parent=None):
        super().__init__(parent)
        self.note_service      = note_service
        self.intention_service = intention_service
        self.current_note      = None
        self._block_widgets    = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Header : titre + bouton renommer
        header = QHBoxLayout()
        self.lbl_title = QLabel("Sélectionnez une note")
        self.btn_rename = QPushButton("✎")
        self.btn_rename.setFixedSize(28, 28)
        self.btn_rename.setToolTip("Renommer la note")
        self.btn_rename.setStyleSheet(
            "background: #2a2a3e; color: white; border-radius: 4px;"
        )
        self.btn_rename.clicked.connect(self._rename_note)
        header.addWidget(self.lbl_title)
        header.addStretch()
        header.addWidget(self.btn_rename)
        layout.addLayout(header)

        # Intention liée
        intention_row = QHBoxLayout()
        self.lbl_intention = QLabel("Intention liée : aucune")
        self.btn_link      = QPushButton("🔗 Lier à une intention")
        self.btn_unlink    = QPushButton("✕ Délier")
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
        layout.addWidget(sep)

        # Zone scrollable des blocs
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.blocks_container = QWidget()
        self.blocks_layout    = QVBoxLayout(self.blocks_container)
        self.blocks_layout.setSpacing(8)
        self.blocks_layout.addStretch()
        self.scroll.setWidget(self.blocks_container)
        layout.addWidget(self.scroll, stretch=1)

        # Barre d'ajout de blocs
        add_bar = QHBoxLayout()
        add_bar.addWidget(QLabel("Ajouter :"))

        for label, btype in [
            ("Titre",     BlockType.TITLE.value),
            ("Texte",     BlockType.TEXT.value),
            ("Checklist", BlockType.CHECKLIST.value),
            ("Tableau",   BlockType.TABLE.value),
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
        self.btn_save.clicked.connect(self._save_note)
        layout.addWidget(self.btn_save)

        self._set_editor_enabled(False)

    def _set_editor_enabled(self, enabled: bool):
        """Active ou désactive les contrôles de l'éditeur."""
        self.btn_rename.setEnabled(enabled)
        self.btn_link.setEnabled(enabled)
        self.btn_unlink.setEnabled(enabled)
        self.btn_save.setEnabled(enabled)
        self.scroll.setEnabled(enabled)

    def load_note(self, note):
        """
        Charge une note dans l'éditeur.
        Reconstruit tous les blocs depuis les données du domaine.
        """
        self.current_note   = note
        self._block_widgets = []
        self.lbl_title.setText(note.title)
        self._set_editor_enabled(True)

        # Intention liée
        if note.intention_id:
            intentions = self.intention_service.get_all_intentions()
            intention  = next(
                (i for i in intentions if i.id == note.intention_id), None
            )
            self.lbl_intention.setText(
                f"Intention liée : {intention.title}"
                if intention else "Intention liée : aucune"
            )
        else:
            self.lbl_intention.setText("Intention liée : aucune")

        # Vide les blocs existants
        while self.blocks_layout.count() > 1:
            item = self.blocks_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Reconstruit les blocs
        for block in note.blocks:
            self._insert_block_widget(
                block.get_id(), block.get_type(), block.get_data()
            )

    def _insert_block_widget(self, block_id: str, block_type: str, data: dict):
        """
        Crée et insère un widget de bloc dans l'éditeur.
        Chaque bloc est encapsulé dans un container avec
        ses boutons de contrôle (ordre, suppression).
        """
        container = QFrame()
        container.setStyleSheet("""
            QFrame { background: #2a2a3e; border-radius: 6px; border: 1px solid #3a3a5c; }
        """)
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(8, 8, 8, 8)
        c_layout.setSpacing(4)

        # Header du bloc
        h = QHBoxLayout()
        type_icons = {
            BlockType.TITLE.value:     "📝 Titre",
            BlockType.TEXT.value:      "✏️ Texte",
            BlockType.CHECKLIST.value: "☑️ Checklist",
            BlockType.TABLE.value:     "📊 Tableau",
        }
        lbl_type = QLabel(type_icons.get(block_type, block_type))

        btn_up  = QPushButton("▲")
        btn_dn  = QPushButton("▼")
        btn_del = QPushButton("✕")
        for b in [btn_up, btn_dn, btn_del]:
            b.setFixedSize(22, 22)
        btn_del.setStyleSheet(
            "background: #1e1e2e; color: #cc4444; border-radius: 3px; font-size: 10px;"
        )

        h.addWidget(lbl_type)
        h.addStretch()
        h.addWidget(btn_up)
        h.addWidget(btn_dn)
        h.addWidget(btn_del)
        c_layout.addLayout(h)

        # Widget du bloc selon son type
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
        c_layout.addWidget(block_widget)

        self._block_widgets.append((block_id, block_widget, container))

        btn_up.clicked.connect(lambda: self._move_block(block_id, -1))
        btn_dn.clicked.connect(lambda: self._move_block(block_id, +1))
        btn_del.clicked.connect(lambda: self._delete_block(block_id))

        insert_pos = self.blocks_layout.count() - 1
        self.blocks_layout.insertWidget(insert_pos, container)

    def _move_block(self, block_id: str, direction: int):
        """
        Déplace un bloc vers le haut ou le bas.
        Sauvegarde silencieuse avant le réordonnancement.
        """
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
        """Supprime un bloc après confirmation."""
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
        """Ajoute un bloc du type donné à la note courante."""
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
        """
        Sauvegarde les données de tous les blocs via NoteService.
        silent=True supprime le message de confirmation.
        """
        if not self.current_note:
            return
        for block_id, widget, _ in self._block_widgets:
            self.note_service.update_block(
                self.current_note.id, block_id, widget.get_data()
            )
        if not silent:
            QMessageBox.information(self, "Sauvegarde", "Note sauvegardée ✓")

    def _rename_note(self):
        """Renomme la note courante via dialog."""
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
        """Lie la note courante à une intention choisie via dialog."""
        if not self.current_note:
            return
        intentions = self.intention_service.get_all_intentions()
        if not intentions:
            QMessageBox.information(self, "Info", "Aucune intention disponible.")
            return
        choice, ok = QInputDialog.getItem(
            self, "Lier à une intention", "Choisir une intention :",
            [i.title for i in intentions], 0, False
        )
        if ok and choice:
            intention = next(i for i in intentions if i.title == choice)
            self.note_service.attach_to_intention(self.current_note.id, intention.id)
            self.current_note = self.note_service.get_note(self.current_note.id)
            self.lbl_intention.setText(f"Intention liée : {intention.title}")

    def _unlink_intention(self):
        """Délie la note courante de son intention."""
        if not self.current_note or not self.current_note.intention_id:
            return
        self.note_service.detach_from_intention(self.current_note.id)
        self.current_note = self.note_service.get_note(self.current_note.id)
        self.lbl_intention.setText("Intention liée : aucune")