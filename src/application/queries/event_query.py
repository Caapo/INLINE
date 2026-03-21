# =========== EventQueryService ============

# =========== Imports ============
from datetime import date
from domain.repositories.i_event_repository import IEventRepository
from domain.repositories.i_intention_repository import IIntentionRepository

# ============ Notes ============
# Cette classe permet d'assurer la gestion des requêtes liées aux événements, telles que la récupération des événements d'une journée donnée.
# Elle interagit avec la base de données (SQLiteEventRepository)  pour récupérer les données des événements.

class EventQueryService:

    def __init__(self, event_repository: IEventRepository, intention_repository:IIntentionRepository):
        self._event_repository = event_repository
        self._intention_repository = intention_repository

    def get_events_for_day(self, day: date):
        events = self._event_repository.get_by_date(day)
        events = sorted(events, key=lambda e: e.start_time)

        if not events:
            return []

        #Récupération de l'intention de référence pour obtenir l'user_id et faire le mapping des intentions de l'utilisateur
        first_intention = self._intention_repository.get_by_id(events[0].intention_id)
        user_id = first_intention.user_id if first_intention else None

        #Mapping des intentions de l'utilisateur (On les récupère toute en une fois) pour éviter les requêtes répétées pour chaque événement
        intentions = self._intention_repository.get_by_user(user_id)
        intentions_map = { i.id: i for i in intentions }
        result = []

        for e in events:
            intention = intentions_map.get(e.intention_id)

            result.append({
                "id": e.id,
                "title": intention.title if intention else None,
                "start_time": e.start_time.strftime("%H:%M"),
                "duration": e.duration,
                "end_time": e.end_time.strftime("%H:%M"),
                "status": e.status
            })

        return result