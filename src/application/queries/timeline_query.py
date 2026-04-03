# ========= INLINE/src/application/queries/timeline_query.py =========

# ======== Imports ========
from datetime import datetime, date
from typing import List
from domain.entities.event import Event
from infrastructure.repositories.sqlite.sqlite_event_repository import SQLiteEventRepository

class TimelineQuery:

    def __init__(self, event_repository:SQLiteEventRepository):
        self._event_repository = event_repository

    def get_events_for_environment_and_day(self, environment_id:str, day:date) -> List[Event]:
        events = self._event_repository.get_by_date(day)
        return [e for e in events if e.environment_id == environment_id]