# src/infrastructure/repositories/sqlite/modules/pomodoro/sqlite_pomodoro_session_repository.py
# Implémentation SQLite du repository des sessions Pomodoro.
# Utilisée par ModuleService pour persister l'historique des sessions.


import sqlite3
from typing import List
from datetime import datetime, date

from domain.entities.modules.pomodoro.pomodoro_session import PomodoroSession
from domain.repositories.modules.pomodoro.i_pomodoro_session_repository import IPomodoroSessionRepository


class SQLitePomodoroSessionRepository(IPomodoroSessionRepository):
    """
    Implémentation SQLite du repository des sessions Pomodoro.
    Utilisée par ModuleService pour persister l'historique des sessions
    et par AnalyticsService pour les statistiques de la page État.
    """

    # ==========================
    # CONSTRUCTEUR
    # ==========================

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    # ==========================
    # MÉTHODES PRINCIPALES
    # ==========================

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pomodoro_sessions (
                id             TEXT PRIMARY KEY,
                module_id      TEXT NOT NULL,
                work_duration  INTEGER NOT NULL,
                break_duration INTEGER NOT NULL,
                status         TEXT NOT NULL,
                started_at     TEXT NOT NULL,
                ended_at       TEXT
            )
        """)
        self.connection.commit()


    def _row_to_session(self, row) -> PomodoroSession:
        return PomodoroSession.from_persistence(
            id=row["id"],
            module_id=row["module_id"],
            work_duration=row["work_duration"],
            break_duration=row["break_duration"],
            status=row["status"],
            started_at=row["started_at"],
            ended_at=row["ended_at"]
        )


    def save(self, session: PomodoroSession) -> None:
        cursor = self.connection.cursor()
        data   = session.to_persistence()
        cursor.execute("""
            INSERT OR REPLACE INTO pomodoro_sessions
            (id, module_id, work_duration, break_duration, status, started_at, ended_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"], data["module_id"], data["work_duration"],
            data["break_duration"], data["status"],
            data["started_at"], data["ended_at"]
        ))
        self.connection.commit()


    def delete_by_module(self, module_id: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM pomodoro_sessions WHERE module_id = ?", (module_id,)
        )
        self.connection.commit()


    # ==========================
    # GETTERS ET AUTRES
    # ==========================

    def get_by_module(self, module_id: str) -> List[PomodoroSession]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM pomodoro_sessions WHERE module_id = ? ORDER BY started_at DESC",
            (module_id,)
        )
        return [self._row_to_session(row) for row in cursor.fetchall()]


    def get_by_date(self, day: date) -> List[PomodoroSession]:
        cursor    = self.connection.cursor()
        day_start = datetime.combine(day, datetime.min.time()).isoformat()
        day_end   = datetime.combine(day, datetime.max.time()).isoformat()
        cursor.execute("""
            SELECT * FROM pomodoro_sessions
            WHERE started_at BETWEEN ? AND ?
            ORDER BY started_at DESC
        """, (day_start, day_end))
        return [self._row_to_session(row) for row in cursor.fetchall()]


    def get_by_module_and_date(self, module_id: str, day: date) -> List[PomodoroSession]:
        cursor    = self.connection.cursor()
        day_start = datetime.combine(day, datetime.min.time()).isoformat()
        day_end   = datetime.combine(day, datetime.max.time()).isoformat()
        cursor.execute("""
            SELECT * FROM pomodoro_sessions
            WHERE module_id = ? AND started_at BETWEEN ? AND ?
            ORDER BY started_at ASC
        """, (module_id, day_start, day_end))
        return [self._row_to_session(row) for row in cursor.fetchall()]

