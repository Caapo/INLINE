# INLINE/src/presentation/views/main/visualization/dialogs/event_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QInputDialog, QMessageBox
)
from datetime import datetime


class EventDialog(QDialog):
    """
    Dialog contextuel d'un événement cliqué sur la timeline.
    Affiche les informations de l'event et propose les actions
    disponibles selon son statut : compléter, reprogrammer,
    annuler ou supprimer.
    """

    def __init__(self, parent=None, event_data=None, event_service=None):
        super().__init__(parent)
        self.event_data    = event_data
        self.event_service = event_service

        self.setWindowTitle(f"Événement — {event_data.get('name', '')}")
        self.resize(320, 200)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{event_data.get('name', '')}</b>"))
        layout.addWidget(QLabel(f"Début : {event_data.get('start_time', '')}"))
        layout.addWidget(QLabel(f"Durée : {event_data.get('duration', '')} min"))
        layout.addWidget(QLabel(f"Statut : {event_data.get('status', '')}"))
        layout.addWidget(QLabel(""))

        status = event_data.get("status", "planned")

        if status == "planned":
            btn_complete = QPushButton("✔   Marquer comme complété")
            btn_complete.clicked.connect(self._complete)
            layout.addWidget(btn_complete)

            btn_reschedule = QPushButton("🕐   Reprogrammer")
            btn_reschedule.clicked.connect(self._reschedule)
            layout.addWidget(btn_reschedule)

            btn_cancel = QPushButton("✕   Annuler l'événement")
            btn_cancel.clicked.connect(self._cancel)
            layout.addWidget(btn_cancel)

        btn_delete = QPushButton("🗑   Supprimer l'événement")
        btn_delete.clicked.connect(self._delete)
        layout.addWidget(btn_delete)

    def _complete(self):
        """Marque l'event comme complété via EventService."""
        self.event_service.complete_event(self.event_data["id"])
        self.accept()

    def _reschedule(self):
        """
        Reprogramme l'event avec une nouvelle heure et durée.
        Reconstruit le datetime en conservant le jour d'origine.
        """
        start_str          = self.event_data.get("start_time", "08:00")
        h, m               = map(int, start_str.split(":"))
        current_hour_float = h + m / 60.0

        new_hour, ok1 = QInputDialog.getDouble(
            self, "Reprogrammer", "Nouvelle heure de début :",
            current_hour_float, 0.0, 23.99, 2
        )
        new_duration, ok2 = QInputDialog.getInt(
            self, "Reprogrammer", "Nouvelle durée (minutes) :",
            self.event_data.get("duration", 60), 1, 1440
        )
        if not (ok1 and ok2):
            return

        original_dt = datetime.fromisoformat(self.event_data["start_time_full"])
        new_start   = original_dt.replace(
            hour=int(new_hour),
            minute=int((new_hour % 1) * 60),
            second=0,
            microsecond=0
        )

        self.event_service.update_event_time(
            event_id=self.event_data["id"],
            start_time=new_start,
            duration=new_duration
        )
        self.accept()

    def _cancel(self):
        """Annule l'event via EventService."""
        self.event_service.cancel_event(self.event_data["id"])
        self.accept()

    def _delete(self):
        """Supprime définitivement l'event après confirmation."""
        confirm = QMessageBox.question(
            self, "Supprimer",
            "Supprimer définitivement cet événement ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.event_service.delete_event(self.event_data["id"])
            self.accept()