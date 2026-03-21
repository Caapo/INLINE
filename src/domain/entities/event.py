# ============ Imports ============
from datetime import datetime
from typing import Optional


# ============ Notes ============  
# Cette classe permet de représenter un événement lié à une intention, en stockant des informations 
# telles que l'heure de début, la durée, le statut (planifié, complété, annulé).



# ============ Class ============   

class Event:

    def __init__(self, id:str, intention_id:str, start_time:datetime, duration:int, status:str="planned", metadata:Optional[dict]=None):
        self._id = id
        self._intention_id = intention_id
        self._start_time = start_time
        self._duration = duration
        self._status = status
        self._created_at = datetime.utcnow()
        self._metadata = metadata or {}

    #-----------------------

    def from_persistence(id:str, intention_id:str, start_time:datetime, duration:int, status:str, created_at:datetime, metadata:dict):
        event = Event(id=id, intention_id=intention_id, start_time=start_time, duration=duration, status=status, metadata=metadata)
        event._created_at = created_at
        return event

    #-----------------------

    def update_time(self, start_time:datetime, duration:int):
        self._start_time = start_time
        self._duration = duration

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

    def to_persistence(self):
        return {
            "id": self._id,
            "intention_id": self._intention_id,
            "start_time": self._start_time.isoformat(),
            "duration": self._duration,
            "status": self._status,
            "created_at": self._created_at.isoformat(),
            "metadata": json.dumps(self._metadata)
        }

    # ----------------------

    def __repr__(self):
        return f"Event(id={self._id}, intention_id={self._intention_id}, start_time={self._start_time}, duration={self._duration}, status={self._status}, created_at={self._created_at}, metadata={self._metadata})"

    # ----------------------

    def get_info(self):
        return {
            "id": self._id,
            "intention_id": self._intention_id,
            "start_time": self._start_time,
            "duration": self._duration,
            "status": self._status,
            "created_at": self._created_at,
            "metadata": self._metadata
        }