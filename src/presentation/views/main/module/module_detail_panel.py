# INLINE/src/presentation/views/main/module/module_detail_panel.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from datetime import datetime, date
from presentation.views.main.module.pomodoro.pomodoro_widget import PomodoroWidget


class _DummyModule:
    """
    Module factice pour initialiser PomodoroWidget
    sans données réelles avant la sélection d'un module.
    """
    name                 = ""
    work_minutes         = 25
    break_minutes        = 5
    long_break_minutes   = 15
    sessions_before_long = 4


class ModuleDetailPanel(QWidget):
    """
    Panneau droit de la page Modules.
    Affiche le widget interactif du module sélectionné.
    Gère la persistance des sessions via ModuleService.
    """

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

        # Page 0 : aucun module sélectionné
        empty = QLabel("Sélectionnez un module")
        empty.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(empty)

        # Page 1 : widget Pomodoro
        self.pomodoro_widget = PomodoroWidget(module=_DummyModule(), parent=self)
        self.pomodoro_widget.session_ended.connect(self._on_session_ended)
        self.stack.addWidget(self.pomodoro_widget)

        self.stack.setCurrentIndex(0)

    def load_module(self, module):
        """
        Charge un module dans le panneau.
        Reconstruit le widget avec les données du module
        et charge l'historique du jour.
        """
        self.current_module = module
        self.pomodoro_widget.load_module(module)

        sessions = self.module_service.get_sessions_for_module_and_date(
            module.id, date.today()
        )
        self.pomodoro_widget.update_history(sessions)
        self.stack.setCurrentIndex(1)

    def _on_session_ended(self, work_duration: int, break_duration: int, status: str):
        """
        Callback déclenché par PomodoroWidget à la fin d'une phase.
        Persiste la session via ModuleService et rafraîchit l'historique.
        """
        if not self.current_module:
            return
        if work_duration <= 0 and break_duration <= 0:
            return

        self.module_service.record_session(
            module_id=self.current_module.id,
            work_duration=work_duration,
            break_duration=break_duration,
            status=status,
            started_at=self._started_at or datetime.now(),
            ended_at=datetime.now()
        )
        self._started_at = None

        sessions = self.module_service.get_sessions_for_module_and_date(
            self.current_module.id, date.today()
        )
        self.pomodoro_widget.update_history(sessions)