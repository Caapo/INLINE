# ============ Imports ============
from datetime import datetime
from uuid import uuid4

from domain.entities.event import Event
from domain.repositories.i_event_repository import IEventRepository
from factories.intention_factory import EventFactory


# ============ Notes ============  
# Cette classe permet d'assurer la gestion des événements, tels que la création, la mise à jour, la complétion et l'annulation d'événements. 
# Elle interagit avec la base de données (SQLiteEventRepository)  pour stocker et récupérer les données des événements.


# ============ Class ============  
class EventService():

    def __init__(self, event_repository:IEventRepository, event_factory: EventFactory):
        self._event_repository = event_repository
        self._event_factory = event_factory
    
    #------------------

    def create_event(self, intention_id:str, start_time:datetime, duration:int):
        event = self._event_factory.create_event(intention_id=intention_id, start_time=start_time, duration=duration)
        self._event_repository.save(event)
        return event

    #------------------

    def _get_event_or_raise(self, event_id:str) -> Event:
        event = self._event_repository.get_by_id(event_id)
        if not event:
            raise ValueError("Aucun événement trouvée.")
        return event

    #------------------

    def update_event_time(self, event_id:str, start_time:datetime, duration:Optional[int] = None) -> Event:
        event = self._get_event_or_raise(event_id)
        event.update_time(start_time, duration or event.get_info()["duration"])
        self._event_repository.save(event)
        return event

    #------------------

    def complete_event(self, event_id:str) -> Event:
        event = self._get_event_or_raise(event_id)
        event.complete()
        self._event_repository.save(event)
        return event    

    #------------------

    def cancel_event(self, event_id:str) -> Event:
        event = self._get_event_or_raise(event_id)
        event.cancel()
        self._event_repository.save(event)
        return event