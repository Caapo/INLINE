# #==== INLINE/src/presentation/views/main/visualization/visualization_page.py ====

# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
#     QFrame, QSizePolicy, QInputDialog, QDialog, QListWidget
# )
# from PySide6.QtCore import Qt, Signal, QPoint
# from PySide6.QtGui import QPainter, QColor, QPen
# from datetime import datetime


# # ObjectWidget
# class ObjectWidget(QFrame):
#     clicked = Signal(str)

#     def __init__(self, name: str, width=80, height=50, parent=None):
#         super().__init__(parent)
#         self.setFrameShape(QFrame.Box)
#         self.setFixedSize(width, height)

#         self.label = QLabel(name, self)
#         self.label.setAlignment(Qt.AlignCenter)
#         self.label.setGeometry(0, 0, width, height)
#         self.label.setStyleSheet("font-weight: bold; color: blue;")

#         self._drag_active = False
#         self._drag_offset = QPoint(0, 0)
#         self._drag_threshold = 5

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self._drag_active = True
#             self._drag_offset = event.position().toPoint()
#             self._start_pos = self.pos()
#         super().mousePressEvent(event)

#     def mouseMoveEvent(self, event):
#         if self._drag_active:
#             new_pos = self.mapToParent(event.position().toPoint() - self._drag_offset)
#             self.move(new_pos)
#         super().mouseMoveEvent(event)

#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self._drag_active = False
#             distance = (self.pos() - self._start_pos).manhattanLength()
#             if distance <= self._drag_threshold:
#                 self.clicked.emit(self.label.text())
#         super().mouseReleaseEvent(event)



# # EnvironmentSwitcher
# class EnvironmentSwitcher(QWidget):
#     environment_changed = Signal(str)

#     def __init__(self, environments=None, parent=None):
#         super().__init__(parent)
#         self.environments = environments or ["Default", "Env2", "Env3"]
#         self.current_index = 0

#         layout = QHBoxLayout(self)
#         self.prev_btn = QPushButton("←")
#         self.next_btn = QPushButton("→")
#         self.label = QLabel(self.environments[self.current_index])
#         self.label.setAlignment(Qt.AlignCenter)

#         layout.addWidget(self.prev_btn)
#         layout.addWidget(self.label)
#         layout.addWidget(self.next_btn)

#         self.prev_btn.clicked.connect(self.prev_env)
#         self.next_btn.clicked.connect(self.next_env)

#     def prev_env(self):
#         self.current_index = (self.current_index - 1) % len(self.environments)
#         self._update()

#     def next_env(self):
#         self.current_index = (self.current_index + 1) % len(self.environments)
#         self._update()

#     def _update(self):
#         env = self.environments[self.current_index]
#         self.label.setText(env)
#         self.environment_changed.emit(env)



# # TimelineWidget
# class TimelineWidget(QWidget):
#     def __init__(self, parent=None, hours_range=(0, 23)):
#         super().__init__(parent)
#         self.hours_range = hours_range
#         self.events = []

#         self.setMinimumHeight(80)
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

#     def load_events(self, events):
#         self.events = events
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         rect = self.rect()
#         width = rect.width()
#         height = rect.height()

#         painter.fillRect(rect, QColor(230, 230, 230))

#         start, end = self.hours_range
#         num_hours = end - start + 1
#         hour_width = width / num_hours

#         # Grille horaire
#         painter.setPen(QPen(QColor(180, 180, 180)))
#         for i in range(num_hours):
#             x = i * hour_width
#             painter.drawLine(int(x), 0, int(x), height)
#             painter.drawText(int(x) + 2, 12, f"{start + i}h")

#         # Events
#         painter.setPen(QPen(QColor(100, 150, 200)))
#         painter.setBrush(QColor(100, 150, 200, 180))

#         offset = {}
#         for ev in self.events:
#             start_x = (ev["start_hour"] - start) * hour_width
#             w = ev["duration_hour"] * hour_width
#             y = 25 + offset.get(start_x, 0) * 20
#             painter.drawRect(int(start_x), int(y), int(w), 15)
#             painter.drawText(int(start_x) + 2, int(y) + 12, ev["name"])
#             offset[start_x] = offset.get(start_x, 0) + 1


# # IntentionManagerDialog
# class IntentionManagerDialog(QDialog):
#     def __init__(self, parent=None, intention_service=None, timeline_widget=None, event_service=None):
#         super().__init__(parent)
#         self.intention_service = intention_service
#         self.event_service = event_service
#         self.timeline_widget = timeline_widget

#         self.setWindowTitle("Gestion des intentions")
#         self.resize(400, 300)

