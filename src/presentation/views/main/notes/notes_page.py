# ======= INLINE/src/presentation/views/main/notes/notes_page.py =======


from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QSplitter, QFrame,
    QInputDialog, QMessageBox, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from presentation.views.main.notes.note_editor import NoteEditor


class NotesPage(QWidget):
    """
    Page principale de gestion des notes.
    Affiche la liste des notes à gauche et l'éditeur à droite.
    S'abonne aux événements du NoteService via Observer
    pour se mettre à jour automatiquement.
    """

    def __init__(self, note_service=None, intention_service=None, parent=None):
        super().__init__(parent)
        self.note_service      = note_service
        self.intention_service = intention_service
        self._init_ui()
        self._subscribe()
        self._load_notes()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- Panneau gauche ----
        left_panel = QFrame()
        left_panel.setFixedWidth(260)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 16, 12, 12)
        left_layout.setSpacing(8)

        left_layout.addWidget(QLabel("Notes"))

        # Filtre par intention
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Toutes les notes", None)
        self.filter_combo.currentIndexChanged.connect(self._on_filter_changed)
        left_layout.addWidget(self.filter_combo)

        # Barre de recherche
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Rechercher...")
        self.search_bar.textChanged.connect(self._on_search)
        left_layout.addWidget(self.search_bar)

        # Liste des notes
        self.note_list = QListWidget()
        self.note_list.currentItemChanged.connect(self._on_note_selected)
        left_layout.addWidget(self.note_list, stretch=1)

        btn_new = QPushButton("+ Nouvelle note")
        btn_new.clicked.connect(self._create_note)
        left_layout.addWidget(btn_new)

        btn_delete = QPushButton("🗑 Supprimer la note")
        btn_delete.clicked.connect(self._delete_note)
        left_layout.addWidget(btn_delete)

        # ---- Panneau droit : éditeur ----
        self.editor = NoteEditor(
            note_service=self.note_service,
            intention_service=self.intention_service
        )

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.editor)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setHandleWidth(1)
        main_layout.addWidget(splitter)

    def _subscribe(self):
        """Abonne la page aux événements du NoteService via Observer."""
        if self.note_service:
            self.note_service.subscribe("note_created", self._on_note_changed)
            self.note_service.subscribe("note_updated", self._on_note_updated)
            self.note_service.subscribe("note_deleted", self._on_note_changed)
            self.note_service.subscribe("note_linked",  self._on_note_changed)

    def _on_note_changed(self, payload):
        """Recharge la liste complète lors d'une création, suppression ou lien."""
        self._load_notes()

    def _on_note_updated(self, note):
        """Met à jour uniquement le titre de la note modifiée dans la liste."""
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if item.data(Qt.UserRole) == note.id:
                suffix = " 🔗" if note.intention_id else ""
                item.setText(f"{note.title}{suffix}")
                break

    def _load_notes(self):
        """Recharge la liste des notes et le filtre par intention."""
        self.note_list.clear()
        if not self.note_service:
            return

        current_filter = self.filter_combo.currentData()
        self.filter_combo.blockSignals(True)
        self.filter_combo.clear()
        self.filter_combo.addItem("Toutes les notes", None)
        if self.intention_service:
            for intention in self.intention_service.get_all_intentions():
                self.filter_combo.addItem(f"📌 {intention.title}", intention.id)
        self.filter_combo.blockSignals(False)

        for i in range(self.filter_combo.count()):
            if self.filter_combo.itemData(i) == current_filter:
                self.filter_combo.setCurrentIndex(i)
                break

        self._apply_filter()

    def _apply_filter(self):
        """Filtre et affiche les notes selon l'intention sélectionnée et la recherche."""
        self.note_list.clear()
        if not self.note_service:
            return

        intention_id = self.filter_combo.currentData()
        notes = (
            self.note_service.get_notes_for_intention(intention_id)
            if intention_id
            else self.note_service.get_notes_for_user("1")
        )

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
        """Applique le filtre lors du changement de l'intention sélectionnée."""
        self._apply_filter()

    def _on_search(self, _):
        """Applique le filtre lors de la saisie dans la barre de recherche."""
        self._apply_filter()

    def _on_note_selected(self, item):
        """Charge la note sélectionnée dans l'éditeur."""
        if not item:
            return
        note = self.note_service.get_note(item.data(Qt.UserRole))
        if note:
            self.editor.load_note(note)

    def _create_note(self):
        """Crée une nouvelle note via dialog."""
        title, ok = QInputDialog.getText(self, "Nouvelle note", "Titre de la note :")
        if ok and title:
            self.note_service.create_note(owner_id="1", title=title)

    def _delete_note(self):
        """Supprime la note sélectionnée après confirmation."""
        item = self.note_list.currentItem()
        if not item:
            return
        note_id = item.data(Qt.UserRole)
        note    = self.note_service.get_note(note_id)
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