# ====== INLINE/src/factories/environment_factory.py ======
# Factory pour créer des instances d'environnement à partir de données brutes.

from uuid import uuid4
from typing import Optional

from domain.entities.environment import Environment


class EnvironmentFactory:
    """
    Factory pour créer des instances d'environnement à partir de données brutes.
    Permet d'abstraire la logique de création et de conversion des environnements.
    """
    
    def create_environment(self, owner_id:str, name:str, objects:Optional[list]=None, metadata:Optional[dict]=None) -> Environment:
        return Environment(
            id=str(uuid4()),
            owner_id=owner_id,
            name=name,
            objects=objects or [],
            metadata=metadata or {}
        )