# ==================== event.py ====================
# ============ Imports ============
from datetime import datetime, timedelta
from typing import Optional
from typing import Any
import json


# ============ Notes ============  
# Cette classe permet de représenter un événement lié à une intention, en stockant des informations 
# telles que l'heure de début, la durée, le statut (planifié, complété, annulé).



# ============ Class ============   

class Event:

    def __init__(self, id:str, intention_id:str, start_time:datetime, duration:int, status:str="planned", created_at:Optional[datetime]=None, metadata:Optional[dict[str, Any]]=None):
        self._id = id
        self._intention_id = intention_id
        self._start_time = start_time
        self._duration = duration
        self._end_time = start_time + timedelta(minutes=duration)
        self._status = status
        self._created_at = created_at or datetime.utcnow()
        self._metadata = metadata or {}

    #-----------------------

    @classmethod
    def from_persistence(cls, id:str, intention_id:str, start_time:datetime, duration:int, end_time:datetime, status:str, created_at:datetime, metadata:Optional[dict[str, Any]]=None):
        event = cls.__new__(cls)
        event._id = id
        event._intention_id = intention_id
        event._start_time = start_time
        event._duration = duration
        event._end_time = end_time
        event._status = status
        event._created_at = created_at
        event._metadata = metadata or {}
        return event

    # ----------------------

    def to_persistence(self):
        return {
            "id": self._id,
            "intention_id": self._intention_id,
            "start_time": self._start_time.isoformat(),
            "duration": self._duration,
            "end_time": self._end_time.isoformat(),
            "status": self._status,
            "created_at": self._created_at.isoformat(),
            "metadata": json.dumps(self._metadata)
        }

    #-----------------------

    def update_time(self, start_time:datetime, duration:int):
        if self._status != "planned":
            raise ValueError("Seuls les événements planifiés peuvent être modifiés.")
        if start_time < datetime.utcnow():
            raise ValueError("L'heure de début doit être dans le futur.")
        if duration <= 0:
            raise ValueError("La durée doit être un entier strictement positif.")

        self._start_time = start_time
        self._duration = duration
        self._end_time = start_time + timedelta(minutes=duration)

    # ----------------------

    def complete(self):
        if self._status == "cancelled":
            raise ValueError("Les évènements annulés ne peuvent pas être complétés")

        self._status = "completed"

    # ----------------------

    def cancel(self):
        if self._status == "completed":
            raise ValueError("Les évènements complétés ne peuvent pas être annulés")

        self._status = "cancelled"

    # ----------------------

    def __repr__(self):
        return(
            f"Event(id={self._id}, "
            f"intention_id={self._intention_id}, "
            f"start_time={self._start_time}, "
            f"duration={self._duration}, "
            f"end_time={self._end_time}, "
            f"status={self._status}, "
            f"created_at={self._created_at}, "
            f"metadata={self._metadata})"
        )

    # ----------------------
    #Pour l'UI
    @property
    def id(self):
        return self._id

    @property
    def start_time(self):
        return self._start_time
    
    @property
    def end_time(self):
        return self._end_time
    
    @property
    def status(self):
        return self._status
    
    @property
    def intention_id(self):
        return self._intention_id

    # ----------------------

    def get_info(self):
        return {
            "id": self._id,
            "intention_id": self._intention_id,
            "start_time": self._start_time,
            "duration": self._duration,
            "end_time": self._end_time,
            "status": self._status,
            "created_at": self._created_at,
            "metadata": self._metadata
        }