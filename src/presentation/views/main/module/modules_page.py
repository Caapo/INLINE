# ======= INLINE/src/presentation/views/main/module/modules_page.py =======

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QSplitter, QFrame,
    QInputDialog, QMessageBox, QScrollArea, QSizePolicy,
    QSpinBox, QFormLayout, QDialog, QDialogButtonBox,
    QStackedWidget
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QColor
from datetime import datetime
from domain.enums.enums import SessionStatus


# =============================================================
# Dialog de création d'un module Pomodoro
# =============================================================

class CreatePomodoroDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau module Pomodoro")
        self.resize(360, 280)
        # self.setStyleSheet("""
        #     QDialog { background: #1e1e2e; color: white; }
        #     QLabel  { color: #ccc; }
        #     QSpinBox {
        #         background: #2a2a3e; color: white;
        #         border: 1px solid #444; border-radius: 4px; padding: 4px;
        #     }
        #     QLineEdit {
        #         background: #2a2a3e; color: white;
        #         border: 1px solid #444; border-radius: 4px; padding: 6px;
        #     }
        # """)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        form.setSpacing(12)

        from PySide6.QtWidgets import QLineEdit
        self.name_edit = QLineEdit("Mon Pomodoro")
        # self.name_edit.setStyleSheet("""
        #     QLineEdit { background: #2a2a3e; color: white;
        #                 border: 1px solid #444; border-radius: 4px; padding: 6px; }
        # """)

        self.work_spin = QSpinBox()
        self.work_spin.setRange(1, 120)
        self.work_spin.setValue(25)
        self.work_spin.setSuffix(" min")

        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 60)
        self.break_spin.setValue(5)
        self.break_spin.setSuffix(" min")

        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 120)
        self.long_break_spin.setValue(15)
        self.long_break_spin.setSuffix(" min")

        self.sessions_spin = QSpinBox()
        self.sessions_spin.setRange(1, 20)
        self.sessions_spin.setValue(4)
        self.sessions_spin.setSuffix(" sessions")

        form.addRow("Nom :",                    self.name_edit)
        form.addRow("Travail :",                self.work_spin)
        form.addRow("Pause courte :",           self.break_spin)
        form.addRow("Pause longue :",           self.long_break_spin)
        form.addRow("Sessions avant longue pause :", self.sessions_spin)

        layout.addLayout(form)
        layout.addStretch()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        # btns.setStyleSheet("""
        #     QPushButton { background: #4A90D9; color: white; border-radius: 4px;
        #                   padding: 6px 16px; font-weight: bold; }
        #     QPushButton:hover { background: #357abd; }
        # """)
        layout.addWidget(btns)

    def get_values(self) -> dict:
        return {
            "name":                 self.name_edit.text().strip() or "Mon Pomodoro",
            "work_minutes":         self.work_spin.value(),
            "break_minutes":        self.break_spin.value(),
            "long_break_minutes":   self.long_break_spin.value(),
            "sessions_before_long": self.sessions_spin.value()
        }


# =============================================================
# Widget Pomodoro — le timer interactif
# =============================================================

