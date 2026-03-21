# ======= sqlite_environment_repository.py =======

# ===== Imports =====
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
                metadata TEXT
            )
        """)
        self.connection.commit()

    # ------------------
    def save(self, environment:Environment) -> None:
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO environments (id, owner_id, name, objects, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            environment.id,
            environment.owner_id,
            environment.name,
            json.dumps([obj.get_info() for obj in environment.objects]),
            json.dumps(environment.metadata)
        ))
        self.connection.commit()

    # ------------------
    def _row_to_environment(self, row) -> Environment:
        environment = Environment(
            id=row["id"],
            owner_id=row["owner_id"],
            name=row["name"],
            objects=[],  # les objets seront ajoutés via service plus tard
            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
        )
        return environment

    # ------------------
    def get_by_id(self, environment_id:str) -> Optional[Environment]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM environments WHERE id = ?", (environment_id,))
        row = cursor.fetchone()
        return self._row_to_environment(row) if row else None

    # ------------------
    def get_by_owner(self, owner_id:str) -> List[Environment]:
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