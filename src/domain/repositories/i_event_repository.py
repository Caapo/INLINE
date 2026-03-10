from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from domain.entities.event import Event


class IEventRepository(ABC):

    @abstractmethod
    def save(self, event: Event) -> None:
        pass

    @abstractmethod
    def get_by_id(self, event_id: str) -> Optional[Event]:
        pass

    @abstractmethod
    def get_by_intention(self, intention_id: str) -> List[Event]:
        pass

    @abstractmethod
    def get_by_date(self, day: date) -> List[Event]:
        pass