# ============= INLINE/src/presentation/views/main/visualization/visualization_page.py =============

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QInputDialog, QDialog, QListWidget,
    QCalendarWidget, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen
from datetime import datetime, timedelta


# -------------------------
# ObjectWidget
# -------------------------
class ObjectWidget(QFrame):
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
        self.label.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 11px;
            background: transparent;
        """)
        self.label.setWordWrap(True)

        self.position      = (0, 0)
        self._drag_active  = False
        self._drag_offset  = QPoint(0, 0)
        self._drag_threshold = 5

    def update_name(self, new_name: str):
        self.obj_name = new_name
        self.label.setText(new_name)

    # --- Drag & drop ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_offset = event.position().toPoint()
            self._start_pos   = self.pos()
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
                self._show_context_menu(event.globalPosition().toPoint())
            else:
                if self.obj_id:
                    self.moved.emit(self.obj_id, self.x(), self.y())
        super().mouseReleaseEvent(event)

    def _show_context_menu(self, global_pos):
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
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3a3a5c;
            }
            QMenu::item:disabled {
                color: #aaa;
                font-size: 11px;
                padding: 4px 24px;
            }
            QMenu::separator {
                height: 1px;
                background: #444;
                margin: 3px 8px;
            }
        """)

        # Titre non cliquable
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


# -------------------------
# TimelineWidget
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
        rect    = self.rect()
        width   = rect.width()
        height  = rect.height()
        painter.fillRect(rect, QColor(230, 230, 230))

        start, end = self.hours_range
        num_hours  = end - start + 1
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
            y = 25 + offset.get(int(start_x), 0) * 20
            painter.drawRect(int(start_x), int(y), int(w), 15)
            painter.drawText(int(start_x) + 2, int(y) + 12, ev["name"])
            offset[int(start_x)] = offset.get(int(start_x), 0) + 1


# -------------------------
# IntentionManagerDialog
# -------------------------
class IntentionManagerDialog(QDialog):
    def __init__(self, parent=None, intention_service=None, timeline_widget=None,
                 event_service=None, current_env_id=None, current_day=None):
        super().__init__(parent)
        self.intention_service = intention_service
        self.event_service     = event_service
        self.timeline_widget   = timeline_widget
        self.current_env_id    = current_env_id
        self.current_day       = current_day or datetime.utcnow().date()

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
            start_hour, ok1 = QInputDialog.getDouble(
                self, "Début", f"Heure de début pour {title}", 8.0, 0.0, 23.99, 2
            )
            duration_minutes, ok2 = QInputDialog.getInt(
                self, "Durée (minutes)", f"Durée pour {title}", 60, 1, 1440
            )
            if not (ok1 and ok2):
                continue

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
                intention_obj = next(
                    (i for i in self.intention_service.get_all_intentions() if i.title == title),
                    None
                )
                if intention_obj:
                    self.event_service.create_event(
                        intention_id=intention_obj.id,
                        environment_id=self.current_env_id,
                        start_time=start_time,
                        duration=duration_minutes
                    )


