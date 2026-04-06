# ==================== INLINE/src/factories/event_factory.py ====================
# Factory de création des événements.
# Centralise la validation et la construction pour garantir
# la cohérence des objets créés.

from datetime import datetime
from uuid import uuid4

from domain.enums.enums import EventStatus
from domain.entities.event import Event


class EventFactory:
    """
    Factory de création des événements.
    Centralise la validation et la construction pour garantir
    la cohérence des objets créés (id, date, statut par défaut).
    """

    def create_event(self, intention_id:str, environment_id:str, start_time:datetime, duration:int) -> Event:
        """
        Crée un nouvel Event avec statut PLANNED par défaut.
        Lève ValueError si duration <= 0.
        Génère automatiquement l'UUID et la date de création.
        """
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