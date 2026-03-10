# ============ Imports ============
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.intention import Intention

# ============ Notes ============
# Cette interface définit les méthodes que doit implémenter un stockage d'intentions



# ============ Class ============

class IIntentionRepository(ABC):

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