# ==================== INLINE/src/domain/entities/event.py ====================
# Classe représentant un événement lié à une intention.
# Les événements permettent de suivre l'exécution des intentions dans le temps.

from datetime import datetime, timedelta
from typing import Optional
from typing import Any
import json

from domain.enums.enums import EventStatus
 

class Event:
    """
    Projection temporelle d'une intention.
    Représente une occurrence planifiée ou réalisée d'une intention
    dans le temps. Ne contient pas de logique métier complexe,
    uniquement la gestion de son cycle de vie (planifié -> complété/annulé).

    Attributs:
        _id (str): Identifiant unique de l'événement.
        _intention_id (str): Identifiant de l'intention associée.
        _environment_id (str): Identifiant de l'environnement d'exécution.
        _start_time (datetime): Date et heure de début planifiée.
        _duration (int): Durée prévue en minutes.
        _end_time (datetime): Date et heure de fin calculée.
        _status (EventStatus): Statut actuel de l'événement (planifié, complété, annulé).
        _created_at (datetime): Date de création de l'événement.
        _metadata (dict): Données extensibles sans modifier la classe.
    """
    def __init__(self, id:str, intention_id:str, environment_id:str, start_time:datetime, duration:int, status:str="planned", created_at:Optional[datetime]=None, metadata:Optional[dict[str, Any]]=None):
        self._id = id
        self._intention_id = intention_id
        self._environment_id = environment_id
        self._start_time = start_time
        self._duration = duration
        self._end_time = start_time + timedelta(minutes=duration)
        self._status = EventStatus(status)
        self._created_at = created_at or datetime.utcnow()
        self._metadata = metadata or {}

    # ==================================================
    # PERSISTANCE
    # ==================================================

    @classmethod
    def from_persistence(cls, id:str, intention_id:str, environment_id:str, start_time:datetime, duration:int, end_time:datetime, status:str, created_at:datetime, 
    metadata:Optional[dict[str, Any]]=None):
        """
        Reconstruit un Event depuis la base.
        """
        event = cls.__new__(cls)
        event._id = id
        event._intention_id = intention_id
        event._environment_id = environment_id
        event._start_time = start_time
        event._duration = duration
        event._end_time = end_time
        event._status = EventStatus(status)
        event._created_at = created_at
        event._metadata = metadata or {}
        return event


    def to_persistence(self):
        """
        Prépare les données de l'événement pour la persistance en base.
        """
        return {
            "id": self._id,
            "intention_id": self._intention_id,
            "environment_id": self._environment_id,
            "start_time": self._start_time.isoformat(), # Convertit en string ISO pour la base de données
            "duration": self._duration,
            "end_time": self._end_time.isoformat(), # Convertit en string ISO pour la base de données
            "status": self._status.value,
            "created_at": self._created_at.isoformat(), # Convertit en string ISO pour la base de données
            "metadata": json.dumps(self._metadata)
        }

    # ==================================================
    # MÉTHODES MÉTIER
    # ==================================================

    def update_time(self, start_time:datetime, duration:int):
        """
        Reprogramme l'event.
        Lève ValueError si l'event n'est pas en statut PLANNED
        ou si la durée est invalide.
        """
        if self._status != EventStatus.PLANNED:
            raise ValueError("Seuls les événements planifiés peuvent être modifiés.")
        if duration <= 0:
            raise ValueError("La durée doit être un entier strictement positif.")

        self._start_time = start_time
        self._duration = duration
        self._end_time = start_time + timedelta(minutes=duration)


    def complete(self):
        """
        Marque l'event comme complété.
        Lève ValueError si déjà annulé ou déjà complété.
        """
        if self._status == EventStatus.CANCELLED:
            raise ValueError("Les évènements annulés ne peuvent pas être complétés")
        if self._status == EventStatus.COMPLETED:
            raise ValueError("Les évènements complétés ne peuvent pas être complétés à nouveau")

        self._status = EventStatus.COMPLETED


    def cancel(self):
        """
        Annule l'event.
        Lève ValueError si déjà complété.
        """
        if self._status == EventStatus.COMPLETED:
            raise ValueError("Les évènements complétés ne peuvent pas être annulés")

        self._status = EventStatus.CANCELLED

    # ==================================================
    # REPRÉSENTATION
    # ==================================================

    def __repr__(self):
        """
        Représentation textuelle de l'événement pour le débogage.
        """
        return(
            f"Event(id={self._id}, "
            f"intention_id={self._intention_id}, "
            f"environment_id={self._environment_id}, "
            f"start_time={self._start_time}, "
            f"duration={self._duration}, "
            f"end_time={self._end_time}, "
            f"status={self._status}, "
            f"created_at={self._created_at}, "
            f"metadata={self._metadata})"
        )

    # ==================================================
    # PROPRIÉTÉS
    # ==================================================

    @property
    def id(self):
        return self._id
    
    @property
    def intention_id(self):
        return self._intention_id
    
    @property
    def environment_id(self):
        return self._environment_id

    @property
    def start_time(self):
        return self._start_time
    
    @property
    def duration(self):
        return self._duration

    @property
    def end_time(self):
        return self._end_time
    
    @property
    def status(self):
        return self._status.value
    

    # ==================================================
    # AUTRES
    # ==================================================

    def get_info(self):
        """
        Retourne un dictionnaire complet des données de l'événement.
        """
        return {
            "id": self._id,
            "intention_id": self._intention_id,
            "environment_id": self._environment_id,
            "start_time": self._start_time.isoformat(),
            "duration": self._duration,
            "end_time": self._end_time.isoformat(),
            "status": self._status.value,
            "created_at": self._created_at.isoformat(),
            "metadata": self._metadata
        }