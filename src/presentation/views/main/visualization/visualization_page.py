#INLINE/src/presentation/views/main/visualization/visualization_page.py


from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen


#Objet interactif cliquable et déplaçable
class ObjectWidget(QFrame):

    def __init__(self, name: str, width=80, height=50, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedSize(width, height)

        #Label pour le nom de l'objet
        self.label = QLabel(name, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, width, height)
        self.label.setStyleSheet("font-weight: bold; color: blue;")

        self._drag_active = False
        self._drag_offset = QPoint(0, 0)

    #Drag
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_offset = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_active:
            new_pos = self.mapToParent(event.position().toPoint() - self._drag_offset)
            self.move(new_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_active = False
        super().mouseReleaseEvent(event)


# ------------------ EnvironmentSwitcher ------------------
#Permet de naviguer entre les environnements
class EnvironmentSwitcher(QWidget):

    environment_changed = Signal(str)

    def __init__(self, environments=None, parent=None):
        super().__init__(parent)
        self.environments = environments or ["Default", "Env2", "Env3"]
        self.current_index = 0

        layout = QHBoxLayout(self)
        self.prev_btn = QPushButton("←")
        self.next_btn = QPushButton("→")
        self.label = QLabel(self.environments[self.current_index])
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.prev_btn)
        layout.addWidget(self.label)
        layout.addWidget(self.next_btn)

        self.prev_btn.clicked.connect(self.prev_env)
        self.next_btn.clicked.connect(self.next_env)

    def prev_env(self):
        self.current_index = (self.current_index - 1) % len(self.environments)
        self._update_label()

    def next_env(self):
        self.current_index = (self.current_index + 1) % len(self.environments)
        self._update_label()

    def _update_label(self):
        env = self.environments[self.current_index]
        self.label.setText(env)
        self.environment_changed.emit(env)


# ------------------ TimelineWidget ------------------
#Timeline horizontale
class TimelineWidget(QWidget):
   
    def __init__(self, parent=None, hours_range=(8, 20)):
        super().__init__(parent)
        self.hours_range = hours_range
        self.events = []
        self.setMinimumHeight(80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def load_events(self, events):
        self.events = events
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        width = rect.width()
        height = rect.height()

        painter.fillRect(rect, QColor(230, 230, 230))

        #Repères horaires
        start, end = self.hours_range
        num_hours = end - start + 1
        hour_width = width / num_hours

        pen = QPen(QColor(180, 180, 180))
        painter.setPen(pen)
        for i in range(num_hours):
            x = i * hour_width
            painter.drawLine(int(x), 0, int(x), height)
            painter.drawText(int(x) + 2, 12, f"{start + i}h")

        #Événements
        pen = QPen(QColor(100, 150, 200))
        painter.setPen(pen)
        painter.setBrush(QColor(100, 150, 200, 180))
        for ev in self.events:
            start_x = (ev["start_hour"] - start) * hour_width
            w = ev["duration_hour"] * hour_width
            painter.drawRect(int(start_x), 25, int(w), 40)
            painter.drawText(int(start_x) + 2, 45, ev["name"])


# ------------------ VisualizationPage ------------------
#Page complète de visualisation avec objets et timeline
class VisualizationPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_environment = "Default"
        self.objects = []

        self._init_ui()
        self._load_environment(self.current_environment)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        #--- Haut : EnvironmentSwitcher ---
        self.env_switcher = EnvironmentSwitcher()
        self.env_switcher.environment_changed.connect(self._on_env_changed)
        layout.addWidget(self.env_switcher)

        #--- Centre : zone de visualisation ---
        self.visual_area = QFrame()
        self.visual_area.setFrameShape(QFrame.StyledPanel)
        self.visual_area.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.visual_area_layout = QVBoxLayout(self.visual_area)
        layout.addWidget(self.visual_area, stretch=1)

        #--- Bas : Timeline ---
        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)
        self.timeline.load_events([
            {"name": "Event 1", "start_hour": 9, "duration_hour": 2},
            {"name": "Event 2", "start_hour": 12, "duration_hour": 1},
            {"name": "Event 3", "start_hour": 15, "duration_hour": 3},
        ])

        #--- Ajout d'objets ---
        self.add_object("Chaise", 100, 60)
        self.add_object("Table", 120, 70)
        self.add_object("Ordinateur", 80, 50)


    def _load_environment(self, env_name):
        self.current_environment = env_name

        #Nettoyage des anciens objets
        for obj in self.objects:
            obj.setParent(None)
        self.objects.clear()

        #Réajouter objets exemples
        self.add_object("Chaise", 100, 60)
        self.add_object("Table", 120, 70)
        self.add_object("Ordinateur", 80, 50)


    def add_object(self, name: str, width=80, height=50):
        #Ajoute un objet dans la zone de visualisation
        obj_widget = ObjectWidget(name, width, height)
        self.visual_area_layout.addWidget(obj_widget)
        self.objects.append(obj_widget)


    def _on_env_changed(self, env_name):
        self._load_environment(env_name)