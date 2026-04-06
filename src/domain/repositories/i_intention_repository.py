# ================ INLINE/src/domain/repositories/i_intention_repository.py ================
# Interface du repository des intentions.
# (Couche domaine)


from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.intention import Intention


class IIntentionRepository(ABC):
    """
    Interface abstraite du repository des intentions.
    """

    @abstractmethod
    def save(self, intention:Intention) -> None:
        pass

    @abstractmethod
    def get_by_id(self, intention_id:str) -> Optional[Intention]:
        pass

    @abstractmethod
    def get_by_user(self, user_id:str) -> List[Intention]:
        pass

    @abstractmethod
    def get_active(self, user_id:str) -> Optional[Intention]:
        pass

    @abstractmethod
    def get_all(self) -> List[Intention]:
        pass

    @abstractmethod
    def delete(self, intention_id:str) -> None:
        pass