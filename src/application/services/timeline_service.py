# ====== INLINE/src/application/services/timeline_service.py ======

# ============ Imports ============
from datetime import date
from domain.repositories.i_event_repository import IEventRepository


# ============ class TimelineService ============
# Cette classe permet de gérer la timeline d'un utilisateur, en récupérant les événements liés à ses intentions pour une journée donnée.

class TimelineService:

    def __init__(self, event_repository:IEventRepository):
        self._event_repository = event_repository

    def get_event_by_date(self, user_id:str, day:date):

        events = self._event_repository.get_by_user_and_day(user_id, day)
        return events