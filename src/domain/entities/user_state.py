from datetime import datetime


class UserState:

    def __init__(self, user_id: str, current_environment_id: str | None = None, active_intention_id: str | None = None, current_event_id: str | None = None,
        opened_module_id: str | None = None, metadata: dict | None = None
    ):

        self._user_id = user_id
        self._current_environment_id = current_environment_id
        self._active_intention_id = active_intention_id
        self._current_event_id = current_event_id
        self._opened_module_id = opened_module_id
        self._session_started_at = datetime.utcnow()
        self._metadata = metadata or {}

    # ----------------------

    def set_current_environment(self, environment_id: str):

        self._current_environment_id = environment_id

    # ----------------------

    def activate_intention(self, intention_id: str):

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