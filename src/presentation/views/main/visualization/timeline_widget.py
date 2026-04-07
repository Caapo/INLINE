# === INLINE/src/presentation/views/main/visualization/timeline_widget.py ===
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QPen


class TimelineWidget(QWidget):
    """
    Widget de visualisation temporelle des événements de la journée.
    Affiche les events sous forme de blocs colorés sur une grille horaire.
    Supporte la surbrillance de l'intention active (focus).
    Émet event_clicked au clic sur un event pour ouvrir EventDialog.

    Signaux:
        event_clicked (str): Émis avec l'id de l'event cliqué.
    """

    event_clicked = Signal(str)

    def __init__(self, parent=None, hours_range=(0, 23)):
        super().__init__(parent)
        self.hours_range         = hours_range
        self.events              = []
        self.active_intention_id = None
        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMouseTracking(True)

    def load_events(self, events) -> None:
        """Charge la liste des events et redessine le widget."""
        self.events = events
        self.update()

    def set_active_intention(self, intention_id) -> None:
        """
        Définit l'intention active pour la surbrillance.
        Appelé par VisualizationPage quand le focus change.
        """
        self.active_intention_id = intention_id
        self.update()

    def _event_rect(self, ev, hour_width, start):
        """Calcule le rectangle d'affichage d'un event."""
        start_x = (ev["start_hour"] - start) * hour_width
        w       = max(ev["duration_hour"] * hour_width, 4)
        y       = 25 + ev.get("_row", 0) * 28
        return int(start_x), int(y), int(w), 20

    def paintEvent(self, event):
        """
        Dessine la grille horaire et les events.
        Les events liés à l'intention active sont affichés
        avec un fond doré et un badge ★ FOCUS.
        Les events normaux sont colorés selon leur statut :
            - planned   → bleu
            - completed → vert
            - cancelled → rouge
        """
        painter    = QPainter(self)
        rect       = self.rect()
        width      = rect.width()
        height     = rect.height()
        painter.fillRect(rect, QColor(240, 240, 245))

        start, end = self.hours_range
        num_hours  = end - start + 1
        hour_width = width / num_hours

        # Calcul des rows pour éviter les chevauchements
        for ev in self.events:
            ev["_row"] = 0
        for i, ev in enumerate(self.events):
            for j in range(i):
                other = self.events[j]
                if abs(ev["start_hour"] - other["start_hour"]) < ev["duration_hour"]:
                    ev["_row"] = max(ev["_row"], other.get("_row", 0) + 1)

        # Grille horaire
        painter.setPen(QPen(QColor(200, 200, 200)))
        for i in range(num_hours):
            x = i * hour_width
            painter.drawLine(int(x), 0, int(x), height)
            painter.drawText(int(x) + 2, 12, f"{start + i}h")

        # Events
        for ev in self.events:
            x, y, w, h = self._event_rect(ev, hour_width, start)
            is_focus    = (
                self.active_intention_id is not None
                and ev.get("intention_id") == self.active_intention_id
            )

            if is_focus:
                painter.setBrush(QColor(255, 200, 50, 230))
                painter.setPen(QPen(QColor(180, 130, 0), 2))
                painter.drawRoundedRect(x, y - 4, w, h + 8, 5, 5)
                painter.setPen(QPen(QColor(120, 80, 0)))
                small_font = painter.font()
                small_font.setBold(True)
                painter.setFont(small_font)
                painter.drawText(x + 4, y + 8,  "★ FOCUS")
                painter.drawText(x + 4, y + 20, ev["name"])
            else:
                color = {
                    "planned":   QColor(100, 150, 220),
                    "completed": QColor(80,  180, 120),
                    "cancelled": QColor(200, 100, 100),
                }.get(ev.get("status", "planned"), QColor(150, 150, 150))

                painter.setBrush(color)
                painter.setPen(QPen(color.darker(130)))
                painter.drawRoundedRect(x, y, w, h, 4, 4)
                painter.setPen(QPen(Qt.white))
                painter.drawText(x + 4, y + 14, ev["name"])

    def mousePressEvent(self, event):
        """Détecte le clic sur un event et émet event_clicked avec son id."""
        if event.button() == Qt.LeftButton:
            start, end = self.hours_range
            hour_width = self.width() / (end - start + 1)
            for ev in self.events:
                x, y, w, h = self._event_rect(ev, hour_width, start)
                if (x <= event.position().x() <= x + w and
                        y <= event.position().y() <= y + h):
                    self.event_clicked.emit(ev["id"])
                    return
        super().mousePressEvent(event)