# ==== INLINE/src/application/services/module_service.py ====
# Service applicatif pour la gestion des modules.
# Orchestre les cas d'usage liés aux modules (création, mise à jour, suppression)
# et notifie les abonnés via le patron Observer.


from uuid import uuid4
from datetime import datetime, date
from typing import List, Optional

from domain.entities.modules.pomodoro.pomodoro_module import PomodoroModule
from domain.entities.modules.pomodoro.pomodoro_session import PomodoroSession
from domain.enums.enums import SessionStatus
from domain.repositories.modules.i_module_repository import IModuleRepository
from domain.repositories.modules.pomodoro.i_pomodoro_session_repository import IPomodoroSessionRepository
from domain.repositories.i_intention_repository import IIntentionRepository
from factories.modules.module_factory import ModuleFactory
from shared.observer import Observable


class ModuleService(Observable):
    """
    Service applicatif de gestion des modules et de leurs sessions.
    Orchestre toutes les opérations sur les modules Pomodoro
    et notifie l'UI via le patron Observer.
    """

    # ==============================
    # CONSTRUCTEUR
    # ==============================

    def __init__(self, module_repository: IModuleRepository, session_repository: IPomodoroSessionRepository, module_factory: ModuleFactory, 
    intention_repository:IIntentionRepository):
        super().__init__()
        self._module_repo = module_repository
        self._session_repo = session_repository
        self._module_factory = module_factory
        self._intention_repo = intention_repository

    # ==============================
    # MÉTHODES CAS D'USAGE
    # ==============================

    def create_pomodoro(self, owner_id:str, name:str, work_minutes:int=25, break_minutes:int=5,
    long_break_minutes:int=15, sessions_before_long:int=4) -> PomodoroModule:
        module = self._module_factory.create_pomodoro(
            owner_id=owner_id, name=name,
            work_minutes=work_minutes,
            break_minutes=break_minutes,
            long_break_minutes=long_break_minutes,
            sessions_before_long=sessions_before_long
        )
        self._module_repo.save(module)
        self.notify("module_created", module)
        return module

    #On peut ajouter d'autres types de modules à l'avenir, ex : HabitTrackerModule, etc.

    # Sessions Pomodoro 
    def record_session(self, module_id:str, work_duration:int, break_duration:int, status:str=SessionStatus.COMPLETED.value, started_at:Optional[datetime]=None,
    ended_at:Optional[datetime]=None) -> PomodoroSession:
        session = PomodoroSession(
            id=str(uuid4()),
            module_id=module_id,
            work_duration=work_duration,
            break_duration=break_duration,
            status=status,
            started_at=started_at or datetime.now(),
            ended_at=ended_at or datetime.now()
        )
        self._session_repo.save(session)
        self.notify("session_recorded", session)
        return session


    def rename_module(self, module_id:str, new_name:str) -> PomodoroModule:
        module = self._get_or_raise(module_id)
        module.rename(new_name)
        self._module_repo.save(module)
        self.notify("module_updated", module)
        return module


    def update_config(self, module_id:str, **kwargs) -> PomodoroModule:
        module = self._get_or_raise(module_id)
        module.update_config(**kwargs)
        self._module_repo.save(module)
        self.notify("module_updated", module)
        return module


    def attach_to_intention(self, module_id:str, intention_id:str) -> PomodoroModule:
        module    = self._get_or_raise(module_id)
        intention = self._intention_repo.get_by_id(intention_id)
        if not intention:
            raise ValueError(f"Intention introuvable : {intention_id}")
        module.attach_to_intention(intention_id)
        self._module_repo.save(module)
        self.notify("module_updated", module)
        return module


    def detach_from_intention(self, module_id:str) -> PomodoroModule:
        module = self._get_or_raise(module_id)
        module.detach_from_intention()
        self._module_repo.save(module)
        self.notify("module_updated", module)
        return module


    def delete_module(self, module_id:str) -> None:
        module = self._get_or_raise(module_id)
        self._session_repo.delete_by_module(module_id)
        self._module_repo.delete(module_id)
        self.notify("module_deleted", module_id)


    # ==============================
    # GETTERS ET AUTRES   
    # ==============================

    def get_module(self, module_id:str) -> Optional[PomodoroModule]:
        return self._module_repo.get_by_id(module_id)

    def get_modules_for_user(self, owner_id:str) -> List[PomodoroModule]:
        return self._module_repo.get_by_owner(owner_id)

    def get_modules_for_intention(self, intention_id:str) -> List[PomodoroModule]:
        return self._module_repo.get_by_intention(intention_id)





    def get_sessions_for_module(self, module_id: str) -> List[PomodoroSession]:
        return self._session_repo.get_by_module(module_id)

    def get_sessions_for_date(self, day: date) -> List[PomodoroSession]:
        return self._session_repo.get_by_date(day)

    def get_sessions_for_module_and_date(self, module_id: str, day: date) -> List[PomodoroSession]:
        return self._session_repo.get_by_module_and_date(module_id, day)

    # ------------ Analytique ------------

    def get_stats_for_module(self, module_id: str) -> dict:
        sessions   = self._session_repo.get_by_module(module_id)
        completed  = [s for s in sessions if s.status == SessionStatus.COMPLETED.value]
        interrupted = [s for s in sessions if s.status == SessionStatus.INTERRUPTED.value]

        total_work  = sum(s.work_duration  for s in completed)
        total_break = sum(s.break_duration for s in completed)

        return {
            "total_sessions":      len(sessions),
            "completed_sessions":  len(completed),
            "interrupted_sessions": len(interrupted),
            "total_work_minutes":  total_work,
            "total_break_minutes": total_break,
            "average_work_per_session": round(total_work / len(completed), 1) if completed else 0
        }

    def get_stats_for_date(self, day: date) -> dict:
        sessions  = self._session_repo.get_by_date(day)
        completed = [s for s in sessions if s.status == SessionStatus.COMPLETED.value]

        return {
            "date":               day.isoformat(),
            "total_sessions":     len(sessions),
            "completed_sessions": len(completed),
            "total_work_minutes": sum(s.work_duration for s in completed)
        }


    def _get_or_raise(self, module_id: str) -> PomodoroModule:
        module = self._module_repo.get_by_id(module_id)
        if not module:
            raise ValueError(f"Module introuvable : {module_id}")
        return module