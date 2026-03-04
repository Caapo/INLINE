# =========== Import =========== 

import uuid
from datetime import datetime
from typing import Dict, Any
import json

# =================================== Class User =================================== 

class User:

    #Constructeur
    def __init__(self, email:str, username:str):
        self.__id:str = str(uuid.uuid4())
        self.__email:str = email
        self.__username:str = username
        self.__created_at:datetime = datetime.utcnow()
        self.__metadata:Dict[str, Any] = {}

    # -------------------------------------------------------------------

    #Constructeur alternatif pour la reconstruction d'un utilisateur depuis la BDD
    @classmethod
    def from_persistence(cls, user_id:str, email:str, username:str, created_at:datetime, metadata:Dict[str, Any] = None) -> "User":
        user = cls.__new__(cls)
        user.__id = user_id
        user.__email = email
        user.__username = username
        user.__created_at = created_at
        user.__metadata = metadata or {}

        return user
    
    # -------------------------------------------------------------------

    #Permet de récupérer les infos de l'user dans un formet prêt pour la BDD
    def to_persistence(self) -> Dict[str, Any]:
        return {"id": self.__id, "email": self.__email, "username": self.__username, "created_at": str(self.__created_at), "metadata": json.dumps(self.__metadata)}
    
    #Permet de récupérer les infos de l'user pour l'UI
    def get_user_info(self) -> Dict[str, Any]:
        return {"id": self.__id, "email": self.__email, "username": self.__username, "created_at": self.__created_at, "metadata": dict(self.__metadata)}

    