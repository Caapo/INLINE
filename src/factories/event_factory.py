# ==================== INLINE/src/factories/event_factory.py ====================

# ============ Imports ============
from datetime import datetime
from uuid import uuid4
from domain.enums.enums import EventStatus
from domain.entities.event import Event

# ============ class EventFactory ============  
# Cette classe permet de créer des instances d'événements, en encapsulant la logique de création.

class EventFactory:

    def create_event(self, intention_id:str, environment_id:str, start_time:datetime, duration:int) -> Event:
        if duration <= 0:
            raise ValueError("La durée doit être un entier strictement positif.")
        
        return Event(
            id=str(uuid4()),
            intention_id=intention_id,
            environment_id=environment_id,
            start_time=start_time,
            duration=duration,
            status=EventStatus.PLANNED.value,
            created_at=datetime.utcnow(),
            metadata={}
        )