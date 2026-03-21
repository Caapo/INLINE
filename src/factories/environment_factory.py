# ====== environment_factory.py ======

# ===== Imports =====
from domain.entities.environment import Environment
from uuid import uuid4
from typing import Optional


class EnvironmentFactory:
    
    def create_environment(self, owner_id:str, name:str, objects:Optional[list]=None, metadata:Optional[dict]=None) -> Environment:
        return Environment(
            id=str(uuid4()),
            owner_id=owner_id,
            name=name,
            objects=objects or [],
            metadata=metadata or {}
        )