# -------------------------
# VisualizationPage
# -------------------------
class VisualizationPage(QWidget):
    def __init__(self, intention_service=None, event_service=None,
                 environment_service=None, interactive_object_service=None, parent=None):
        super().__init__(parent)
        self.intention_service          = intention_service
        self.event_service              = event_service
        self.environment_service        = environment_service
        self.interactive_object_service = interactive_object_service

        self.environments      = []
        self.current_env_index = 0
        self.objects_by_env    = {}
        self.current_day       = datetime.utcnow().date()

        self._init_ui()
        self._load_environments_from_db()
        self._subscribe_to_services()
        self.refresh_events()

    # -------------------------------------------------------
    # Properties
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
    # Observer
    # -------------------------------------------------------
    def _subscribe_to_services(self):
        if self.event_service:
            self.event_service.subscribe("event_created", self._on_event_changed)
            self.event_service.subscribe("event_updated", self._on_event_changed)
        if self.intention_service:
            self.intention_service.subscribe("intention_created", self._on_intention_changed)
        if self.environment_service:
            self.environment_service.subscribe("environment_created", self._on_environment_created)

    def _on_event_changed(self, event):
        self.refresh_events()

    def _on_intention_changed(self, intention):
        self._refresh_intention_count()

    def _on_environment_created(self, environment):
        self._update_env_label()

    # -------------------------------------------------------
    # Chargement depuis la DB
    # -------------------------------------------------------
    def _load_environments_from_db(self):
        if not self.environment_service:
            return

        envs = self.environment_service.get_environments_for_owner("1")
        if not envs:
            default_env = self.environment_service.create_environment(owner_id="1", name="Default")
            envs = [default_env]

        self.environments      = envs
        self.current_env_index = 0

        for env in self.environments:
            widgets = []
            for obj in env.objects:
                x, y = obj.get_position()
                w = self._make_widget(obj.name, obj.id, (x, y))
                widgets.append(w)
            self.objects_by_env[env.id] = widgets

        self._update_env_label()
        self._refresh_visual_area()
        self._refresh_intention_count()

    # -------------------------------------------------------
    # UI
    # -------------------------------------------------------
    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Navigation jour
        day_layout = QHBoxLayout()
        self.btn_prev_day    = QPushButton("← Jour précédent")
        self.btn_next_day    = QPushButton("Jour suivant →")
        self.btn_select_day  = QPushButton("Choisir un jour…")
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

        # Switcher environnement
        env_layout = QHBoxLayout()
        self.btn_prev_env = QPushButton("←")
        self.btn_next_env = QPushButton("→")
        self.lbl_env_name = QLabel("...")
        self.lbl_env_name.setAlignment(Qt.AlignCenter)
        self.btn_add_env  = QPushButton("+ Env")
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
        self.visual_area.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ccc;")
        layout.addWidget(self.visual_area, stretch=1)

        # Timeline
        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)

        # Compteur intentions (Observer visible)
        self.lbl_intention_count = QLabel("Intentions : 0")
        self.lbl_intention_count.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_intention_count)

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
        self._update_env_label()
        self._refresh_visual_area()
        self.refresh_events()

    def next_env(self):
        if not self.environments:
            return
        self.current_env_index = (self.current_env_index + 1) % len(self.environments)
        self._update_env_label()
        self._refresh_visual_area()
        self.refresh_events()

    def _update_env_label(self):
        obj = self.current_environment_obj
        self.lbl_env_name.setText(obj.name if obj else "—")

    def add_env_dialog(self):
        name, ok = QInputDialog.getText(self, "Nouvel environnement", "Nom :")
        if not ok or not name:
            return
        if any(e.name == name for e in self.environments):
            return
        new_env = self.environment_service.create_environment(owner_id="1", name=name)
        self.environments.append(new_env)
        self.objects_by_env[new_env.id] = []
        self.current_env_index = len(self.environments) - 1
        self._update_env_label()
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
    def _make_widget(self, name: str, obj_id: str, position=(10, 10)) -> ObjectWidget:
        w = ObjectWidget(name, parent=self.visual_area)
        w.obj_id   = obj_id
        w.position = position
        w.request_intention.connect(self._on_request_intention)
        w.request_rename.connect(self._on_request_rename)
        w.request_delete.connect(self._on_request_delete)
        w.moved.connect(self._on_object_moved)
        return w

    def add_object(self, name, position=(10, 10)):
        env = self.current_environment_obj
        if not env or not self.interactive_object_service:
            return
        from domain.enums.enums import ObjectCategory
        from uuid import uuid4

        new_id = str(uuid4())
        self.interactive_object_service.create_object(
            environment_id=env.id,
            type="clickable",
            id=new_id,
            name=name,
            position=position,
            category=ObjectCategory.PHYSIQUE
        )
        w = self._make_widget(name, new_id, position)
        self.objects_by_env.setdefault(env.id, []).append(w)
        self._refresh_visual_area()

    def _refresh_visual_area(self):
        for widgets in self.objects_by_env.values():
            for w in widgets:
                w.setParent(None)

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
            self.add_object(name, position=(10, 10))

    def _find_widget_by_id(self, obj_id: str):
        for w in self.objects_by_env.get(self.current_environment_id, []):
            if w.obj_id == obj_id:
                return w
        return None

    # -------------------------------------------------------
    # Handlers menu contextuel
    # -------------------------------------------------------
    def _on_request_intention(self, obj_id: str):
        w = self._find_widget_by_id(obj_id)
        if not w or not self.intention_service:
            return
        title, ok = QInputDialog.getText(
            self, "Nouvelle intention", f"Intention pour « {w.obj_name} » :"
        )
        if ok and title:
            self.intention_service.create_intention(
                user_id="1", title=title, category="Physique"
            )

    def _on_request_rename(self, obj_id: str):
        w = self._find_widget_by_id(obj_id)
        if not w:
            return
        new_name, ok = QInputDialog.getText(
            self, "Renommer", "Nouveau nom :", text=w.obj_name
        )
        if ok and new_name:
            self.interactive_object_service.rename_object(
                environment_id=self.current_environment_id,
                object_id=obj_id,
                new_name=new_name
            )
            w.update_name(new_name)

    def _on_request_delete(self, obj_id: str):
        w = self._find_widget_by_id(obj_id)
        if not w:
            return
        confirm = QMessageBox.question(
            self, "Supprimer",
            f"Supprimer « {w.obj_name} » ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.interactive_object_service.delete_object(
                environment_id=self.current_environment_id,
                object_id=obj_id
            )
            env_id = self.current_environment_id
            self.objects_by_env[env_id] = [
                x for x in self.objects_by_env[env_id] if x.obj_id != obj_id
            ]
            w.setParent(None)

    def _on_object_moved(self, obj_id: str, x: int, y: int):
        env = self.current_environment_obj
        if not env or not self.interactive_object_service:
            return
        self.interactive_object_service.update_object_position(
            environment_id=env.id,
            object_id=obj_id,
            position=(x, y)
        )

    # -------------------------------------------------------
    # Intentions
    # -------------------------------------------------------
    def _refresh_intention_count(self):
        if self.intention_service:
            count = len(self.intention_service.get_all_intentions())
            self.lbl_intention_count.setText(f"Intentions : {count}")

    def open_intention_manager(self):
        if not self.intention_service:
            return
        dialog = IntentionManagerDialog(
            parent=self,
            intention_service=self.intention_service,
            timeline_widget=self.timeline,
            event_service=self.event_service,
            current_env_id=self.current_environment_id,
            current_day=self.current_day
        )
        dialog.exec()

    # -------------------------------------------------------
    # Refresh events
    # -------------------------------------------------------
    def refresh_events(self):
        env_id = self.current_environment_id
        if not env_id or not self.event_service or not self.intention_service:
            self.timeline.load_events([])
            return

        start_day = datetime.combine(self.current_day, datetime.min.time())
        end_day   = datetime.combine(self.current_day, datetime.max.time())

        events        = self.event_service.get_events_between(env_id, start_day, end_day)
        intentions_map = self.intention_service.get_intentions_map()

        ui_events = []
        for ev in events:
            intention = intentions_map.get(ev.intention_id)
            ui_events.append({
                "name":          intention.title if intention else "Unknown",
                "start_hour":    ev.start_time.hour + ev.start_time.minute / 60,
                "duration_hour": ev.duration / 60
            })

        self.timeline.load_events(ui_events)