#         layout = QVBoxLayout(self)

#         self.list_widget = QListWidget()
#         layout.addWidget(self.list_widget)

#         self.btn_create_event = QPushButton("Créer événement")
#         layout.addWidget(self.btn_create_event)
#         self.btn_create_event.clicked.connect(self.add_event_for_selected)

#         self.load_intentions()

#     def load_intentions(self):
#         self.list_widget.clear()
#         if not self.intention_service:
#             return
#         #Méthode à ajouter dans IntentionService: get_all_intentions()
#         for i in self.intention_service.get_all_intentions():
#             self.list_widget.addItem(f"{i.id}: {i.title}")

#     def add_event_for_selected(self):
#         selected_items = self.list_widget.selectedItems()
#         if not selected_items:
#             return
    
#         for item in selected_items:
#             text = item.text()
#             title = text.split(":", 1)[1].strip()
    
#             # Saisie horaire
#             start_hour, ok1 = QInputDialog.getInt(self, "Début", f"Heure de début pour {title}", 8, 0, 23)
#             duration_minutes, ok2 = QInputDialog.getInt(self, "Durée (minutes)", f"Durée (minutes) pour {title}", 60, 1, 1440)
#             if not (ok1 and ok2):
#                 continue
    
#             # Création datetime de début basé sur aujourd'hui
#             now = datetime.utcnow()
#             start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    
#             # Création via EventService
#             if self.event_service:
#                 env_id = getattr(self.parent(), "current_environment", "Default")
#                 # récupération de l'id de l’intention : ici simplifié, en prenant le premier qui correspond au titre
#                 intention_list = self.intention_service.get_all_intentions()
#                 intention_obj = next((i for i in intention_list if i.title == title), None)
#                 if intention_obj:
#                     self.event_service.create_event(
#                         intention_id=intention_obj.id,
#                         environment_id=env_id,
#                         start_time=start_time,
#                         duration=duration_minutes
#                     )
    
#             # Ajout direct à la timeline pour l'affichage
#             if self.timeline_widget:
#                 self.timeline_widget.events.append({
#                     "name": title,
#                     "start_hour": start_hour,
#                     "duration_hour": duration_minutes / 60
#                 })
#                 self.timeline_widget.update()


# from PySide6.QtWidgets import QCalendarWidget, QDialog, QVBoxLayout, QPushButton
# from datetime import datetime, timedelta


# # VisualizationPage 
# class VisualizationPage(QWidget):
#     def __init__(self, intention_service=None, event_service=None, environment_service=None, parent=None):
#         super().__init__(parent)
#         self.intention_service = intention_service
#         self.event_service = event_service
#         self.environment_service = environment_service

#         self.current_environment = "Default"
#         self.objects = []
#         self.current_day = datetime.utcnow().date()  # jour affiché par défaut

#         self._init_ui()
#         self.refresh_events()

#     def _init_ui(self):
#         layout = QVBoxLayout(self)

#         # --- Sélecteur de jour ---
#         day_layout = QHBoxLayout()
#         self.btn_prev_day = QPushButton("← Jour précédent")
#         self.btn_next_day = QPushButton("Jour suivant →")
#         self.btn_select_day = QPushButton("Choisir un jour…")
#         self.lbl_current_day = QLabel(self.current_day.strftime("%Y-%m-%d"))
#         self.lbl_current_day.setAlignment(Qt.AlignCenter)

#         day_layout.addWidget(self.btn_prev_day)
#         day_layout.addWidget(self.lbl_current_day)
#         day_layout.addWidget(self.btn_next_day)
#         day_layout.addWidget(self.btn_select_day)
#         layout.addLayout(day_layout)

#         self.btn_prev_day.clicked.connect(self.go_prev_day)
#         self.btn_next_day.clicked.connect(self.go_next_day)
#         self.btn_select_day.clicked.connect(self.select_day_dialog)

#         # EnvironmentSwitcher
#         self.env_switcher = EnvironmentSwitcher()
#         self.env_switcher.environment_changed.connect(self._on_env_changed)
#         layout.addWidget(self.env_switcher)

#         # Visual area
#         self.visual_area = QFrame()
#         self.visual_area.setFrameShape(QFrame.StyledPanel)
#         self.visual_area.setStyleSheet("background-color: white; border: 1px solid gray;")
#         self.visual_area_layout = QVBoxLayout(self.visual_area)
#         layout.addWidget(self.visual_area, stretch=1)

#         # Timeline
#         self.timeline = TimelineWidget()
#         layout.addWidget(self.timeline)

