# src/domain/repositories/modules/i_module_repository.py
# Interface définissant les méthodes de base pour la gestion des modules.
# Permet d'abstraire la couche de persistance et de faciliter les tests.


from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.modules.pomodoro.pomodoro_module import PomodoroModule


class IModuleRepository(ABC):
    """
    Interface définissant les méthodes de base pour la gestion des modules.
    Permet d'abstraire la couche de persistance et de faciliter les tests.
    """

    @abstractmethod
    def save(self, module: PomodoroModule) -> None:
        pass

    @abstractmethod
    def get_by_id(self, module_id: str) -> Optional[PomodoroModule]:
        pass

    @abstractmethod
    def get_by_owner(self, owner_id: str) -> List[PomodoroModule]:
        pass

    @abstractmethod
    def get_by_intention(self, intention_id: str) -> List[PomodoroModule]:
        pass

    @abstractmethod
    def delete(self, module_id: str) -> None:
        pass