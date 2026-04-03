# ==================== INLINE/src/infrastructure/repositories/sqlite/sqlite_environment_repository.py ====================
import sqlite3
import json
from typing import List, Optional
from domain.entities.environment import Environment
from domain.repositories.i_environment_repository import IEnvironmentRepository

class SQLiteEnvironmentRepository(IEnvironmentRepository):
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS environments (
                id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                name TEXT NOT NULL,
                objects TEXT,
                metadata TEXT,
                created_at TEXT NOT NULL
            )
        """)
        self.connection.commit()

    # ------------------
    def save(self, environment: Environment) -> None:
        cursor = self.connection.cursor()
        environment_info = environment.to_persistence()
        cursor.execute("""
            INSERT OR REPLACE INTO environments (id, owner_id, name, objects, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            environment_info["id"],
            environment_info["owner_id"],
            environment_info["name"],
            environment_info["objects"],
            environment_info["metadata"],
            environment_info["created_at"]
        ))
        self.connection.commit()

    # ------------------

    def _row_to_environment(self, row) -> Environment:
        return Environment.from_persistence(
            id=row["id"],
            owner_id=row["owner_id"],
            name=row["name"],
            objects=json.loads(row["objects"]) if row["objects"] else [],
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
            created_at=row["created_at"]
            
        )

    # ------------------
    def get_by_id(self, environment_id: str) -> Optional[Environment]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM environments WHERE id = ?", (environment_id,))
        row = cursor.fetchone()
        return self._row_to_environment(row) if row else None

    # ------------------
    def get_by_owner(self, owner_id: str) -> List[Environment]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM environments WHERE owner_id = ?", (owner_id,))
        rows = cursor.fetchall()
        return [self._row_to_environment(row) for row in rows]

    # ------------------
    def list_all(self) -> List[Environment]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM environments")
        rows = cursor.fetchall()
        return [self._row_to_environment(row) for row in rows]

    #------------------
    def delete(self, env_id:str) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM environments WHERE id = ?", (env_id,))
        self.connection.commit()