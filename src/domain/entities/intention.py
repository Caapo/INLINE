from datetime import datetime
from typing import Optional


class Intention:

    def __init__(self, id: str, user_id: str, title: str, category: str, object_id: Optional[str] = None,
                is_active: bool = False, created_at: Optional[datetime] = None, metadata: Optional[dict] = None
    ):
        
        self._id = id
        self._user_id = user_id
        self._title = title
        self._category = category
        self._object_id = object_id
        self._is_active = is_active
        self._created_at = created_at or datetime.utcnow()
        self._metadata = metadata or {}

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