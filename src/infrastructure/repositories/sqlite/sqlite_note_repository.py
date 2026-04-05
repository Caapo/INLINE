# src/infrastructure/repositories/sqlite/sqlite_note_repository.py

import sqlite3
import json
from typing import List, Optional
from domain.entities.note import Note
from domain.repositories.i_note_repository import INoteRepository


class SQLiteNoteRepository(INoteRepository):

    def __init__(self, db_path:str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    #------------------------

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id           TEXT PRIMARY KEY,
                owner_id     TEXT NOT NULL,
                intention_id TEXT,               -- nullable
                title        TEXT NOT NULL,
                blocks       TEXT,
                created_at   TEXT NOT NULL,
                updated_at   TEXT NOT NULL,
                metadata     TEXT
            )
        """)
        self.connection.commit()

    #------------------------

    def save(self, note: Note) -> None:
        cursor = self.connection.cursor()
        data   = note.to_persistence()
        cursor.execute("""
            INSERT OR REPLACE INTO notes
            (id, owner_id, intention_id, title, blocks, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"], data["owner_id"], data["intention_id"], data["title"],
            data["blocks"], data["created_at"], data["updated_at"], data["metadata"]
        ))
        self.connection.commit()

    #------------------------

    def _row_to_note(self, row) -> Note:
        return Note.from_persistence(
            id=row["id"],
            owner_id=row["owner_id"],
            title=row["title"],
            blocks_json=row["blocks"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            metadata_json=row["metadata"],
            intention_id=row["intention_id"] if row["intention_id"] else None
        )

    #------------------------

    def get_by_id(self, note_id:str) -> Optional[Note]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        return self._row_to_note(row) if row else None

    #------------------------

    def get_by_owner(self, owner_id:str) -> List[Note]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM notes WHERE owner_id = ? ORDER BY updated_at DESC", (owner_id,))
        return [self._row_to_note(row) for row in cursor.fetchall()]

    #------------------------

    def get_by_intention(self, intention_id: str) -> List[Note]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM notes WHERE intention_id = ? ORDER BY updated_at DESC",
            (intention_id,)
        )
        return [self._row_to_note(row) for row in cursor.fetchall()]

    #------------------------

    def delete(self, note_id:str) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.connection.commit()