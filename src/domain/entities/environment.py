# ======== environment.py =========

# ===== Imports =====
from typing import List, Optional, Any
from domain.entities.i_interactive_object import IInteractiveObject
from datetime import datetime
import json

class Environment:
    def __init__(self, id:str, owner_id:str, name:str, objects:Optional[List[IInteractiveObject]]=None, metadata:Optional[dict[str, Any]]=None):
        self._id = id
        self._owner_id = owner_id
        self._name = name
        self._objects = objects or []
        self._created_at = datetime.utcnow()
        self._metadata = metadata or {}
        

    #------------------

    def to_persistence(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "name": self.name,
            "objects": json.dumps([o.get_info() for o in self.objects]),
            "metadata": json.dumps(self._metadata),
            "created_at": self._created_at.isoformat()
        }

    #-----------------

    @classmethod
    def from_persistence(cls, id, owner_id, name, objects, metadata, created_at):
        env = cls(
            id=id,
            owner_id=owner_id,
            name=name,
            objects=[],
            metadata=metadata
        )
        env._created_at = created_at
        return env

    #------------------

    def add_interactive_object(self, obj:IInteractiveObject):
        self._objects.append(obj)

    #------------------
    
    def remove_interactive_object(self, obj_id:str):
        self._objects = [o for o in self._objects if o.id != obj_id]

    #------------------

    def get_interactive_object(self, obj_id:str) -> Optional[IInteractiveObject]:
        for o in self._objects:
            if o.id == obj_id:
                return o
        return None

    #------------------

    def __repr__(self):
        return f"Environment(id={self._id}, owner_id={self._owner_id}, name={self._name}, objects={len(self._objects)})"

    #------------------

    @property
    def id(self) -> str:
        return self._id

    @property
    def owner_id(self) -> str:
        return self._owner_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def objects(self) -> List[IInteractiveObject]:
        return self._objects

    #------------------

    def get_info(self):
        return {
            "id": self._id,
            "owner_id": self._owner_id,
            "name": self._name,
            "objects": [o.get_info() for o in self._objects],
            "metadata": self._metadata,
            "created_at": self._created_at
        }