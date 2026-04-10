# === INLINE/src/presentation/views/main/visualization/visualization_page.py ===

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QFrame, QInputDialog, QDialog, QCalendarWidget, QMessageBox)
from PySide6.QtCore import Qt
from datetime import datetime, timedelta

from presentation.views.main.visualization.object_widget import ObjectWidget
from presentation.views.main.visualization.timeline_widget import TimelineWidget
from presentation.views.main.visualization.dialogs.event_dialog import EventDialog
from presentation.views.main.visualization.dialogs.intention_manager_dialog import IntentionManagerDialog


class VisualizationPage(QWidget):
    """
    Page principale de visualisation des espaces de vie.
    Affiche les environnements, leurs objets interactifs et la timeline.
    Orchestre les interactions entre l'utilisateur et les services
    via le patron Observer pour se mettre à jour automatiquement.
    """

    def __init__(self, intention_service=None, event_service=None,
                 environment_service=None, interactive_object_service=None, parent=None):
        super().__init__(parent)
        self.intention_service          = intention_service
        self.event_service              = event_service
        self.environment_service        = environment_service
        self.interactive_object_service = interactive_object_service

        self.environments         = []
        self.current_env_index    = 0
        self.objects_by_env       = {}
        self.current_day          = datetime.utcnow().date()
        self._current_events_data = []

        self._init_ui()
        self._load_environments_from_db()
        self._subscribe_to_services()
        self.refresh_events()

    # -------------------------------------------------------
    # Properties
    # -------------------------------------------------------

    @property
    def current_environment_obj(self):
        """Retourne l'objet Environment courant ou None."""
        if not self.environments:
            return None
        return self.environments[self.current_env_index]

    @property
    def current_environment_id(self):
        """Retourne l'id de l'environnement courant ou None."""
        obj = self.current_environment_obj
        return obj.id if obj else None

    # -------------------------------------------------------
    # Observer — abonnements aux services
    # -------------------------------------------------------

    def _subscribe_to_services(self):
        """
        Abonne la page aux événements des services via Observer.
        Permet la mise à jour automatique de l'UI sans couplage direct.
        """
        if self.event_service:
            self.event_service.subscribe("event_created", self._on_event_changed)
            self.event_service.subscribe("event_updated", self._on_event_changed)
            self.event_service.subscribe("event_deleted", self._on_event_changed)
        if self.intention_service:
            self.intention_service.subscribe("intention_created", self._on_intention_changed)
            self.intention_service.subscribe("intention_updated", self._on_intention_changed)
            self.intention_service.subscribe("intention_deleted", self._on_intention_changed)
        if self.environment_service:
            self.environment_service.subscribe("environment_created", self._on_environment_changed)
            self.environment_service.subscribe("environment_renamed", self._on_environment_changed)
            self.environment_service.subscribe("environment_deleted", self._on_environment_deleted)

    def _on_event_changed(self, payload):
        """Rafraîchit la timeline lors de tout changement d'event."""
        self.refresh_events()

    def _on_intention_changed(self, payload):
        """Met à jour le compteur d'intentions et le focus."""
        self._refresh_intention_count()
        self._refresh_focus()

    def _on_environment_changed(self, payload):
        """Met à jour le label de l'environnement courant."""
        self._update_env_label()

    def _on_environment_deleted(self, env_id):
        """Recharge tous les environnements depuis la DB après suppression."""
        self._reload_environments()

    # -------------------------------------------------------
    # Chargement depuis la DB
    # -------------------------------------------------------

    def _load_environments_from_db(self):
        """
        Charge les environnements et leurs objets depuis la DB.
        Crée un environnement Default si aucun n'existe.
        """
        if not self.environment_service:
            return
        envs = self.environment_service.get_environments_for_owner("1")
        if not envs:
            default_env = self.environment_service.create_environment(
                owner_id="1", name="Default"
            )
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
        self._refresh_focus()

    def _reload_environments(self):
        """Nettoie les widgets existants et recharge tout depuis la DB."""
        for widgets in self.objects_by_env.values():
            for w in widgets:
                w.setParent(None)
        self.objects_by_env = {}
        self.environments   = []
        self._load_environments_from_db()
        self.refresh_events()
        self._refresh_focus()

    # -------------------------------------------------------
    # UI
    # -------------------------------------------------------

    def _init_ui(self):
        """Construit l'interface de la page de visualisation."""
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
        self.btn_prev_env   = QPushButton("←")
        self.btn_next_env   = QPushButton("→")
        self.lbl_env_name   = QLabel("...")
        self.lbl_env_name.setAlignment(Qt.AlignCenter)
        self.btn_add_env    = QPushButton("+ Env")
        self.btn_rename_env = QPushButton("✎")
        self.btn_rename_env.setToolTip("Renommer l'environnement")
        self.btn_delete_env = QPushButton("✕")
        self.btn_delete_env.setToolTip("Supprimer l'environnement")
        env_layout.addWidget(self.btn_prev_env)
        env_layout.addWidget(self.lbl_env_name)
        env_layout.addWidget(self.btn_next_env)
        env_layout.addWidget(self.btn_add_env)
        env_layout.addWidget(self.btn_rename_env)
        env_layout.addWidget(self.btn_delete_env)
        layout.addLayout(env_layout)

        self.btn_prev_env.clicked.connect(self.prev_env)
        self.btn_next_env.clicked.connect(self.next_env)
        self.btn_add_env.clicked.connect(self.add_env_dialog)
        self.btn_rename_env.clicked.connect(self.rename_env_dialog)
        self.btn_delete_env.clicked.connect(self.delete_env_dialog)

        # Zone visuelle
        self.visual_area = QFrame()
        self.visual_area.setFrameShape(QFrame.StyledPanel)
        self.visual_area.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ccc;")
        layout.addWidget(self.visual_area, stretch=1)

        # Timeline
        self.timeline = TimelineWidget()
        self.timeline.event_clicked.connect(self._on_timeline_event_clicked)
        layout.addWidget(self.timeline)

        # Compteur et focus
        self.lbl_intention_count = QLabel("Intentions : 0")
        self.lbl_intention_count.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_intention_count)

        self.lbl_focus = QLabel("★ Focus : aucun")
        self.lbl_focus.setAlignment(Qt.AlignCenter)
        self.lbl_focus.setStyleSheet("""
            background: #fffbe6; border: 1px solid #f0c040;
            border-radius: 4px; padding: 4px 10px;
            font-weight: bold; color: #7a5c00;
        """)
        layout.addWidget(self.lbl_focus)

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
        """Navigue vers l'environnement précédent."""
        if not self.environments:
            return
        self.current_env_index = (self.current_env_index - 1) % len(self.environments)
        self._update_env_label()
        self._refresh_visual_area()
        self.refresh_events()

    def next_env(self):
        """Navigue vers l'environnement suivant."""
        if not self.environments:
            return
        self.current_env_index = (self.current_env_index + 1) % len(self.environments)
        self._update_env_label()
        self._refresh_visual_area()
        self.refresh_events()

    def _update_env_label(self):
        """Met à jour le label avec le nom de l'environnement courant."""
        obj = self.current_environment_obj
        self.lbl_env_name.setText(obj.name if obj else "—")

    def add_env_dialog(self):
        """Crée un nouvel environnement via dialog."""
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

    def rename_env_dialog(self):
        """Renomme l'environnement courant via dialog."""
        env = self.current_environment_obj
        if not env:
            return
        new_name, ok = QInputDialog.getText(
            self, "Renommer l'environnement", "Nouveau nom :", text=env.name
        )
        if ok and new_name:
            self.environment_service.rename_environment(env.id, new_name)
            self.environments[self.current_env_index]._name = new_name
            self._update_env_label()

    def delete_env_dialog(self):
        """Supprime l'environnement courant après confirmation."""
        env = self.current_environment_obj
        if not env:
            return
        if len(self.environments) == 1:
            QMessageBox.warning(
                self, "Impossible",
                "Vous devez conserver au moins un environnement."
            )
            return
        confirm = QMessageBox.question(
            self, "Supprimer",
            f"Supprimer l'environnement « {env.name} » et tous ses objets ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.environment_service.delete_environment(env.id)

    # -------------------------------------------------------
    # Navigation jour
    # -------------------------------------------------------

    def go_prev_day(self):
        """Navigue au jour précédent."""
        self.current_day -= timedelta(days=1)
        self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
        self.refresh_events()

    def go_next_day(self):
        """Navigue au jour suivant."""
        self.current_day += timedelta(days=1)
        self.lbl_current_day.setText(self.current_day.strftime("%Y-%m-%d"))
        self.refresh_events()

    def select_day_dialog(self):
        """Ouvre un calendrier pour choisir un jour."""
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
    # Objets interactifs
    # -------------------------------------------------------

    def _make_widget(self, name: str, obj_id: str, position=(10, 10)) -> ObjectWidget:
        """Crée un ObjectWidget et connecte ses signaux."""
        w = ObjectWidget(name, parent=self.visual_area)
        w.obj_id   = obj_id
        w.position = position
        w.request_intention.connect(self._on_request_intention)
        w.request_rename.connect(self._on_request_rename)
        w.request_delete.connect(self._on_request_delete)
        w.moved.connect(self._on_object_moved)
        return w

    def add_object(self, name, position=(10, 10)):
        """Crée un objet interactif, le persiste et l'ajoute à la zone visuelle."""
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
        """
        Rafraîchit la zone visuelle en affichant uniquement
        les objets de l'environnement courant.
        Clampe les positions dans les limites de la zone.
        """
        for widgets in self.objects_by_env.values():
            for w in widgets:
                w.setParent(None)

        env_id = self.current_environment_id
        if not env_id:
            return

        area_w = self.visual_area.width()
        area_h = self.visual_area.height()

        for w in self.objects_by_env.get(env_id, []):
            w.setParent(self.visual_area)
            x, y = getattr(w, 'position', (10, 10))
            x = max(0, min(x, max(area_w - w.width(),  0)))
            y = max(0, min(y, max(area_h - w.height(), 0)))
            w.position = (x, y)
            w.move(x, y)
            w.show()

    def create_object_dialog(self):
        """Crée un nouvel objet interactif via dialog."""
        name, ok = QInputDialog.getText(self, "Nouvel objet", "Nom de l'objet :")
        if ok and name:
            self.add_object(name, position=(10, 10))

    def _find_widget_by_id(self, obj_id: str):
        """Retourne le widget correspondant à un obj_id ou None."""
        for w in self.objects_by_env.get(self.current_environment_id, []):
            if w.obj_id == obj_id:
                return w
        return None

    def _on_request_intention(self, obj_id: str):
        """Crée une intention liée à l'objet cliqué."""
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
        """Renomme l'objet sélectionné."""
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
        """Supprime l'objet sélectionné après confirmation."""
        w = self._find_widget_by_id(obj_id)
        if not w:
            return
        confirm = QMessageBox.question(
            self, "Supprimer", f"Supprimer « {w.obj_name} » ?",
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
        """Persiste la nouvelle position d'un objet après drag."""
        env = self.current_environment_obj
        if not env or not self.interactive_object_service:
            return
        self.interactive_object_service.update_object_position(
            environment_id=env.id,
            object_id=obj_id,
            position=(x, y)
        )

    # -------------------------------------------------------
    # Timeline
    # -------------------------------------------------------

    def _on_timeline_event_clicked(self, event_id: str):
        """Ouvre EventDialog au clic sur un event de la timeline."""
        event_data = next(
            (e for e in self._current_events_data if e["id"] == event_id), None
        )
        if not event_data:
            return
        dialog = EventDialog(
            parent=self,
            event_data=event_data,
            event_service=self.event_service
        )
        dialog.exec()

    # -------------------------------------------------------
    # Intentions et focus
    # -------------------------------------------------------

    def _refresh_intention_count(self):
        """Met à jour le compteur d'intentions."""
        if self.intention_service:
            count = len(self.intention_service.get_all_intentions())
            self.lbl_intention_count.setText(f"Intentions : {count}")

    def open_intention_manager(self):
        """Ouvre le dialog de gestion des intentions."""
        if not self.intention_service:
            return
        dialog = IntentionManagerDialog(
            parent=self,
            intention_service=self.intention_service,
            event_service=self.event_service,
            current_env_id=self.current_environment_id,
            current_day=self.current_day
        )
        dialog.exec()

    def _refresh_focus(self):
        """
        Met à jour le label focus et la surbrillance de la timeline
        selon l'intention active de l'utilisateur.
        """
        if not self.intention_service:
            return
        active = self.intention_service.get_active_intention_by_user("1")
        if active:
            self.timeline.set_active_intention(active.id)
            self.lbl_focus.setText(f"★ Focus : {active.title}")
            self.lbl_focus.setStyleSheet("""
                background: #fffbe6; border: 1px solid #f0c040;
                border-radius: 4px; padding: 4px 10px;
                font-weight: bold; color: #7a5c00;
            """)
        else:
            self.timeline.set_active_intention(None)
            self.lbl_focus.setText("★ Focus : aucun")
            self.lbl_focus.setStyleSheet("""
                background: #f0f0f0; border: 1px solid #ccc;
                border-radius: 4px; padding: 4px 10px; color: #999;
            """)

    # -------------------------------------------------------
    # Refresh events
    # -------------------------------------------------------

    def refresh_events(self):
        """
        Récupère les events du jour et de l'environnement courant
        et les charge dans la timeline.
        """
        env_id = self.current_environment_id
        if not env_id or not self.event_service or not self.intention_service:
            self.timeline.load_events([])
            self._refresh_focus()
            return

        start_day = datetime.combine(self.current_day, datetime.min.time())
        end_day   = datetime.combine(self.current_day, datetime.max.time())

        events         = self.event_service.get_events_between(env_id, start_day, end_day)
        intentions_map = self.intention_service.get_intentions_map()

        ui_events = []
        for ev in events:
            intention = intentions_map.get(ev.intention_id)
            ui_events.append({
                "id":              ev.id,
                "intention_id":    ev.intention_id,
                "name":            intention.title if intention else "Unknown",
                "start_hour":      ev.start_time.hour + ev.start_time.minute / 60,
                "duration_hour":   ev.duration / 60,
                "start_time":      ev.start_time.strftime("%H:%M"),
                "start_time_full": ev.start_time.isoformat(),
                "duration":        ev.duration,
                "status":          ev.status,
            })

        self._current_events_data = ui_events
        self.timeline.load_events(ui_events)
        self._refresh_focus()

    # -------------------------------------------------------
    # Responsive
    # -------------------------------------------------------

    def resizeEvent(self, event):
        """Reclampe les objets dans les limites lors du redimensionnement."""
        super().resizeEvent(event)
        self._clamp_all_objects()

    def _clamp_all_objects(self):
        """Ramène tous les objets dans les limites de la zone visuelle."""
        area_w = self.visual_area.width()
        area_h = self.visual_area.height()
        if area_w <= 0 or area_h <= 0:
            return

        for widgets in self.objects_by_env.values():
            for w in widgets:
                x, y  = w.position
                new_x = max(0, min(x, area_w - w.width()))
                new_y = max(0, min(y, area_h - w.height()))
                if (new_x, new_y) != (x, y):
                    w.position = (new_x, new_y)
                    if w.parent() == self.visual_area:
                        w.move(new_x, new_y)