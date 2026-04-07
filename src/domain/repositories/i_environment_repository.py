# ======== INLINE/src/domain/repositories/i_environment_repository.py =========
# Interface définissant les méthodes de base pour la gestion des environnements.
# Permet d'abstraire la couche de persistance et de faciliter les tests.



from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.environment import Environment

class IEnvironmentRepository(ABC):
    """
    Interface abstraite du repository des environnements.
    """

    @abstractmethod
    def save(self, env:Environment) -> None:
        pass

    @abstractmethod
    def get_by_id(self, env_id:str) -> Optional[Environment]:
        pass

    @abstractmethod
    def get_by_owner(self, owner_id:str) -> List[Environment]:
        pass

    @abstractmethod
    def list_all(self) -> List[Environment]:
        pass

    @abstractmethod
    def delete(self, env_id:str) -> None:
        pass