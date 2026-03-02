#import
import uuid
from datetime import datetime
from typing import Dict, Any

# ======================== Class User ======================== 
class User:
    def __init__(self, email:str, username:str):
        #Attributs prives
        self.__id:str = str(uuid.uuid4())
        self.__email:str = email
        self.__username:str = username
        self.__created_at:datetime = datetime.utcnow()
        self.__metadata:Dict[str, Any] = {}


    #Methodes
    def get_info(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "email": self.__email,
            "username": self.__username,
            "created_at": self.__created_at,
            "metadata": dict(self.__metadata),
        }