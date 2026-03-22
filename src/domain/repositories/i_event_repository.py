# ==================== i_event_repository.py ====================

# ============ Imports ============
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, datetime
from domain.entities.event import Event

# ============ Notes ============
# Cette interface définit les méthodes que doit implémenter un stockage d'événements


# ============ Class ============

class IEventRepository(ABC):

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