# src/domain/repositories/modules/pomodoro/i_pomodoro_session_repository.py

from abc import ABC, abstractmethod
from typing import List
from datetime import date
from domain.entities.modules.pomodoro.pomodoro_session import PomodoroSession


class IPomodoroSessionRepository(ABC):

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
        pass

    @abstractmethod
    def delete_by_module(self, module_id: str) -> None:
        pass