from datetime import datetime
from uuid import uuid4

from domain.entities.event import Event

# ============ Notes ============  
# Cette classe permet de créer des instances d'événements, en encapsulant la logique de création.

class EventFactory:

    def create(self, intention_id:str, start_time:datetime, duration:int) -> Event:

        return Event(
            intention_id=intention_id,
            start_time=start_time,
            duration=duration,
            status="planned",
            created_at=datetime.utcnow()
        )