# ==================== INLINE/src/application/services/event_service.py ====================
# Service applicatif des événements.
# Orchestre les cas d'usage liés aux événements et notifie
# les abonnés via le patron Observer.


from datetime import datetime
from typing import Optional

from domain.entities.event import Event
from domain.repositories.i_event_repository import IEventRepository
from factories.event_factory import EventFactory
from shared.observer import Observable


class EventService(Observable):
    """
    Service applicatif de gestion des événements.
    Orchestre le cycle de vie des events et notifie l'UI via Observer.

    Attributs:
        _event_repository (IEventRepository): Interface de persistance des événements.
        _event_factory (EventFactory): Factory pour créer des instances d'Event.
    """   

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================

    def __init__(self, event_repository:IEventRepository, event_factory:EventFactory):
        super().__init__()
        self._event_repository = event_repository
        self._event_factory = event_factory

    # ==================================================
    # MÉTHODES CAS D'USAGE
    # ==================================================

    def create_event(self, intention_id:str, environment_id:str, start_time:datetime, duration:int):
        """
        Crée un nouvel événement et le persiste.
        Notifie les abonnés avec l'événement "event_created".
        """
        event = self._event_factory.create_event(
            intention_id=intention_id,
            environment_id=environment_id,
            start_time=start_time,
            duration=duration
        )
        self._event_repository.save(event)
        self.notify("event_created", event)
        return event


    def update_event_time(self, event_id:str, start_time:datetime, duration:Optional[int]=None) -> Event:
        """
        Met à jour l'heure de début et la durée d'un événement existant.
        Notifie les abonnés avec l'événement "event_updated".
        """
        event = self._get_event_or_raise(event_id)
        new_duration = duration if duration is not None else event.duration
        event.update_time(start_time, new_duration)
        self._event_repository.save(event)
        self.notify("event_updated", event)
        return self._event_repository.get_by_id(event_id)

    

    def complete_event(self, event_id:str) -> Event:
        """
        Marque un événement comme complété.
        Notifie les abonnés avec l'événement "event_updated".
        Retourne l'événement mis à jour.
        Lève ValueError si l'événement n'existe pas ou n'est pas dans un état planifié.
        """
        event = self._get_event_or_raise(event_id)
        event.complete()
        self._event_repository.save(event)
        self.notify("event_updated", event)
        return self._event_repository.get_by_id(event_id)


    def cancel_event(self, event_id:str) -> Event:
        """
        Annule un événement existant.
        Notifie les abonnés avec l'événement "event_updated".
        Retourne l'événement mis à jour.
        Lève ValueError si l'événement n'existe pas ou n'est pas dans un état planifié.
        """
        event = self._get_event_or_raise(event_id)
        event.cancel()
        self._event_repository.save(event)
        self.notify("event_updated", event)
        return self._event_repository.get_by_id(event_id)


    def delete_event(self, event_id:str) -> None:
        """
        Supprime un événement existant.
        Notifie les abonnés avec l'événement "event_deleted".
        Lève ValueError si l'événement n'existe pas.
        """
        event = self._get_event_or_raise(event_id)
        self._event_repository.delete(event_id)
        self.notify("event_deleted", event_id)

    # ===============================================
    # GETTERS ET AUTRES
    # ===============================================

    def _get_event_or_raise(self, event_id:str) -> Event:
        """
        Récupère un événement ou lève ValueError si introuvable.
        """
        event = self._event_repository.get_by_id(event_id)
        if not event:
            raise ValueError("Aucun événement trouvé.")
        return event


    def get_events_for_environment_and_day(self, environment_id:str, day:datetime):
        """
        Récupère tous les événements d'un environnement donné pour une journée donnée.
        """
        return self._event_repository.get_by_environment_and_date(environment_id, day.date())
    

    def get_events_between(self, environment_id:str, start:datetime, end:datetime):
        """
        Récupère tous les événements d'un environnement donné entre deux dates.
        """
        return self._event_repository.get_between(environment_id, start, end)
