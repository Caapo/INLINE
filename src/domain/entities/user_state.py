# ============ Imports ============
from datetime import datetime


# ============ Notes ============  
# Cette classe permet de représenter l'état actuel d'un utilisateur dans l'application, en stockant des informations 
# telles que l'environnement actuel, les intentions actives, l'événement en cours, le module ouvert...



# ============ Class ============  

class UserState:

    def __init__(self, user_id:str, current_environment_id:Optional[str] = None, active_intention_id:Optional[str] = None, current_event_id:Optional[str] = None,
        opened_module_id:Optional[str] = None, metadata:Optional[dict] = None
    ):

        self._user_id = user_id
        self._current_environment_id = current_environment_id
        self._active_intention_id = active_intention_id
        self._current_event_id = current_event_id
        self._opened_module_id = opened_module_id
        self._session_started_at = datetime.utcnow()
        self._metadata = metadata or {}

    # ----------------------

    def set_current_environment(self, environment_id:str):

        self._current_environment_id = environment_id

    # ----------------------

    def activate_intention(self, intention_id:str):

        self._active_intention_id = intention_id

    # ----------------------

    def clear_intention(self):

        self._active_intention_id = None

    # ----------------------

    def get_snapshot(self):

        return {
            "user_id": self._user_id,
            "current_environment_id": self._current_environment_id,
            "active_intention_id": self._active_intention_id,
            "current_event_id": self._current_event_id,
            "opened_module_id": self._opened_module_id,
            "session_started_at": self._session_started_at,
            "metadata": self._metadata
        }