#         # Bouton pour gérer les intentions et créer événements
#         self.btn_manage_intentions = QPushButton("Gérer les intentions / Créer événement")
#         layout.addWidget(self.btn_manage_intentions)
#         self.btn_manage_intentions.clicked.connect(self.open_intention_manager)

#         # Objets exemples
#         self.add_object("Chaise", 100, 60)
#         self.add_object("Table", 120, 70)
#         self.add_object("Ordinateur", 80, 50)

#     # --- Navigation jour ---
#     def go_prev_day(self):
#         self.current_day -= timedelta(days=1)
#         self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
#         self.refresh_events()

#     def go_next_day(self):
#         self.current_day += timedelta(days=1)
#         self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
#         self.refresh_events()

#     def select_day_dialog(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Choisir un jour")
#         layout = QVBoxLayout(dialog)
#         calendar = QCalendarWidget()
#         calendar.setSelectedDate(self.current_day)
#         layout.addWidget(calendar)
#         btn_ok = QPushButton("Valider")
#         layout.addWidget(btn_ok)

#         def on_ok():
#             self.current_day = calendar.selectedDate().toPython()
#             self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
#             self.refresh_events()
#             dialog.accept()

#         btn_ok.clicked.connect(on_ok)
#         dialog.exec()

#     # --- Objets et intentions ---
#     def add_object(self, name, width=80, height=50):
#         obj = ObjectWidget(name, width, height)
#         obj.clicked.connect(lambda n=name: self.create_intention(n))
#         self.visual_area_layout.addWidget(obj)
#         self.objects.append(obj)

#     def create_intention(self, object_name):
#         if not self.intention_service:
#             print(f"[DEBUG] Objet cliqué : {object_name} (aucun service)")
#             return
#         title, ok = QInputDialog.getText(self, "Nouvelle Intention", f"Titre pour {object_name} :")
#         if ok and title:
#             self.intention_service.create_intention(user_id="1", title=title, category="Physique")
#             print(f"Intention créée pour {object_name}: {title}")

#     def open_intention_manager(self):
#         if not self.intention_service:
#             return
#         dialog = IntentionManagerDialog(
#             parent=self,
#             intention_service=self.intention_service,
#             timeline_widget=self.timeline,
#             event_service=self.event_service
#         )
#         dialog.exec()

#     # --- EnvironmentSwitcher ---
#     def _on_env_changed(self, env_name):
#         self.current_environment = env_name
#         self.refresh_events()

#     # --- Refresh events pour le jour courant et l'environnement courant ---
#     def refresh_events(self):
#         if not self.event_service:
#             self.timeline.load_events([])
#             return

#         start_day = datetime.combine(self.current_day, datetime.min.time())
#         end_day = datetime.combine(self.current_day, datetime.max.time())

#         events = self.event_service.get_events_between(self.current_environment, start_day, end_day)
#         ui_events = [{"name": getattr(ev, "intention_id", "Event"),
#                       "start_hour": ev.start_time.hour + ev.start_time.minute / 60,
#                       "duration_hour": ev.duration / 60} for ev in events]
#         self.timeline.load_events(ui_events)



from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QInputDialog, QDialog, QListWidget, QCalendarWidget
)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen
from datetime import datetime, timedelta


