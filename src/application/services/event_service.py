# ============ Imports ============
from datetime import datetime
from uuid import uuid4

from domain.entities.event import Event
from domain.repositories.i_event_repository import IEventRepository


# ============ Notes ============  
# Cette classe permet d'assurer la gestion des événements, tels que la création, la mise à jour, la complétion et l'annulation d'événements. 
# Elle interagit avec la base de données (SQLiteEventRepository)  pour stocker et récupérer les données des événements.


# ============ Class ============  
class EventService():

    def __init__(self, event_repository:IEventRepository):
        self._event_repository = event_repository
    
    #------------------

    def create_event(self, intention_id:str, start_time:datetime, duration:int):

        event = Event(
            id = str(uuid4()),
            intention_id = intention_id,
            start_time = start_time,
            duration = duration
        )

        self._event_repository.save(event)
        return event

    #------------------

    def update_event_time(self, event_id:str, start_time:datetime, duration:Optional[int] = None):
        event = self._event_repository.get_by_id(event_id)

        if not event:
            raise ValueError("Aucun événement trouvée.")

        event.update_time(start_time, duration or event.get_info()["duration"])
        self._event_repository.save(event)
        return event

    #------------------

    def complete_event(self, event_id:str):
        event = self._event_repository.get_by_id(event_id)

        if not event:
            raise ValueError("Aucun événement trouvée.")

        event.complete()
        self._event_repository.save(event)
        return event    

    #------------------

    def cancel_event(self, event_id:str):
        event = self._event_repository.get_by_id(event_id)

        if not event:
            raise ValueError("Aucun événement trouvée.")

        event.cancel()
        self._event_repository.save(event)
        return event