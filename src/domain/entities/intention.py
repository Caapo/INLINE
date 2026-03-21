# ==================================== intention.py ====================================

# ============ Imports ============
from datetime import datetime
from typing import Optional
from typing import Any
import json


# ============ Notes ============  
# Cette classe permet de représenter une intention, en stockant des informations 
# telles que le titre, la catégorie, le statut (active, inactive).
   

class Intention:

    def __init__(self, id:str, user_id:str, title:str, category:str, object_id:Optional[str]=None, created_at:Optional[datetime]=None, metadata:Optional[dict[str, Any]]=None):
        
        self._id = id
        self._user_id = user_id
        self._title = title
        self._category = category
        self._object_id = object_id
        self._is_active = False
        self._created_at = created_at or datetime.utcnow()
        self._metadata = metadata or {}

    #--------------------------------------------

    @classmethod
    def from_persistence(cls, id:str, user_id:str, title:str, category:str, object_id:Optional[str], is_active:bool, created_at:datetime, metadata:Optional[dict[str, Any]]=None) -> "Intention":
        intention = cls.__new__(cls)
        intention._id = id
        intention._user_id = user_id
        intention._title = title
        intention._category = category
        intention._object_id = object_id
        intention._is_active = is_active
        intention._created_at = created_at
        intention._metadata = metadata or {}
        return intention

    #--------------------------------------------

    def to_persistence(self) -> dict:

        return {
            "id": self._id,
            "user_id": self._user_id,
            "object_id": self._object_id,
            "category": self._category,
            "title": self._title,
            "is_active": self._is_active,
            "created_at": self._created_at.isoformat(),
            "metadata": json.dumps(self._metadata)
        }

    #--------------------------------------------

    def rename(self, new_title:str):
        if not new_title:
            raise ValueError("Le titre de l'intention ne peut pas être vide.")
        self._title = new_title

    #--------------------------------------------

    def activate(self):
        self._is_active = True


    def deactivate(self):
        self._is_active = False

    #--------------------------------------------

    def __repr__(self):
        return f"Intention(id={self._id}, title={self._title}, active={self._is_active})"

    #--------------------------------------------
    #En attendant pour éviter d'avoir à ajouter un getter quand j'en ai besoin
    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def title(self):
        return self._title
    
    @property
    def category(self):
        return self._category
    
    @property
    def object_id(self):
        return self._object_id

    @property
    def is_active(self):
        return self._is_active

    @property
    def created_at(self):
        return self._created_at

    @property
    def metadata(self):
        return self._metadata

    #--------------------------------------------

    def get_info(self):

        return {
            "id": self._id,
            "user_id": self._user_id,
            "title": self._title,
            "category": self._category,
            "object_id": self._object_id,
            "is_active": self._is_active,
            "created_at": self._created_at,
            "metadata": self._metadata
        }