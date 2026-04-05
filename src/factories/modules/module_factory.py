# src/factories/modules/module_factory.py

from uuid import uuid4
from datetime import datetime
from domain.entities.modules.pomodoro.pomodoro_module import PomodoroModule
from domain.enums.enums import ModuleType


class ModuleFactory:

    def create_pomodoro(self, owner_id:str, name:str, work_minutes:int=25, break_minutes:int=5, long_break_minutes:int=15, sessions_before_long:int=4) -> PomodoroModule:
        return PomodoroModule(
            id=str(uuid4()),
            owner_id=owner_id,
            name=name,
            work_minutes=work_minutes,
            break_minutes=break_minutes,
            long_break_minutes=long_break_minutes,
            sessions_before_long=sessions_before_long,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )