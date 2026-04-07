# src/domain/repositories/modules/pomodoro/i_pomodoro_session_repository.py

from abc import ABC, abstractmethod
from typing import List
from datetime import date
from domain.entities.modules.pomodoro.pomodoro_session import PomodoroSession


class IPomodoroSessionRepository(ABC):
    """
    Interface abstraite du repository des sessions Pomodoro.
    Séparé du repository des modules pour respecter SRP,
    les sessions ont leur propre cycle de vie et leurs propres requêtes.
    """

    @abstractmethod
    def save(self, session: PomodoroSession) -> None:
        pass

    @abstractmethod
    def get_by_module(self, module_id: str) -> List[PomodoroSession]:
        pass

    @abstractmethod
    def get_by_date(self, day: date) -> List[PomodoroSession]:
        pass

    @abstractmethod
    def get_by_module_and_date(self, module_id: str, day: date) -> List[PomodoroSession]:
        """
        Retourne les sessions d'un module pour un jour donné.
        Utilisé pour afficher l'historique du jour dans le widget Pomodoro.
        Triées par heure croissante.
        """
        pass

    @abstractmethod
    def delete_by_module(self, module_id: str) -> None:
        pass