# src/domain/entities/modules/pomodoro/pomodoro_module.py
# Représente le module Pomodoro, mini-application de gestion du temps.
# Contient sa propre configuration et son historique de sessions.


from datetime import datetime
from typing import Optional
import json

from domain.enums.enums import ModuleType


class PomodoroModule:
    """
    Module autonome de gestion du temps par la technique Pomodoro.
    Mini-application encapsulant sa propre configuration et son historique.

    Paramètres configurables par l'utilisateur :
        - Durée de travail (défaut : 25 min)
        - Durée de pause courte (défaut : 5 min)
        - Durée de pause longue (défaut : 15 min)
        - Nombre de sessions avant pause longue (défaut : 4)

    Attributs:
        _id (str): Identifiant unique du module.
        _owner_id (str): Identifiant de l'utilisateur propriétaire.
        _name (str): Nom donné par l'utilisateur.
        _type (ModuleType): Type du module, ici toujours POMODORO.
        _work_minutes (int): Durée de travail en minutes.
        _break_minutes (int): Durée de la pause courte en minutes.
        _long_break_minutes (int): Durée de la pause longue en minutes.
        _sessions_before_long (int): Nombre de sessions avant une pause longue.
        _intention_id (str | None): ID de l'intention associée, si liée à une intention.
        _created_at (datetime): Date de création du module.
        _updated_at (datetime): Date de la dernière mise à jour du module.
        _metadata (dict): Données extensibles pour flexibilité future.
    """

    # ==============================================
    # CONSTRUCTEUR
    # ==============================================

    def __init__(self, id:str, owner_id:str, name:str, work_minutes:int=25, break_minutes:int=5, long_break_minutes:int=15, sessions_before_long:int=4,
                intention_id:Optional[str]=None, created_at: Optional[datetime]=None, updated_at: Optional[datetime]=None, metadata: Optional[dict]=None):

        self._id = id
        self._owner_id = owner_id
        self._name = name
        self._type = ModuleType.POMODORO
        self._work_minutes = work_minutes
        self._break_minutes = break_minutes
        self._long_break_minutes = long_break_minutes
        self._sessions_before_long = sessions_before_long
        self._intention_id = intention_id
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
        self._metadata = metadata or {}

    # ==============================================
    # PERSISTANCE
    # ==============================================

    def to_persistence(self) -> dict:
        config = {
            "work_minutes":         self._work_minutes,
            "break_minutes":        self._break_minutes,
            "long_break_minutes":   self._long_break_minutes,
            "sessions_before_long": self._sessions_before_long
        }
        return {
            "id":           self._id,
            "owner_id":     self._owner_id,
            "name":         self._name,
            "type":         self._type.value,
            "intention_id": self._intention_id,
            "config":       json.dumps(config),
            "created_at":   self._created_at.isoformat(),
            "updated_at":   self._updated_at.isoformat(),
            "metadata":     json.dumps(self._metadata)
        }


    @classmethod
    def from_persistence(cls, id:str, owner_id:str, name:str, config_json:str, intention_id:Optional[str], created_at:str, updated_at:str,
                        metadata_json:str) -> "PomodoroModule":
        config = json.loads(config_json) if config_json else {}
        m = cls.__new__(cls)
        m._id = id
        m._owner_id = owner_id
        m._name = name
        m._type = ModuleType.POMODORO
        m._work_minutes = config.get("work_minutes", 25)
        m._break_minutes = config.get("break_minutes", 5)
        m._long_break_minutes = config.get("long_break_minutes", 15)
        m._sessions_before_long = config.get("sessions_before_long", 4)
        m._intention_id = intention_id
        m._created_at = datetime.fromisoformat(created_at)
        m._updated_at = datetime.fromisoformat(updated_at)
        m._metadata = json.loads(metadata_json) if metadata_json else {}
        return m



    # ==============================================
    # MÉTHODES MÉTIER
    # ==============================================

    def rename(self, new_name: str) -> None:
        if not new_name:
            raise ValueError("Le nom ne peut pas être vide.")
        self._name = new_name
        self._touch()


    def update_config(self, work_minutes: int = None, break_minutes: int = None,
                      long_break_minutes: int = None, sessions_before_long: int = None) -> None:
        if work_minutes is not None:
            if work_minutes <= 0:
                raise ValueError("La durée de travail doit être positive.")
            self._work_minutes = work_minutes
        if break_minutes is not None:
            if break_minutes <= 0:
                raise ValueError("La durée de pause doit être positive.")
            self._break_minutes = break_minutes
        if long_break_minutes is not None:
            if long_break_minutes <= 0:
                raise ValueError("La durée de longue pause doit être positive.")
            self._long_break_minutes = long_break_minutes
        if sessions_before_long is not None:
            if sessions_before_long <= 0:
                raise ValueError("Le nombre de sessions doit être positif.")
            self._sessions_before_long = sessions_before_long
        self._touch()


    def attach_to_intention(self, intention_id: str) -> None:
        self._intention_id = intention_id
        self._touch()


    def detach_from_intention(self) -> None:
        self._intention_id = None
        self._touch()


    def _touch(self) -> None:
        self._updated_at = datetime.utcnow()

    
    # ==================================================
    # PROPRIÉTÉS
    # ==================================================

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
    def type(self) -> str:            
        return self._type.value

    @property
    def work_minutes(self) -> int:            
        return self._work_minutes

    @property
    def break_minutes(self) -> int:            
        return self._break_minutes

    @property
    def long_break_minutes(self) -> int:            
        return self._long_break_minutes

    @property
    def sessions_before_long(self) -> int:            
        return self._sessions_before_long

    @property
    def intention_id(self) -> Optional[str]:  
        return self._intention_id

    @property
    def created_at(self) -> datetime:       
        return self._created_at

    @property
    def updated_at(self) -> datetime:       
        return self._updated_at

    @property
    def metadata(self) -> dict:           
        return self._metadata


    # ==================================================
    # GETTERS ET AUTRES
    # ==================================================

    def get_info(self) -> dict:
        return {
            "id":                   self._id,
            "owner_id":             self._owner_id,
            "name":                 self._name,
            "type":                 self._type.value,
            "work_minutes":         self._work_minutes,
            "break_minutes":        self._break_minutes,
            "long_break_minutes":   self._long_break_minutes,
            "sessions_before_long": self._sessions_before_long,
            "intention_id":         self._intention_id,
            "created_at":           self._created_at.isoformat(),
            "updated_at":           self._updated_at.isoformat()
        }