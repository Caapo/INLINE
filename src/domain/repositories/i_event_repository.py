# ==================== INLINE/src/domain/repositories/i_event_repository.py ====================
# Interface du repository des événements.
# (Couche domaine)

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, datetime

from domain.entities.event import Event



class IEventRepository(ABC):
    """
    Interface abstraite du repository des événements.
    """

    @abstractmethod
    def save(self, event:Event) -> None:
        pass

    @abstractmethod
    def get_by_id(self, event_id:str) -> Optional[Event]:
        pass

    @abstractmethod
    def get_by_intention(self, intention_id:str) -> List[Event]:
        pass

    @abstractmethod
    def get_by_date(self, day:date) -> List[Event]:
        pass

    @abstractmethod
    def get_by_environment_and_date(self, environment_id:str, day:date) -> List[Event]:
        pass

    @abstractmethod
    def get_between(self, environment_id:str, start:datetime, end:datetime) -> List[Event]:
        pass
    
    @abstractmethod
    def delete(self, event_id:str) -> None:
        pass