# === INLINE/src/presentation/views/main/visualization/object_widget.py ===

from PySide6.QtWidgets import QFrame, QLabel, QMenu
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QColor


class ObjectWidget(QFrame):
    """
    Widget représentant un objet interactif dans la visualisation.
    Supporte le drag & drop avec contrainte dans les limites du parent,
    et affiche un menu contextuel au clic pour créer une intention,
    renommer ou supprimer l'objet.

    Signaux:
        request_intention (str): Émis quand l'utilisateur veut créer une intention.
        request_rename (str): Émis quand l'utilisateur veut renommer l'objet.
        request_delete (str): Émis quand l'utilisateur veut supprimer l'objet.
        moved (str, int, int): Émis après un drag avec obj_id, x, y.
    """

    request_intention = Signal(str)
    request_rename    = Signal(str)
    request_delete    = Signal(str)
    moved             = Signal(str, int, int)

    def __init__(self, name: str, width=100, height=60, parent=None):
        super().__init__(parent)
        self.obj_id   = None
        self.obj_name = name

        self.setFixedSize(width, height)
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("""
            QFrame {
                background-color: #4A90D9;
                border-radius: 8px;
                border: 2px solid #2c5f8a;
            }
        """)

        self.label = QLabel(name, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, width, height)
        self.label.setStyleSheet(
            "color: white; font-weight: bold; font-size: 11px; background: transparent;"
        )
        self.label.setWordWrap(True)

        self.position        = (0, 0)
        self._drag_active    = False
        self._drag_offset    = QPoint(0, 0)
        self._drag_threshold = 5

    def update_name(self, new_name: str) -> None:
        """Met à jour le nom affiché sur le widget."""
        self.obj_name = new_name
        self.label.setText(new_name)

    def mousePressEvent(self, event):
        """Initialise le drag au clic gauche."""
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_offset = event.position().toPoint()
            self._start_pos   = self.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Déplace le widget en contraignant sa position dans les limites du parent."""
        if self._drag_active and self.parent():
            new_pos = self.mapToParent(event.position().toPoint() - self._drag_offset)
            new_pos = self._clamp_to_parent(new_pos)
            self.move(new_pos)
            self.position = (new_pos.x(), new_pos.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Au relâchement du clic :
        - si déplacement court → menu contextuel
        - si déplacement long → émet moved pour persistance
        """
        if event.button() == Qt.LeftButton:
            self._drag_active = False
            distance = (self.pos() - self._start_pos).manhattanLength()
            self.position = (self.x(), self.y())
            if distance <= self._drag_threshold:
                self._show_context_menu(event.globalPosition().toPoint())
            else:
                if self.obj_id:
                    self.moved.emit(self.obj_id, self.x(), self.y())
        super().mouseReleaseEvent(event)

    def _clamp_to_parent(self, pos):
        """Contraint la position dans les limites du widget parent."""
        if not self.parent():
            return pos
        parent_rect = self.parent().rect()
        x = max(0, min(pos.x(), parent_rect.width()  - self.width()))
        y = max(0, min(pos.y(), parent_rect.height() - self.height()))
        from PySide6.QtCore import QPoint
        return QPoint(x, y)

    def _show_context_menu(self, global_pos):
        """Affiche le menu contextuel avec les actions disponibles sur l'objet."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e2e;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 4px;
                color: white;
                font-size: 12px;
            }
            QMenu::item { padding: 8px 24px; border-radius: 4px; }
            QMenu::item:selected { background-color: #3a3a5c; }
            QMenu::item:disabled { color: #aaa; font-size: 11px; padding: 4px 24px; }
            QMenu::separator { height: 1px; background: #444; margin: 3px 8px; }
        """)

        title = menu.addAction(f"  {self.obj_name}")
        title.setEnabled(False)
        menu.addSeparator()
        action_intention = menu.addAction("✦   Créer une intention")
        action_rename    = menu.addAction("✎   Renommer")
        menu.addSeparator()
        action_delete    = menu.addAction("✕   Supprimer l'objet")

        chosen = menu.exec(global_pos)
        if chosen == action_intention:
            self.request_intention.emit(self.obj_id)
        elif chosen == action_rename:
            self.request_rename.emit(self.obj_id)
        elif chosen == action_delete:
            self.request_delete.emit(self.obj_id)