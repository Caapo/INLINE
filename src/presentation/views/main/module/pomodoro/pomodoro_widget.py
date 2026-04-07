# INLINE/src/presentation/views/main/module/pomodoro_widget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from datetime import datetime
from domain.enums.enums import SessionStatus


class PomodoroWidget(QWidget):
    """
    Widget interactif du timer Pomodoro.
    Gère l'affichage et la logique du timer, des phases
    (travail/pause/longue pause) et des indicateurs de session.
    Émet session_ended à chaque fin de phase pour permettre
    la persistance via ModuleDetailPanel.
    """

    session_ended = Signal(int, int, str)  # work_duration, break_duration, status

    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.module              = module
        self._timer              = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._seconds_left       = 0
        self._is_work_phase      = True
        self._sessions_done      = 0
        self._current_work_start = None
        self._elapsed_work       = 0
        self._elapsed_break      = 0
        self._running            = False

        self._init_ui()
        self._reset()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        self.lbl_module_name = QLabel(self.module.name)
        self.lbl_module_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_module_name)

        self.lbl_phase = QLabel("TRAVAIL")
        self.lbl_phase.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_phase)

        self.lbl_timer = QLabel("25:00")
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(64)
        font.setBold(True)
        self.lbl_timer.setFont(font)
        layout.addWidget(self.lbl_timer)

        self.lbl_sessions = QLabel("Session 1 / 4")
        self.lbl_sessions.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_sessions)

        self.dots_layout = QHBoxLayout()
        self.dots_layout.setAlignment(Qt.AlignCenter)
        self._dots = []
        layout.addLayout(self.dots_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(12)

        self.btn_start_pause = QPushButton("▶  Démarrer")
        self.btn_skip        = QPushButton("⏭  Passer")
        self.btn_stop        = QPushButton("⏹  Arrêter")

        for btn in [self.btn_start_pause, self.btn_skip, self.btn_stop]:
            btn.setFixedHeight(40)
            btn.setMinimumWidth(130)

        btn_layout.addWidget(self.btn_start_pause)
        btn_layout.addWidget(self.btn_skip)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)

        self.lbl_stats = QLabel("")
        self.lbl_stats.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_stats)

        lbl_hist = QLabel("Historique du jour")
        lbl_hist.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_hist)

        self.lbl_history = QLabel("—")
        self.lbl_history.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_history)

        self.btn_start_pause.clicked.connect(self._toggle_start_pause)
        self.btn_skip.clicked.connect(self._skip_phase)
        self.btn_stop.clicked.connect(self._stop)

    def load_module(self, module):
        """Charge un nouveau module et réinitialise le timer."""
        self.module = module
        self.lbl_module_name.setText(module.name)
        self._reset()

    def update_history(self, sessions):
        """Met à jour l'affichage de l'historique du jour."""
        if not sessions:
            self.lbl_history.setText("Aucune session aujourd'hui")
            return
        completed  = sum(1 for s in sessions if s.status == SessionStatus.COMPLETED.value)
        total_work = sum(s.work_duration for s in sessions
                        if s.status == SessionStatus.COMPLETED.value)
        self.lbl_history.setText(
            f"{completed} session(s) complétée(s) — {total_work} min travaillées"
        )

    def _reset(self):
        """Réinitialise le timer à son état initial."""
        self._timer.stop()
        self._is_work_phase      = True
        self._sessions_done      = 0
        self._elapsed_work       = 0
        self._elapsed_break      = 0
        self._running            = False
        self._seconds_left       = self.module.work_minutes * 60
        self._update_display()
        self._rebuild_dots()
        self.btn_start_pause.setText("▶  Démarrer")
        self.lbl_stats.setText("")

    def _rebuild_dots(self):
        """Reconstruit les indicateurs de session (cercles)."""
        for d in self._dots:
            d.setParent(None)
        self._dots.clear()
        for _ in range(self.module.sessions_before_long):
            dot = QLabel("○")
            self.dots_layout.addWidget(dot)
            self._dots.append(dot)
        self._update_dots()

    def _update_dots(self):
        """Met à jour l'état visuel des indicateurs de session."""
        for i, dot in enumerate(self._dots):
            if i < self._sessions_done % self.module.sessions_before_long:
                dot.setText("●")
            else:
                dot.setText("○")

    def _toggle_start_pause(self):
        """Démarre ou met en pause le timer."""
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
        """Décrémente le timer d'une seconde et détecte la fin de phase."""
        if self._seconds_left > 0:
            self._seconds_left -= 1
            if self._is_work_phase:
                self._elapsed_work  += 1
            else:
                self._elapsed_break += 1
            self._update_display()
        else:
            self._phase_complete()

    def _phase_complete(self):
        """Gère la fin d'une phase (travail ou pause)."""
        self._timer.stop()
        self._running = False

        if self._is_work_phase:
            self._sessions_done += 1
            self._update_dots()
            self._is_work_phase = False

            if self._sessions_done % self.module.sessions_before_long == 0:
                self._seconds_left = self.module.long_break_minutes * 60
                self.lbl_phase.setText("LONGUE PAUSE")
            else:
                self._seconds_left = self.module.break_minutes * 60
                self.lbl_phase.setText("PAUSE")

            self._update_display()
            self._update_sessions_label()
            self.btn_start_pause.setText("▶  Démarrer la pause")

            # Émet la session de travail complétée
            self.session_ended.emit(
                max(1, self._elapsed_work // 60),
                0,
                SessionStatus.COMPLETED.value
            )
            self._elapsed_work = 0

        else:
            # Fin de pause → retour au travail sans enregistrement
            self._elapsed_break = 0
            self._is_work_phase = True
            self._seconds_left  = self.module.work_minutes * 60
            self.lbl_phase.setText("TRAVAIL")
            self._update_display()
            self._update_sessions_label()
            self.btn_start_pause.setText("▶  Démarrer")

    def _skip_phase(self):
        """Passe la phase courante en émettant une session interrompue si nécessaire."""
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
        """Arrête le timer et enregistre la session interrompue si du temps a été passé."""
        self._timer.stop()
        if self._elapsed_work > 0 or self._elapsed_break > 0:
            self.session_ended.emit(
                max(1, self._elapsed_work  // 60) if self._elapsed_work  > 0 else 0,
                max(1, self._elapsed_break // 60) if self._elapsed_break > 0 else 0,
                SessionStatus.INTERRUPTED.value
            )
        self._elapsed_work       = 0
        self._elapsed_break      = 0
        self._current_work_start = None
        self._reset()

    def _update_display(self):
        """Met à jour l'affichage du timer."""
        mins = self._seconds_left // 60
        secs = self._seconds_left % 60
        self.lbl_timer.setText(f"{mins:02d}:{secs:02d}")

    def _update_sessions_label(self):
        """Met à jour le label de progression des sessions."""
        session_num = (self._sessions_done % self.module.sessions_before_long) + 1
        self.lbl_sessions.setText(
            f"Session {session_num} / {self.module.sessions_before_long}"
        )