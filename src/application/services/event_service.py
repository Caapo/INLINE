# ==================== INLINE/src/application/services/event_service.py ====================
# ============ Imports ============
from datetime import datetime
from uuid import uuid4
from typing import Optional

from domain.entities.event import Event
from domain.repositories.i_event_repository import IEventRepository
from factories.event_factory import EventFactory


# ============ Class EventService ============  
# Cette classe permet d'assurer la gestion des événements, tels que la création, la mise à jour, la complétion et l'annulation d'événements. 
# Elle interagit avec la base de données (SQLiteEventRepository)  pour stocker et récupérer les données des événements.


class EventService():

    def __init__(self, event_repository:IEventRepository, event_factory:EventFactory):
        self._event_repository = event_repository
        self._event_factory = event_factory
    
    #------------------

    def create_event(self, intention_id:str, environment_id:str, start_time:datetime, duration:int):
        event = self._event_factory.create_event(intention_id=intention_id, environment_id=environment_id, start_time=start_time, duration=duration)
        self._event_repository.save(event)
        return event

    #------------------

    def _get_event_or_raise(self, event_id:str) -> Event:
        event = self._event_repository.get_by_id(event_id)
        if not event:
            raise ValueError("Aucun événement trouvé.")
        return event

    #------------------

    def get_events_for_environment_and_day(self, environment_id:str, day:datetime):
        return self._event_repository.get_by_environment_and_date(environment_id, day.date())

    #------------------
    
    def get_events_between(self, environment_id:str, start:datetime, end:datetime):
        return self._event_repository.get_between(environment_id, start, end)

    #------------------

    def update_event_time(self, event_id:str, start_time:datetime, duration:Optional[int]=None) -> Event:
        event = self._get_event_or_raise(event_id)
        new_duration = duration if duration is not None else event.duration
        event.update_time(start_time, new_duration)
        self._event_repository.save(event)
        return self._event_repository.get_by_id(event_id)

    #------------------

    def complete_event(self, event_id:str) -> Event:
        event = self._get_event_or_raise(event_id)
        event.complete()
        self._event_repository.save(event)
        return self._event_repository.get_by_id(event_id) 

    #------------------

    def cancel_event(self, event_id:str) -> Event:
        event = self._get_event_or_raise(event_id)
        event.cancel()
        self._event_repository.save(event)
        return self._event_repository.get_by_id(event_id)