class PomodoroWidget(QWidget):
    session_ended = Signal(int, int, str)  # work_duration, break_duration, status

    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.module               = module
        self._timer               = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._seconds_left        = 0
        self._is_work_phase       = True
        self._sessions_done       = 0
        self._current_work_start  = None
        self._elapsed_work        = 0
        self._elapsed_break       = 0
        self._running             = False

        self._init_ui()
        self._reset()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        # Titre du module
        self.lbl_module_name = QLabel(self.module.name)
        self.lbl_module_name.setAlignment(Qt.AlignCenter)
        # self.lbl_module_name.setStyleSheet(
        #     "font-size: 20px; font-weight: bold; color: white;"
        # )
        layout.addWidget(self.lbl_module_name)

        # Phase (TRAVAIL / PAUSE)
        self.lbl_phase = QLabel("TRAVAIL")
        self.lbl_phase.setAlignment(Qt.AlignCenter)
        # self.lbl_phase.setStyleSheet(
        #     "font-size: 13px; font-weight: bold; color: #4A90D9; letter-spacing: 3px;"
        # )
        layout.addWidget(self.lbl_phase)

        # Timer
        self.lbl_timer = QLabel("25:00")
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(64)
        font.setBold(True)
        self.lbl_timer.setFont(font)
        # self.lbl_timer.setStyleSheet("color: white;")
        layout.addWidget(self.lbl_timer)

        # Compteur sessions
        self.lbl_sessions = QLabel("Session 1 / 4")
        self.lbl_sessions.setAlignment(Qt.AlignCenter)
        # self.lbl_sessions.setStyleSheet("color: #aaa; font-size: 13px;")
        layout.addWidget(self.lbl_sessions)

        # Indicateurs sessions (cercles)
        self.dots_layout = QHBoxLayout()
        self.dots_layout.setAlignment(Qt.AlignCenter)
        self._dots = []
        layout.addLayout(self.dots_layout)

        # Boutons contrôle
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(12)

        self.btn_start_pause = QPushButton("▶  Démarrer")
        self.btn_skip        = QPushButton("⏭  Passer")
        self.btn_stop        = QPushButton("⏹  Arrêter")

        for btn in [self.btn_start_pause, self.btn_skip, self.btn_stop]:
            btn.setFixedHeight(40)
            btn.setMinimumWidth(130)
            # btn.setStyleSheet("""
            #     QPushButton {
            #         background: #2a2a3e; color: white;
            #         border: 1px solid #444; border-radius: 8px;
            #         font-size: 13px; font-weight: bold;
            #     }
            #     QPushButton:hover { background: #3a3a5c; }
            # """)

        # self.btn_start_pause.setStyleSheet("""
        #     QPushButton {
        #         background: #4A90D9; color: white;
        #         border-radius: 8px; font-size: 13px; font-weight: bold;
        #     }
        #     QPushButton:hover { background: #357abd; }
        # """)

        btn_layout.addWidget(self.btn_start_pause)
        btn_layout.addWidget(self.btn_skip)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)

        # Stats de la session en cours
        self.lbl_stats = QLabel("")
        self.lbl_stats.setAlignment(Qt.AlignCenter)
        # self.lbl_stats.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.lbl_stats)

        # Historique rapide
        lbl_hist = QLabel("Historique du jour")
        lbl_hist.setAlignment(Qt.AlignCenter)
        # lbl_hist.setStyleSheet("color: #888; font-size: 11px; margin-top: 8px;")
        layout.addWidget(lbl_hist)

        self.lbl_history = QLabel("—")
        self.lbl_history.setAlignment(Qt.AlignCenter)
        # self.lbl_history.setStyleSheet("color: #aaa; font-size: 12px;")
        layout.addWidget(self.lbl_history)

        # Connexions
        self.btn_start_pause.clicked.connect(self._toggle_start_pause)
        self.btn_skip.clicked.connect(self._skip_phase)
        self.btn_stop.clicked.connect(self._stop)

    def load_module(self, module):
        self.module = module
        self.lbl_module_name.setText(module.name)
        self._reset()

    def update_history(self, sessions):
        if not sessions:
            self.lbl_history.setText("Aucune session aujourd'hui")
            return
        completed   = sum(1 for s in sessions if s.status == SessionStatus.COMPLETED.value)
        total_work  = sum(s.work_duration for s in sessions
                         if s.status == SessionStatus.COMPLETED.value)
        self.lbl_history.setText(
            f"{completed} session(s) complétée(s) — {total_work} min travaillées"
        )

    def _reset(self):
        self._timer.stop()
        self._is_work_phase   = True
        self._sessions_done   = 0
        self._elapsed_work    = 0
        self._elapsed_break   = 0
        self._running         = False
        self._seconds_left    = self.module.work_minutes * 60
        self._update_display()
        self._rebuild_dots()
        self.btn_start_pause.setText("▶  Démarrer")
        self.lbl_stats.setText("")

    def _rebuild_dots(self):
        for d in self._dots:
            d.setParent(None)
        self._dots.clear()
        for i in range(self.module.sessions_before_long):
            dot = QLabel("○")
            # dot.setStyleSheet("color: #444; font-size: 18px;")
            self.dots_layout.addWidget(dot)
            self._dots.append(dot)
        self._update_dots()

    def _update_dots(self):
        for i, dot in enumerate(self._dots):
            if i < self._sessions_done % self.module.sessions_before_long:
                dot.setText("●")
                # dot.setStyleSheet("color: #4A90D9; font-size: 18px;")
            else:
                dot.setText("○")
                # dot.setStyleSheet("color: #444; font-size: 18px;")

    def _toggle_start_pause(self):
        if self._running:
            self._timer.stop()
            self._running = False
            self.btn_start_pause.setText("▶  Reprendre")
        else:
            if not self._current_work_start:
                self._current_work_start = datetime.utcnow()
            self._timer.start(1000)
            self._running = True
            self.btn_start_pause.setText("⏸  Pause")

    def _tick(self):
        if self._seconds_left > 0:
            self._seconds_left -= 1
            if self._is_work_phase:
                self._elapsed_work += 1
            else:
                self._elapsed_break += 1
            self._update_display()
        else:
            self._phase_complete()

    def _phase_complete(self):
        self._timer.stop()
        self._running = False

        if self._is_work_phase:
            # Fin de la phase travail → pause
            self._sessions_done += 1
            self._update_dots()
            self._is_work_phase = False

            # Longue pause ou courte pause
            if self._sessions_done % self.module.sessions_before_long == 0:
                self._seconds_left = self.module.long_break_minutes * 60
                self.lbl_phase.setText("LONGUE PAUSE")
                # self.lbl_phase.setStyleSheet(
                #     "font-size: 13px; font-weight: bold; color: #50c878; letter-spacing: 3px;"
                # )
            else:
                self._seconds_left = self.module.break_minutes * 60
                self.lbl_phase.setText("PAUSE")
                # self.lbl_phase.setStyleSheet(
                #     "font-size: 13px; font-weight: bold; color: #f0a500; letter-spacing: 3px;"
                # )

            self._update_display()
            self._update_sessions_label()
            self.btn_start_pause.setText("▶  Démarrer la pause")

            # Fin de phase travail
            self.session_ended.emit(
                max(1, self._elapsed_work // 60),   # au moins 1 minute
                0,
                SessionStatus.COMPLETED.value
            )
            self._elapsed_work = 0

        else:
            # Fin de la pause → nouvelle session travail
            self.session_ended.emit(
                0,
                max(1, self._elapsed_break // 60),  # au moins 1 minute
                SessionStatus.COMPLETED.value
            )
            self._elapsed_break = 0
            self._elapsed_break = 0
            self._is_work_phase = True
            self._seconds_left  = self.module.work_minutes * 60
            self.lbl_phase.setText("TRAVAIL")
            # self.lbl_phase.setStyleSheet(
            #     "font-size: 13px; font-weight: bold; color: #4A90D9; letter-spacing: 3px;"
            # )
            self._update_display()
            self._update_sessions_label()
            self.btn_start_pause.setText("▶  Démarrer")

    def _skip_phase(self):
        self._timer.stop()
        self._running = False
        if self._is_work_phase and self._elapsed_work > 0:
            self.session_ended.emit(
                max(1, self._elapsed_work // 60),
                0,
                SessionStatus.INTERRUPTED.value
            )
            self._elapsed_work = 0
        elif not self._is_work_phase and self._elapsed_break > 0:
            self.session_ended.emit(
                0,
                max(1, self._elapsed_break // 60),
                SessionStatus.INTERRUPTED.value
            )
            self._elapsed_break = 0
        self._phase_complete()


    def _stop(self):
        self._timer.stop()
        if self._elapsed_work > 0 or self._elapsed_break > 0:
            self.session_ended.emit(
                max(1, self._elapsed_work // 60) if self._elapsed_work > 0 else 0,
                max(1, self._elapsed_break // 60) if self._elapsed_break > 0 else 0,
                SessionStatus.INTERRUPTED.value
            )
        self._elapsed_work       = 0
        self._elapsed_break      = 0
        self._current_work_start = None
        self._reset()

    def _update_display(self):
        mins = self._seconds_left // 60
        secs = self._seconds_left % 60
        self.lbl_timer.setText(f"{mins:02d}:{secs:02d}")

    def _update_sessions_label(self):
        session_num = (self._sessions_done % self.module.sessions_before_long) + 1
        self.lbl_sessions.setText(
            f"Session {session_num} / {self.module.sessions_before_long}"
        )


# =============================================================
# Panneau de détails / config d'un module
# =============================================================

class ModuleDetailPanel(QWidget):
    def __init__(self, module_service, intention_service, parent=None):
        super().__init__(parent)
        self.module_service    = module_service
        self.intention_service = intention_service
        self.current_module    = None
        self._started_at       = None

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Page 0 : placeholder vide
        empty = QLabel("Sélectionnez un module")
        empty.setAlignment(Qt.AlignCenter)
        # empty.setStyleSheet("color: #555; font-size: 16px;")
        self.stack.addWidget(empty)

        # Page 1 : pomodoro
        self.pomodoro_widget = PomodoroWidget(
            module=_DummyModule(),
            parent=self
        )
        # self.pomodoro_widget.setStyleSheet("background: #13131f;")
        self.pomodoro_widget.session_ended.connect(self._on_session_ended)
        self.stack.addWidget(self.pomodoro_widget)

        self.stack.setCurrentIndex(0)

    def load_module(self, module):
        self.current_module = module
        self.pomodoro_widget.load_module(module)

        # Charge l'historique du jour
        from datetime import date
        sessions = self.module_service.get_sessions_for_module_and_date(
            module.id, date.today()
        )
        self.pomodoro_widget.update_history(sessions)
        self.stack.setCurrentIndex(1)

    def _on_session_ended(self, work_duration: int, break_duration: int, status: str):
        if not self.current_module:
            return
        # On enregistre dès qu'il y a au moins une des deux durées > 0
        if work_duration <= 0 and break_duration <= 0:
            return

        self.module_service.record_session(
            module_id=self.current_module.id,
            work_duration=work_duration,
            break_duration=break_duration,
            status=status,
            started_at=self._started_at or datetime.utcnow(),
            ended_at=datetime.utcnow()
        )
        self._started_at = None

        from datetime import date
        sessions = self.module_service.get_sessions_for_module_and_date(self.current_module.id, date.today())
        self.pomodoro_widget.update_history(sessions)


class _DummyModule:
    """Module factice pour initialiser PomodoroWidget sans données réelles."""
    name                 = ""
    work_minutes         = 25
    break_minutes        = 5
    long_break_minutes   = 15
    sessions_before_long = 4


# =============================================================
# ModulesPage
# =============================================================

class ModulesPage(QWidget):
    def __init__(self, module_service=None, intention_service=None, parent=None):
        super().__init__(parent)
        self.module_service    = module_service
        self.intention_service = intention_service
        self._init_ui()
        self._subscribe()
        self._load_modules()

    def _init_ui(self):
        self.setStyleSheet("background-color: #13131f;")
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- Panneau gauche ----
        left_panel = QFrame()
        left_panel.setFixedWidth(260)
        # left_panel.setStyleSheet("""
        #     QFrame { background: #1e1e2e; border-right: 1px solid #2a2a3e; }
        # """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 16, 12, 12)
        left_layout.setSpacing(8)

        lbl = QLabel("Modules")
        # lbl.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(lbl)

        # Filtre intention
        from PySide6.QtWidgets import QComboBox
        self.filter_combo = QComboBox()
        # self.filter_combo.setStyleSheet("""
        #     QComboBox { background: #2a2a3e; color: #ccc; border: 1px solid #444;
        #                 border-radius: 4px; padding: 4px; }
        #     QComboBox::drop-down { border: none; }
        #     QComboBox QAbstractItemView { background: #2a2a3e; color: white; }
        # """)
        self.filter_combo.addItem("Tous les modules", None)
        self.filter_combo.currentIndexChanged.connect(self._apply_filter)
        left_layout.addWidget(self.filter_combo)

        # Liste
        self.module_list = QListWidget()
        # self.module_list.setStyleSheet("""
        #     QListWidget { background: transparent; border: none; color: white; }
        #     QListWidget::item { padding: 10px 8px; border-radius: 6px; margin: 2px 0; }
        #     QListWidget::item:selected { background: #3a3a5c; }
        #     QListWidget::item:hover { background: #2a2a4a; }
        # """)
        self.module_list.currentItemChanged.connect(self._on_module_selected)
        left_layout.addWidget(self.module_list, stretch=1)

        # Boutons
        btn_new = QPushButton("+ Nouveau Pomodoro")
        # btn_new.setStyleSheet("""
        #     QPushButton { background: #4A90D9; color: white; font-weight: bold;
        #                   border-radius: 6px; padding: 8px; }
        #     QPushButton:hover { background: #357abd; }
        # """)
        btn_new.clicked.connect(self._create_module)
        left_layout.addWidget(btn_new)

        # Boutons rename / link / delete
        action_layout = QHBoxLayout()

        btn_rename = QPushButton("✎")
        btn_rename.setToolTip("Renommer")
        btn_rename.setFixedHeight(32)
        # btn_rename.setStyleSheet("""
        #     QPushButton { background: #2a2a3e; color: #ccc;
        #                   border: 1px solid #444; border-radius: 4px; }
        #     QPushButton:hover { background: #3a3a5c; }
        # """)
        btn_rename.clicked.connect(self._rename_module)

        btn_link = QPushButton("🔗")
        btn_link.setToolTip("Lier à une intention")
        btn_link.setFixedHeight(32)
        # btn_link.setStyleSheet("""
        #     QPushButton { background: #2a2a3e; color: #4A90D9;
        #                   border: 1px solid #4A90D9; border-radius: 4px; }
        #     QPushButton:hover { background: #3a3a5c; }
        # """)
        btn_link.clicked.connect(self._link_intention)

        btn_unlink = QPushButton("✕🔗")
        btn_unlink.setToolTip("Délier l'intention")
        btn_unlink.setFixedHeight(32)
        # btn_unlink.setStyleSheet("""
        #     QPushButton { background: #2a2a3e; color: #cc4444;
        #                   border: 1px solid #cc4444; border-radius: 4px; }
        #     QPushButton:hover { background: #3a2020; }
        # """)
        btn_unlink.clicked.connect(self._unlink_intention)

        btn_delete = QPushButton("🗑")
        btn_delete.setToolTip("Supprimer")
        btn_delete.setFixedHeight(32)
        # btn_delete.setStyleSheet("""
        #     QPushButton { background: #2a2a3e; color: #cc4444;
        #                   border: 1px solid #cc4444; border-radius: 4px; }
        #     QPushButton:hover { background: #3a2020; }
        # """)
        btn_delete.clicked.connect(self._delete_module)

        action_layout.addWidget(btn_rename)
        action_layout.addWidget(btn_link)
        action_layout.addWidget(btn_unlink)
        action_layout.addWidget(btn_delete)
        left_layout.addLayout(action_layout)

        # Config rapide
        btn_config = QPushButton("⚙  Configurer")
        # btn_config.setStyleSheet("""
        #     QPushButton { background: #2a2a3e; color: #ccc;
        #                   border: 1px solid #444; border-radius: 6px; padding: 6px; }
        #     QPushButton:hover { background: #3a3a5c; }
        # """)
        btn_config.clicked.connect(self._configure_module)
        left_layout.addWidget(btn_config)

        # ---- Panneau droit ----
        self.detail_panel = ModuleDetailPanel(
            module_service=self.module_service,
            intention_service=self.intention_service
        )
        self.detail_panel.setStyleSheet("background: #13131f;")

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.detail_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setHandleWidth(1)
        # splitter.setStyleSheet("QSplitter::handle { background: #2a2a3e; }")

        main_layout.addWidget(splitter)

    def _subscribe(self):
        if self.module_service:
            self.module_service.subscribe("module_created",  self._on_module_changed)
            self.module_service.subscribe("module_updated",  self._on_module_updated)
            self.module_service.subscribe("module_deleted",  self._on_module_changed)

    def _on_module_changed(self, payload):
        self._load_modules()

    def _on_module_updated(self, module):
        for i in range(self.module_list.count()):
            item = self.module_list.item(i)
            if item.data(Qt.UserRole) == module.id:
                suffix = " 🔗" if module.intention_id else ""
                item.setText(f"🍅 {module.name}{suffix}")
                break

    def _load_modules(self):
        self.module_list.clear()
        if not self.module_service:
            return

        # Recharge le filtre
        current_filter = self.filter_combo.currentData()
        self.filter_combo.blockSignals(True)
        self.filter_combo.clear()
        self.filter_combo.addItem("Tous les modules", None)
        if self.intention_service:
            for i in self.intention_service.get_all_intentions():
                self.filter_combo.addItem(f"📌 {i.title}", i.id)
        self.filter_combo.blockSignals(False)

        for i in range(self.filter_combo.count()):
            if self.filter_combo.itemData(i) == current_filter:
                self.filter_combo.setCurrentIndex(i)
                break

        self._apply_filter()

    def _apply_filter(self):
        self.module_list.clear()
        if not self.module_service:
            return

        intention_id = self.filter_combo.currentData()
        if intention_id:
            modules = self.module_service.get_modules_for_intention(intention_id)
        else:
            modules = self.module_service.get_modules_for_user("1")

        for module in modules:
            suffix = " 🔗" if module.intention_id else ""
            item   = QListWidgetItem(f"🍅 {module.name}{suffix}")
            item.setData(Qt.UserRole, module.id)
            if module.intention_id:
                item.setForeground(QColor("#4A90D9"))
            self.module_list.addItem(item)

    def _on_module_selected(self, item):
        if not item:
            return
        module_id = item.data(Qt.UserRole)
        module    = self.module_service.get_module(module_id)
        if module:
            self.detail_panel.load_module(module)

    def _create_module(self):
        dialog = CreatePomodoroDialog(self)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_values()
            self.module_service.create_pomodoro(
                owner_id="1",
                **values
            )

    def _selected_module(self):
        item = self.module_list.currentItem()
        if not item:
            return None
        return self.module_service.get_module(item.data(Qt.UserRole))

    def _rename_module(self):
        module = self._selected_module()
        if not module:
            return
        new_name, ok = QInputDialog.getText(
            self, "Renommer", "Nouveau nom :", text=module.name
        )
        if ok and new_name:
            self.module_service.rename_module(module.id, new_name)
            if self.detail_panel.current_module and \
               self.detail_panel.current_module.id == module.id:
                self.detail_panel.pomodoro_widget.lbl_module_name.setText(new_name)

    def _link_intention(self):
        module = self._selected_module()
        if not module or not self.intention_service:
            return
        intentions = self.intention_service.get_all_intentions()
        if not intentions:
            QMessageBox.information(self, "Info", "Aucune intention disponible.")
            return
        choices = [i.title for i in intentions]
        choice, ok = QInputDialog.getItem(
            self, "Lier à une intention", "Choisir :", choices, 0, False
        )
        if ok and choice:
            intention = next(i for i in intentions if i.title == choice)
            self.module_service.attach_to_intention(module.id, intention.id)

    def _unlink_intention(self):
        module = self._selected_module()
        if not module or not module.intention_id:
            return
        self.module_service.detach_from_intention(module.id)

    def _delete_module(self):
        module = self._selected_module()
        if not module:
            return
        confirm = QMessageBox.question(
            self, "Supprimer",
            f"Supprimer le module « {module.name} » et tout son historique ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.module_service.delete_module(module.id)
            self.detail_panel.stack.setCurrentIndex(0)

    def _configure_module(self):
        module = self._selected_module()
        if not module:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Configurer — {module.name}")
        dialog.resize(320, 260)
        # dialog.setStyleSheet("""
        #     QDialog { background: #1e1e2e; color: white; }
        #     QLabel  { color: #ccc; }
        #     QSpinBox {
        #         background: #2a2a3e; color: white;
        #         border: 1px solid #444; border-radius: 4px; padding: 4px;
        #     }
        # """)

        layout = QVBoxLayout(dialog)
        form   = QFormLayout()
        form.setSpacing(12)

        work_spin = QSpinBox()
        work_spin.setRange(1, 120)
        work_spin.setValue(module.work_minutes)
        work_spin.setSuffix(" min")

        break_spin = QSpinBox()
        break_spin.setRange(1, 60)
        break_spin.setValue(module.break_minutes)
        break_spin.setSuffix(" min")

        long_break_spin = QSpinBox()
        long_break_spin.setRange(1, 120)
        long_break_spin.setValue(module.long_break_minutes)
        long_break_spin.setSuffix(" min")

        sessions_spin = QSpinBox()
        sessions_spin.setRange(1, 20)
        sessions_spin.setValue(module.sessions_before_long)
        sessions_spin.setSuffix(" sessions")

        form.addRow("Travail :",                work_spin)
        form.addRow("Pause courte :",           break_spin)
        form.addRow("Pause longue :",           long_break_spin)
        form.addRow("Sessions avant longue pause :", sessions_spin)

        layout.addLayout(form)
        layout.addStretch()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        # btns.setStyleSheet("""
        #     QPushButton { background: #4A90D9; color: white; border-radius: 4px;
        #                   padding: 6px 16px; font-weight: bold; }
        #     QPushButton:hover { background: #357abd; }
        # """)
        layout.addWidget(btns)

        if dialog.exec() == QDialog.Accepted:
            self.module_service.update_config(
                module.id,
                work_minutes=work_spin.value(),
                break_minutes=break_spin.value(),
                long_break_minutes=long_break_spin.value(),
                sessions_before_long=sessions_spin.value()
            )
            # Recharge le module dans le panneau si c'est le module actif
            if self.detail_panel.current_module and \
               self.detail_panel.current_module.id == module.id:
                updated = self.module_service.get_module(module.id)
                self.detail_panel.load_module(updated)