# -------------------------
# ObjectWidget : objet draggable et cliquable
# -------------------------
class ObjectWidget(QFrame):
    clicked = Signal(str)

    def __init__(self, name: str, width=80, height=50, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedSize(width, height)

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
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = False
            distance = (self.pos() - self._start_pos).manhattanLength()
            if distance <= self._drag_threshold:
                self.clicked.emit(self.label.text())
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
        self.btn_add_env = QPushButton("+ Env")  # ajouter un environnement

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

        # grille horaire
        painter.setPen(QPen(QColor(180, 180, 180)))
        for i in range(num_hours):
            x = i * hour_width
            painter.drawLine(int(x), 0, int(x), height)
            painter.drawText(int(x) + 2, 12, f"{start + i}h")

        # events
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
# IntentionManagerDialog : création d’événements avec heure précise
# -------------------------
class IntentionManagerDialog(QDialog):
    def __init__(self, parent=None, intention_service=None, timeline_widget=None, event_service=None):
        super().__init__(parent)
        self.intention_service = intention_service
        self.event_service = event_service
        self.timeline_widget = timeline_widget

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
            # heure précise début
            start_hour, ok1 = QInputDialog.getDouble(self, "Début", f"Heure précise de début pour {title}", 8.0, 0.0, 23.99, 2)
            duration_minutes, ok2 = QInputDialog.getInt(self, "Durée (minutes)", f"Durée pour {title}", 60, 1, 1440)
            if not (ok1 and ok2):
                continue

            now = datetime.utcnow()
            start_time = now.replace(hour=int(start_hour), minute=int((start_hour % 1) * 60), second=0, microsecond=0)

            if self.event_service:
                env_id = getattr(self.parent(), "current_environment", "Default")
                intention_obj = next((i for i in self.intention_service.get_all_intentions() if i.title == title), None)
                if intention_obj:
                    self.event_service.create_event(
                        intention_id=intention_obj.id,
                        environment_id=env_id,
                        start_time=start_time,
                        duration=duration_minutes
                    )

            if self.timeline_widget:
                self.timeline_widget.events.append({
                    "name": title,
                    "start_hour": start_hour,
                    "duration_hour": duration_minutes / 60
                })
                self.timeline_widget.update()


# -------------------------
# VisualizationPage : page principale
# -------------------------
class VisualizationPage(QWidget):
    def __init__(self, intention_service=None, event_service=None, environment_service=None, parent=None):
        super().__init__(parent)
        self.intention_service = intention_service
        self.event_service = event_service
        self.environment_service = environment_service

        self.current_environment = "Default"
        self.objects_by_env = {}   # dict[env_name] = [ObjectWidget,...]
        self.timeline_by_env = {}  # dict[env_name] = events list
        self.current_day = datetime.utcnow().date()

        self._init_ui()
        self.refresh_events()

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
        self.env_switcher = EnvironmentSwitcher()
        self.env_switcher.environment_changed.connect(self._on_env_changed)
        layout.addWidget(self.env_switcher)

        # Zone visuelle
        self.visual_area = QFrame()
        self.visual_area.setFrameShape(QFrame.StyledPanel)
        self.visual_area.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.visual_area_layout = QVBoxLayout(self.visual_area)
        layout.addWidget(self.visual_area, stretch=1)

        # Timeline
        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)

        # Bouton intentions
        self.btn_manage_intentions = QPushButton("Gérer les intentions / Créer événement")
        layout.addWidget(self.btn_manage_intentions)
        self.btn_manage_intentions.clicked.connect(self.open_intention_manager)

        # Bouton création d'objet dynamique
        self.btn_add_object = QPushButton("Ajouter un objet")
        layout.addWidget(self.btn_add_object)
        self.btn_add_object.clicked.connect(self.create_object_dialog)

    # --- Navigation jour ---
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

    # --- Objets dynamiques ---
    def add_object(self, name, width=80, height=50):
        obj = ObjectWidget(name, width, height)
        obj.clicked.connect(lambda n=name: self.create_intention(n))
        env = self.current_environment
        self.objects_by_env.setdefault(env, []).append(obj)
        self._refresh_visual_area()
        
    def _refresh_visual_area(self):
        # supprime tout et recharge les objets pour l'environnement courant
        for i in reversed(range(self.visual_area_layout.count())):
            w = self.visual_area_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        for obj in self.objects_by_env.get(self.current_environment, []):
            self.visual_area_layout.addWidget(obj)

    def create_object_dialog(self):
        name, ok = QInputDialog.getText(self, "Nouvel objet", "Nom de l'objet :")
        if ok and name:
            self.add_object(name)

    def create_intention(self, object_name):
        if not self.intention_service:
            print(f"[DEBUG] Objet cliqué : {object_name} (aucun service)")
            return
        title, ok = QInputDialog.getText(self, "Nouvelle Intention", f"Titre pour {object_name} :")
        if ok and title:
            self.intention_service.create_intention(user_id="1", title=title, category="Physique")
            print(f"Intention créée pour {object_name}: {title}")

    def open_intention_manager(self):
        if not self.intention_service:
            return
        dialog = IntentionManagerDialog(
            parent=self,
            intention_service=self.intention_service,
            timeline_widget=self.timeline,
            event_service=self.event_service
        )
        dialog.exec()

    # --- EnvironmentSwitcher ---
    def _on_env_changed(self, env_name):
        self.current_environment = env_name
        self._refresh_visual_area()
        self.refresh_events()

    # --- Rafraîchissement des événements ---
    def refresh_events(self):
        env = self.current_environment
        if not self.event_service:
            self.timeline.load_events([])
            return

        start_day = datetime.combine(self.current_day, datetime.min.time())
        end_day = datetime.combine(self.current_day, datetime.max.time())
        events = self.event_service.get_events_between(env, start_day, end_day)
        ui_events = [{
            "name": getattr(ev, "intention_id", "Event"),
            "start_hour": ev.start_time.hour + ev.start_time.minute / 60,
            "duration_hour": ev.duration / 60
        } for ev in events]
        self.timeline.load_events(ui_events)