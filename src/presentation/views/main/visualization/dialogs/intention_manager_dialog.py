# INLINE/src/presentation/views/main/visualization/dialogs/intention_manager_dialog.py

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QInputDialog, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from datetime import datetime


class IntentionManagerDialog(QDialog):
    """
    Dialog de gestion des intentions depuis la page de visualisation.
    Permet de créer, renommer, supprimer une intention,
    de définir ou retirer le focus, et de planifier un événement
    pour l'intention sélectionnée.
    """

    def __init__(self, parent=None, intention_service=None, event_service=None,
                 current_env_id=None, current_day=None):
        super().__init__(parent)
        self.intention_service = intention_service
        self.event_service     = event_service
        self.current_env_id    = current_env_id
        self.current_day       = current_day or datetime.utcnow().date()

        self.setWindowTitle("Gestion des intentions")
        self.resize(480, 420)

        layout = QVBoxLayout(self)

        # Label focus actuel
        self.lbl_active = QLabel("★ Focus actuel : aucun")
        self.lbl_active.setStyleSheet("""
            background: #fffbe6;
            border: 1px solid #f0c040;
            border-radius: 4px;
            padding: 6px;
            font-weight: bold;
            color: #7a5c00;
        """)
        layout.addWidget(self.lbl_active)

        layout.addWidget(QLabel("<b>Intentions</b>"))
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_create_intention = QPushButton("+ Créer")
        self.btn_rename_intention = QPushButton("✎ Renommer")
        self.btn_delete_intention = QPushButton("✕ Supprimer")
        self.btn_toggle_focus     = QPushButton("★ Définir focus")
        btn_layout.addWidget(self.btn_create_intention)
        btn_layout.addWidget(self.btn_rename_intention)
        btn_layout.addWidget(self.btn_delete_intention)
        btn_layout.addWidget(self.btn_toggle_focus)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel(""))
        self.btn_create_event = QPushButton(
            "✦ Planifier l'intention sélectionnée → Créer un événement"
        )
        layout.addWidget(self.btn_create_event)

        self.btn_create_intention.clicked.connect(self._create_intention)
        self.btn_rename_intention.clicked.connect(self._rename_intention)
        self.btn_delete_intention.clicked.connect(self._delete_intention)
        self.btn_toggle_focus.clicked.connect(self._toggle_focus)
        self.btn_create_event.clicked.connect(self._create_event)
        self.list_widget.currentItemChanged.connect(
            lambda: self._update_focus_button()
        )

        self._load_intentions()

    def _load_intentions(self):
        """Recharge la liste des intentions et met à jour le label focus."""
        self.list_widget.clear()
        if not self.intention_service:
            return

        active_found = None
        for i in self.intention_service.get_all_intentions():
            if i.is_active:
                item = QListWidgetItem(f"★  {i.title}  [FOCUS]")
                item.setForeground(QColor(180, 130, 0))
                item.setBackground(QColor(255, 250, 220))
                active_found = i.title
            else:
                item = QListWidgetItem(f"   {i.title}")
            item.setData(Qt.UserRole,     i.id)
            item.setData(Qt.UserRole + 1, i.is_active)
            self.list_widget.addItem(item)

        self.lbl_active.setText(
            f"★ Focus actuel : {active_found}" if active_found
            else "★ Focus actuel : aucun"
        )
        self._update_focus_button()

    def _update_focus_button(self):
        """Met à jour le texte du bouton focus selon l'item sélectionné."""
        item = self.list_widget.currentItem()
        if not item:
            self.btn_toggle_focus.setText("★ Définir focus")
            return
        self.btn_toggle_focus.setText(
            "☆ Retirer le focus"
            if item.data(Qt.UserRole + 1)
            else "★ Définir comme focus"
        )

    def _selected_id(self):
        """Retourne l'id de l'intention sélectionnée ou None."""
        item = self.list_widget.currentItem()
        return item.data(Qt.UserRole) if item else None

    def _selected_title(self):
        """Retourne le titre nettoyé de l'intention sélectionnée."""
        item = self.list_widget.currentItem()
        if not item:
            return None
        return item.text().strip().replace("★  ", "").replace("  [FOCUS]", "").strip()

    def _create_intention(self):
        """Crée une nouvelle intention et recharge la liste."""
        title, ok = QInputDialog.getText(self, "Nouvelle intention", "Titre :")
        if ok and title:
            self.intention_service.create_intention(
                user_id="1", title=title, category="Physique"
            )
            self._load_intentions()

    def _rename_intention(self):
        """Renomme l'intention sélectionnée."""
        intention_id = self._selected_id()
        if not intention_id:
            return
        new_title, ok = QInputDialog.getText(
            self, "Renommer", "Nouveau titre :", text=self._selected_title()
        )
        if ok and new_title:
            self.intention_service.rename_intention(intention_id, new_title)
            self._load_intentions()

    def _delete_intention(self):
        """Supprime l'intention sélectionnée après confirmation."""
        intention_id = self._selected_id()
        if not intention_id:
            return
        confirm = QMessageBox.question(
            self, "Supprimer",
            f"Supprimer « {self._selected_title()} » ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.intention_service.delete_intention(intention_id)
            self._load_intentions()

    def _toggle_focus(self):
        """
        Active ou désactive le focus de l'intention sélectionnée.
        Notifie VisualizationPage pour mettre à jour le label focus
        et la surbrillance de la timeline.
        """
        intention_id = self._selected_id()
        if not intention_id:
            return
        item      = self.list_widget.currentItem()
        is_active = item.data(Qt.UserRole + 1)

        if is_active:
            self.intention_service.deactivate_intention(intention_id)
        else:
            self.intention_service.activate_intention(intention_id)

        self._load_intentions()

        if self.parent():
            self.parent()._refresh_focus()

    def _create_event(self):
        """
        Crée un événement pour l'intention sélectionnée.
        Demande l'heure de début et la durée via des dialogs.
        """
        intention_id = self._selected_id()
        title        = self._selected_title()
        if not intention_id:
            return

        start_hour, ok1 = QInputDialog.getDouble(
            self, "Début", f"Heure de début pour « {title} »", 8.0, 0.0, 23.99, 2
        )
        duration_minutes, ok2 = QInputDialog.getInt(
            self, "Durée", f"Durée (minutes) pour « {title} »", 60, 1, 1440
        )
        if not (ok1 and ok2):
            return

        start_time = datetime(
            year=self.current_day.year,
            month=self.current_day.month,
            day=self.current_day.day,
            hour=int(start_hour),
            minute=int((start_hour % 1) * 60),
            second=0,
            microsecond=0
        )

        if self.event_service and self.current_env_id:
            self.event_service.create_event(
                intention_id=intention_id,
                environment_id=self.current_env_id,
                start_time=start_time,
                duration=duration_minutes
            )