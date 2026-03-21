# ==================================== sqlite_intention_repository.py ====================================

# ============ Imports ============
import sqlite3
import json
from typing import List, Optional
from datetime import datetime

from domain.entities.intention import Intention
from domain.repositories.i_intention_repository import IIntentionRepository


# ============ Class ============
class SQLiteIntentionRepository(IIntentionRepository):

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    # ------------------

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intentions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                object_id TEXT,
                category TEXT,
                title TEXT NOT NULL,
                is_active INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            )
        """)
        #Une seule intention active par utilisateur
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_active_intention
            ON intentions(user_id)
            WHERE is_active = 1
        """)
        self.connection.commit()

    # ------------------

    def save(self, intention: Intention) -> None:
        cursor = self.connection.cursor()

        data = intention.to_persistence()

        cursor.execute("""
            INSERT OR REPLACE INTO intentions 
            (id, user_id, object_id, category, title, is_active, created_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"],
            data["user_id"],
            data.get("object_id"),
            data.get("category"),
            data["title"],
            1 if data["is_active"] else 0,
            data["created_at"], #iso
            data["metadata"] #json
        ))

        self.connection.commit()

    # ------------------

    def _row_to_intention(self, row) -> Intention:
        return Intention.from_persistence(
            id=row["id"],
            user_id=row["user_id"],
            object_id=row["object_id"],
            category=row["category"],
            title=row["title"],
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
        )

    # ------------------

    def get_by_id(self, intention_id: str) -> Optional[Intention]:
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT * FROM intentions WHERE id = ?
        """, (intention_id,))

        row = cursor.fetchone()
        return self._row_to_intention(row) if row else None

    # ------------------

    def get_by_user(self, user_id: str) -> List[Intention]:
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT * FROM intentions WHERE user_id = ?
        """, (user_id,))

        rows = cursor.fetchall()

        intentions = []
        for row in rows:
            intention = self._row_to_intention(row)
            if intention:
                intentions.append(intention)

        return intentions

    # ------------------

    def get_active(self, user_id: str) -> Optional[Intention]:
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT * FROM intentions 
            WHERE user_id = ? AND is_active = 1
            LIMIT 1
        """, (user_id,))

        row = cursor.fetchone()
        return self._row_to_intention(row) if row else None