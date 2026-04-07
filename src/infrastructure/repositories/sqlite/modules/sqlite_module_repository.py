# src/infrastructure/repositories/sqlite/modules/sqlite_module_repository.py
# Implémentation SQLite du repository des modules.
# La configuration du module est stockée en JSON dans la colonne 'config'
# et restaurée via from_persistence() au chargement.

import sqlite3
import json
from typing import List, Optional

from domain.entities.modules.pomodoro.pomodoro_module import PomodoroModule
from domain.repositories.modules.i_module_repository import IModuleRepository


class SQLiteModuleRepository(IModuleRepository):
    """
    Implémentation SQLite du repository des modules.
    La configuration du module est stockée en JSON dans la colonne 'config'
    et restaurée via from_persistence() au chargement.
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
            CREATE TABLE IF NOT EXISTS modules (
                id           TEXT PRIMARY KEY,
                owner_id     TEXT NOT NULL,
                name         TEXT NOT NULL,
                type         TEXT NOT NULL,
                intention_id TEXT,
                config       TEXT,
                created_at   TEXT NOT NULL,
                updated_at   TEXT NOT NULL,
                metadata     TEXT
            )
        """)
        self.connection.commit()


    def _row_to_module(self, row) -> PomodoroModule:
        return PomodoroModule.from_persistence(
            id=row["id"],
            owner_id=row["owner_id"],
            name=row["name"],
            config_json=row["config"],
            intention_id=row["intention_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            metadata_json=row["metadata"]
        )

    def save(self, module: PomodoroModule) -> None:
        cursor = self.connection.cursor()
        data   = module.to_persistence()
        cursor.execute("""
            INSERT OR REPLACE INTO modules
            (id, owner_id, name, type, intention_id, config, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"], data["owner_id"], data["name"], data["type"],
            data["intention_id"], data["config"],
            data["created_at"], data["updated_at"], data["metadata"]
        ))
        self.connection.commit()

    def delete(self, module_id: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM modules WHERE id = ?", (module_id,))
        self.connection.commit()


    # ==========================
    # GETTERS ET AUTRES
    # ==========================

    def get_by_id(self, module_id: str) -> Optional[PomodoroModule]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
        row = cursor.fetchone()
        return self._row_to_module(row) if row else None

    def get_by_owner(self, owner_id: str) -> List[PomodoroModule]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM modules WHERE owner_id = ? ORDER BY updated_at DESC",
            (owner_id,)
        )
        return [self._row_to_module(row) for row in cursor.fetchall()]

    def get_by_intention(self, intention_id: str) -> List[PomodoroModule]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM modules WHERE intention_id = ?", (intention_id,)
        )
        return [self._row_to_module(row) for row in cursor.fetchall()]

