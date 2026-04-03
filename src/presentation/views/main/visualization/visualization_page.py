# ============= INLINE/src/presentation/views/main/visualization/visualization_page.py =============


# =========================================== Imports ===========================================
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QInputDialog, QDialog, QListWidget, QCalendarWidget
)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen
from datetime import datetime, timedelta

# =========================================== Code ===========================================

class ObjectWidget(QFrame):
    clicked = Signal(str)
    moved = Signal(str, int, int)  

    def __init__(self, name: str, obj_id: str, width=80, height=50, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedSize(width, height)
        self.obj_id = obj_id  
        self.position = (0, 0)

        self.label = QLabel(name, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, width, height)
        self.label.setStyleSheet("font-weight: bold; color: blue;")

        self._drag_active = False
        self._drag_offset = QPoint(0, 0)
        self._drag_threshold = 5

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_offset = event.position().toPoint()
            self._start_pos = self.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_active:
            new_pos = self.mapToParent(event.position().toPoint() - self._drag_offset)
            self.move(new_pos)
            self.position = (new_pos.x(), new_pos.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = False
            distance = (self.pos() - self._start_pos).manhattanLength()
            self.position = (self.x(), self.y())
            if distance <= self._drag_threshold:
                self.clicked.emit(self.label.text())
            else:
                self.moved.emit(self.obj_id, self.x(), self.y())
        super().mouseReleaseEvent(event)

# -------------------------
# EnvironmentSwitcher : changement d'environnement
# -------------------------
class EnvironmentSwitcher(QWidget):
    environment_changed = Signal(str)

    def __init__(self, environments=None, parent=None):
        super().__init__(parent)
        self.environments = environments or ["Default"]
        self.current_index = 0

        layout = QHBoxLayout(self)
        self.prev_btn = QPushButton("←")
        self.next_btn = QPushButton("→")
        self.label = QLabel(self.environments[self.current_index])
        self.label.setAlignment(Qt.AlignCenter)
        self.btn_add_env = QPushButton("+ Env")

        layout.addWidget(self.prev_btn)
        layout.addWidget(self.label)
        layout.addWidget(self.next_btn)
        layout.addWidget(self.btn_add_env)

        self.prev_btn.clicked.connect(self.prev_env)
        self.next_btn.clicked.connect(self.next_env)
        self.btn_add_env.clicked.connect(self.add_env_dialog)

    def prev_env(self):
        self.current_index = (self.current_index - 1) % len(self.environments)
        self._update()

    def next_env(self):
        self.current_index = (self.current_index + 1) % len(self.environments)
        self._update()

    def _update(self):
        env = self.environments[self.current_index]
        self.label.setText(env)
        self.environment_changed.emit(env)

    def add_env_dialog(self):
        name, ok = QInputDialog.getText(self, "Nouvel environnement", "Nom :")
        if ok and name:
            if name not in self.environments:
                self.environments.append(name)
                self.current_index = len(self.environments) - 1
                self._update()


# -------------------------
# TimelineWidget : affichage des événements
# -------------------------
class TimelineWidget(QWidget):
    def __init__(self, parent=None, hours_range=(0, 23)):
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

        start, end = self.hours_range
        num_hours = end - start + 1
        hour_width = width / num_hours

        painter.setPen(QPen(QColor(180, 180, 180)))
        for i in range(num_hours):
            x = i * hour_width
            painter.drawLine(int(x), 0, int(x), height)
            painter.drawText(int(x) + 2, 12, f"{start + i}h")

        painter.setPen(QPen(QColor(100, 150, 200)))
        painter.setBrush(QColor(100, 150, 200, 180))
        offset = {}
        for ev in self.events:
            start_x = (ev["start_hour"] - start) * hour_width
            w = ev["duration_hour"] * hour_width
            y = 25 + offset.get(start_x, 0) * 20
            painter.drawRect(int(start_x), int(y), int(w), 15)
            painter.drawText(int(start_x) + 2, int(y) + 12, ev["name"])
            offset[start_x] = offset.get(start_x, 0) + 1


# -------------------------
# IntentionManagerDialog : création d’événements
# -------------------------
class IntentionManagerDialog(QDialog):

    def __init__(self, parent=None, intention_service=None, timeline_widget=None, event_service=None, current_env_id=None):
        super().__init__(parent)
        self.intention_service = intention_service
        self.event_service = event_service
        self.timeline_widget = timeline_widget
        self.current_env_id = current_env_id  

        self.setWindowTitle("Gestion des intentions")
        self.resize(400, 300)

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.btn_create_event = QPushButton("Créer événement")
        layout.addWidget(self.btn_create_event)
        self.btn_create_event.clicked.connect(self.add_event_for_selected)
        self.load_intentions()

    def load_intentions(self):
        self.list_widget.clear()
        if not self.intention_service:
            return
        for i in self.intention_service.get_all_intentions():
            self.list_widget.addItem(f"{i.id}: {i.title}")



    def add_event_for_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
    
        for item in selected_items:
            title = item.text().split(":", 1)[1].strip()
            start_hour, ok1 = QInputDialog.getDouble(self, "Début", f"Heure de début pour {title}", 8.0, 0.0, 23.99, 2)
            duration_minutes, ok2 = QInputDialog.getInt(self, "Durée (minutes)", f"Durée pour {title}", 60, 1, 1440)
            if not (ok1 and ok2):
                continue
    
            now = datetime.utcnow()
            start_time = now.replace(
                hour=int(start_hour),
                minute=int((start_hour % 1) * 60),
                second=0,
                microsecond=0
            )
    
            env_id = self.current_env_id  
    
            if self.event_service and env_id:
                intention_obj = next(
                    (i for i in self.intention_service.get_all_intentions() if i.title == title),
                    None
                )
                if intention_obj:
                    self.event_service.create_event(
                        intention_id=intention_obj.id,
                        environment_id=env_id,
                        start_time=start_time,
                        duration=duration_minutes
                    )
    
            if self.parent():
                self.parent().refresh_events()


# -------------------------
# VisualizationPage
# -------------------------
class VisualizationPage(QWidget):
    def __init__(self, intention_service=None, event_service=None, environment_service=None, interactive_object_service=None, parent=None):
        super().__init__(parent)
        self.intention_service = intention_service
        self.event_service = event_service
        self.environment_service = environment_service
        self.interactive_object_service = interactive_object_service

        self.environments = []    
        self.current_env_index = 0
        self.objects_by_env = {}         
        self.current_day = datetime.utcnow().date()

        self._init_ui()
        self._load_environments_from_db()
        self.refresh_events()

    # -------------------------------------------------------
    # Propriété utilitaire : environnement courant (domaine)
    # -------------------------------------------------------
    @property
    def current_environment_obj(self):
        if not self.environments:
            return None
        return self.environments[self.current_env_index]

    @property
    def current_environment_id(self):
        obj = self.current_environment_obj
        return obj.id if obj else None

    # -------------------------------------------------------
    # Chargement initial depuis la DB
    # -------------------------------------------------------
    def _load_environments_from_db(self):
        if not self.environment_service:
            return

        envs = self.environment_service.get_environments_for_owner("1")

        if not envs:
            # Crée un environnement par défaut si aucun n'existe
            default_env = self.environment_service.create_environment(owner_id="1", name="Default")
            envs = [default_env]

        self.environments = envs
        self.current_env_index = 0

        # Reconstruit les ObjectWidget depuis les objets persistés
        for env in self.environments:
            widgets = []
            for obj in env.objects:
                x, y = obj.get_position()
                w = ObjectWidget(name=obj.name, obj_id=obj.id, parent=self.visual_area)
                w.position = (x, y)
                w.clicked.connect(lambda n=obj.name: self.create_intention(n))
                w.moved.connect(self._on_object_moved)
                widgets.append(w)
            self.objects_by_env[env.id] = widgets

        self._update_env_switcher_label()
        self._refresh_visual_area()

    # -------------------------------------------------------
    # UI
    # -------------------------------------------------------
    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Navigation jour
        day_layout = QHBoxLayout()
        self.btn_prev_day = QPushButton("← Jour précédent")
        self.btn_next_day = QPushButton("Jour suivant →")
        self.btn_select_day = QPushButton("Choisir un jour…")
        self.lbl_current_day = QLabel(self.current_day.strftime("%Y-%m-%d"))
        self.lbl_current_day.setAlignment(Qt.AlignCenter)
        day_layout.addWidget(self.btn_prev_day)
        day_layout.addWidget(self.lbl_current_day)
        day_layout.addWidget(self.btn_next_day)
        day_layout.addWidget(self.btn_select_day)
        layout.addLayout(day_layout)

        self.btn_prev_day.clicked.connect(self.go_prev_day)
        self.btn_next_day.clicked.connect(self.go_next_day)
        self.btn_select_day.clicked.connect(self.select_day_dialog)

        # EnvironmentSwitcher
        env_layout = QHBoxLayout()
        self.btn_prev_env = QPushButton("←")
        self.btn_next_env = QPushButton("→")
        self.lbl_env_name = QLabel("...")
        self.lbl_env_name.setAlignment(Qt.AlignCenter)
        self.btn_add_env = QPushButton("+ Env")
        env_layout.addWidget(self.btn_prev_env)
        env_layout.addWidget(self.lbl_env_name)
        env_layout.addWidget(self.btn_next_env)
        env_layout.addWidget(self.btn_add_env)
        layout.addLayout(env_layout)

        self.btn_prev_env.clicked.connect(self.prev_env)
        self.btn_next_env.clicked.connect(self.next_env)
        self.btn_add_env.clicked.connect(self.add_env_dialog)

        # Zone visuelle
        self.visual_area = QFrame()
        self.visual_area.setFrameShape(QFrame.StyledPanel)
        self.visual_area.setStyleSheet("background-color: white; border: 1px solid gray;")
        layout.addWidget(self.visual_area, stretch=1)

        # Timeline
        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)

        # Boutons
        self.btn_manage_intentions = QPushButton("Gérer les intentions / Créer événement")
        layout.addWidget(self.btn_manage_intentions)
        self.btn_manage_intentions.clicked.connect(self.open_intention_manager)

        self.btn_add_object = QPushButton("Ajouter un objet")
        layout.addWidget(self.btn_add_object)
        self.btn_add_object.clicked.connect(self.create_object_dialog)

    # -------------------------------------------------------
    # Navigation environnements
    # -------------------------------------------------------
    def prev_env(self):
        if not self.environments:
            return
        self.current_env_index = (self.current_env_index - 1) % len(self.environments)
        self._update_env_switcher_label()
        self._refresh_visual_area()
        self.refresh_events()

    def next_env(self):
        if not self.environments:
            return
        self.current_env_index = (self.current_env_index + 1) % len(self.environments)
        self._update_env_switcher_label()
        self._refresh_visual_area()
        self.refresh_events()

    def _update_env_switcher_label(self):
        obj = self.current_environment_obj
        self.lbl_env_name.setText(obj.name if obj else "—")

    def add_env_dialog(self):
        name, ok = QInputDialog.getText(self, "Nouvel environnement", "Nom :")
        if not ok or not name:
            return

        # Vérifie doublon de nom
        if any(e.name == name for e in self.environments):
            return

        # Persiste
        new_env = self.environment_service.create_environment(owner_id="1", name=name)
        self.environments.append(new_env)
        self.objects_by_env[new_env.id] = []
        self.current_env_index = len(self.environments) - 1
        self._update_env_switcher_label()
        self._refresh_visual_area()
        self.refresh_events()

    # -------------------------------------------------------
    # Navigation jour
    # -------------------------------------------------------
    def go_prev_day(self):
        self.current_day -= timedelta(days=1)
        self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
        self.refresh_events()

    def go_next_day(self):
        self.current_day += timedelta(days=1)
        self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
        self.refresh_events()

    def select_day_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Choisir un jour")
        layout = QVBoxLayout(dialog)
        calendar = QCalendarWidget()
        calendar.setSelectedDate(self.current_day)
        layout.addWidget(calendar)
        btn_ok = QPushButton("Valider")
        layout.addWidget(btn_ok)

        def on_ok():
            self.current_day = calendar.selectedDate().toPython()
            self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
            self.refresh_events()
            dialog.accept()

        btn_ok.clicked.connect(on_ok)
        dialog.exec()

    # -------------------------------------------------------
    # Gestion des objets
    # -------------------------------------------------------
    def add_object(self, name, position=(10, 10)):
        env = self.current_environment_obj
        if not env:
            return

        # Crée dans le domaine via le service (qui persiste)
        from domain.enums.enums import ObjectCategory
        from uuid import uuid4

        obj_domain = self.interactive_object_service.create_object(
            environment_id=env.id,
            type="clickable",
            id=str(uuid4()),
            name=name,
            position=position,
            category=ObjectCategory.PHYSIQUE
        )

        # Crée le widget correspondant
        w = ObjectWidget(name, parent=self.visual_area)
        w.position = position
        w.clicked.connect(lambda n=name: self.create_intention(n))
        w.moved.connect(self._on_object_moved)   # <-- ajout
        self.objects_by_env.setdefault(env.id, []).append(w)
        self._refresh_visual_area()

    def _on_object_moved(self, obj_id: str, x: int, y: int):
        env = self.current_environment_obj
        if not env or not self.interactive_object_service:
            return
        # Met à jour la position dans le domaine et persiste
        self.interactive_object_service.update_object_position(
            environment_id=env.id,
            object_id=obj_id,
            position=(x, y)
        )

    def _refresh_visual_area(self):
        # Détache tous les widgets
        for env_id, widgets in self.objects_by_env.items():
            for w in widgets:
                w.setParent(None)

        # Affiche uniquement ceux de l'environnement courant
        env_id = self.current_environment_id
        if not env_id:
            return
        for w in self.objects_by_env.get(env_id, []):
            w.setParent(self.visual_area)
            x, y = getattr(w, 'position', (10, 10))
            w.move(x, y)
            w.show()


    def create_object_dialog(self):
        name, ok = QInputDialog.getText(self, "Nouvel objet", "Nom de l'objet :")
        if ok and name:
            from domain.enums.enums import ObjectCategory
            from uuid import uuid4
            env = self.current_environment_obj
            if not env:
                return
            new_id = str(uuid4())
            self.interactive_object_service.create_object(
                environment_id=env.id,
                type="clickable",
                id=new_id,
                name=name,
                position=(10, 10),
                category=ObjectCategory.PHYSIQUE
            )
            self.add_object(name=name, obj_id=new_id, position=(10, 10))

    def create_intention(self, object_name):
        if not self.intention_service:
            return
        title, ok = QInputDialog.getText(self, "Nouvelle Intention", f"Titre pour {object_name} :")
        if ok and title:
            self.intention_service.create_intention(user_id="1", title=title, category="Physique")


    def open_intention_manager(self):
        if not self.intention_service:
            return
        dialog = IntentionManagerDialog(
            parent=self,
            intention_service=self.intention_service,
            timeline_widget=self.timeline,
            event_service=self.event_service,
            current_env_id=self.current_environment_id 
        )
        dialog.exec()

    # -------------------------------------------------------
    # Rafraîchissement des événements
    # -------------------------------------------------------
    def refresh_events(self):
        env_id = self.current_environment_id
        if not env_id or not self.event_service or not self.intention_service:
            self.timeline.load_events([])
            return

        start_day = datetime.combine(self.current_day, datetime.min.time())
        end_day = datetime.combine(self.current_day, datetime.max.time())

        events = self.event_service.get_events_between(env_id, start_day, end_day)
        intentions_map = self.intention_service.get_intentions_map()

        ui_events = []
        for ev in events:
            intention = intentions_map.get(ev.intention_id)
            ui_events.append({
                "name": intention.title if intention else "Unknown",
                "start_hour": ev.start_time.hour + ev.start_time.minute / 60,
                "duration_hour": ev.duration / 60
            })

        self.timeline.load_events(ui_events)