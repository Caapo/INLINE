# src/domain/entities/modules/pomodoro/pomodoro_session.py
# Représente une session de travail enregistrée par le module Pomodoro.
# Unité de données analytiques - chaque session complétée ou interrompue
# est persistée pour alimenter la page État/Activités.


from datetime import datetime
from typing import Optional

from domain.enums.enums import SessionStatus


class PomodoroSession:
    """
    Représente une session de travail enregistrée par le module Pomodoro.
    Unité de données analytiques — chaque session complétée ou interrompue
    est persistée pour alimenter la page État/Activités.

    Une session correspond uniquement à une phase de TRAVAIL.
    Les pauses ne sont pas enregistrées comme sessions distinctes.

    Attributs:
        _work_duration (int): Durée de travail en minutes.
        _break_duration (int): Durée de la pause.
        _status (SessionStatus): COMPLETED ou INTERRUPTED.
        _started_at (datetime): Heure de début de la session.
        _ended_at (datetime | None): Heure de fin de la session.
    """

    # =================================================
    # CONSTRUCTEUR
    # =================================================
    
    def __init__(self, id:str, module_id:str, work_duration:int, break_duration:int, status:str=SessionStatus.COMPLETED.value,
    started_at:Optional[datetime]=None, ended_at:Optional[datetime]=None):
        self._id = id
        self._module_id = module_id
        self._work_duration = work_duration 
        self._break_duration = break_duration
        self._status = SessionStatus(status)
        self._started_at = started_at or datetime.utcnow()
        self._ended_at = ended_at

    # ==============================================
    # PERSISTANCE
    # ==============================================

    def to_persistence(self) -> dict:
        return {
            "id": self._id,
            "module_id": self._module_id,
            "work_duration": self._work_duration,
            "break_duration": self._break_duration,
            "status": self._status.value,
            "started_at": self._started_at.isoformat(),
            "ended_at": self._ended_at.isoformat() if self._ended_at else None
        }

    @classmethod
    def from_persistence(cls, id:str, module_id:str, work_duration:int, break_duration:int, status:str, started_at:str,
    ended_at: Optional[str]) -> "PomodoroSession":
        s = cls.__new__(cls)
        s._id = id
        s._module_id = module_id
        s._work_duration = work_duration
        s._break_duration = break_duration
        s._status = SessionStatus(status)
        s._started_at = datetime.fromisoformat(started_at)
        s._ended_at = datetime.fromisoformat(ended_at) if ended_at else None
        return s

    # ==============================================
    # PROPRIÉTÉS
    # ==============================================
    
    @property
    def id(self) -> str:
        return self._id

    @property
    def module_id(self) -> str:               
        return self._module_id

    @property
    def work_duration(self) -> int:               
        return self._work_duration

    @property
    def break_duration(self) -> int:               
        return self._break_duration

    @property
    def status(self) -> str:               
        return self._status.value

    @property
    def started_at(self) -> datetime:          
        return self._started_at

    @property
    def ended_at(self) -> Optional[datetime]: 
        return self._ended_at


    def get_info(self) -> dict:
        return self.to_persistence()