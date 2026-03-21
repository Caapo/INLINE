# ==================================== user.py ====================================

# =========== Import =========== 

import uuid
from datetime import datetime
from typing import Dict, Any
import json

# =================================== Class User =================================== 

class User:

    #Constructeur
    def __init__(self, email:str, username:str):
        self._id:str = str(uuid.uuid4())
        self._email:str = email
        self._username:str = username
        self._created_at:datetime = datetime.utcnow()
        self._metadata:Dict[str, Any] = {}

    # -------------------------------------------------------------------

    #Constructeur alternatif pour la reconstruction d'un utilisateur depuis la BDD
    @classmethod
    def from_persistence(cls, id:str, email:str, username:str, created_at:datetime, metadata:Dict[str, Any] = None) -> "User":
        user = cls.__new__(cls)
        user._id = id
        user._email = email
        user._username = username
        user._created_at = created_at
        user._metadata = metadata or {}

        return user
    
    # -------------------------------------------------------------------

    #Permet de récupérer les infos de l'user dans un format prêt pour la BDD
    def to_persistence(self) -> Dict[str, Any]:
        return {"id": self._id, "email": self._email, "username": self._username, "created_at": str(self._created_at), "metadata": json.dumps(self._metadata)}
    
    # -------------------------------------------------------------------


    def __repr__(self):
        return f"User(id={self._id}, email={self._email}, username={self._username}, created_at={self._created_at}, metadata={self._metadata})"

    # -------------------------------------------------------------------

    @property
    def id(self):
        return self._id
    
    # -------------------------------------------------------------------
    
    #Permet de récupérer les infos de l'user pour l'UI
    def get_user_info(self) -> Dict[str, Any]:
        return {"id": self._id, "email": self._email, "username": self._username, "created_at": self._created_at, "metadata": dict(self._metadata)}

    