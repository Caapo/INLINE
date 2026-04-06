# ==================== INLINE/src/infrastructure/repositories/sqlite/sqlite_event_repository.py ====================
# Implémentation SQLite du repository des événements.
# (Couche infrastructure)


import sqlite3
import json
from typing import List, Optional
from datetime import datetime, date

from domain.entities.event import Event
from domain.repositories.i_event_repository import IEventRepository


class SQLiteEventRepository(IEventRepository):
    """
    Implémentation du repository des événements via SQLite.
    Gère la persistance des événements dans une base de données

    Attributs:
        connection (sqlite3.Connection): Connexion à la base de données SQLite.
    """

    #===================================================
    # CONSTRUCTEUR
    #===================================================

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    # ===================================================
    # MÉTHODES PRINCIPALES
    # ===================================================

    def _create_table(self):
        """
        Crée la table "events" si elle n'existe pas déjà.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                intention_id TEXT NOT NULL,
                environment_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                duration INTEGER NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            )
        """)
        self.connection.commit()


    def save(self, event:Event) -> None:
        """
        INSERT OR REPLACE gère création et mise à jour.
        """
        cursor = self.connection.cursor()
        event_info = event.to_persistence()
        cursor.execute("""
            INSERT OR REPLACE INTO events (id, intention_id, environment_id, start_time, duration, end_time, status, created_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (event_info["id"], event_info["intention_id"], event_info["environment_id"], event_info["start_time"], event_info["duration"], event_info["end_time"], event_info["status"],
            event_info["created_at"], event_info["metadata"])
        )
        self.connection.commit()


    def delete(self, event_id: str) -> None:
        """
        Supprime un événement de la base de données.
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.connection.commit()


    def _row_to_event(self, row) -> Event:
        """
        Convertit une ligne SQLite en instance d'Event via from_persistence().
        Parse les datetimes depuis leur format ISO stocké en TEXT.
        """
        return Event.from_persistence(
            id=row["id"],
            intention_id=row["intention_id"],
            environment_id=row["environment_id"],
            start_time=datetime.fromisoformat(row["start_time"]),
            duration=row["duration"],
            end_time=datetime.fromisoformat(row["end_time"]),
            status=row["status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
        )

    
    # ==================================================
    # GETTERS ET AUTRES
    # ==================================================

    def get_by_id(self, event_id:str) -> Optional[Event]:
        """
        Récupère un événement par son ID.
        Retourne None si l'événement n'existe pas.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, intention_id, environment_id, start_time, duration, end_time, status, created_at, metadata FROM events WHERE id = ?", (event_id,))
        row = cursor.fetchone()
        return self._row_to_event(row) if row else None


    def get_by_intention(self, intention_id:str) -> List[Event]:
        """
        Récupère tous les événements associés à une intention donnée.
        Retourne une liste d'Event, vide si aucun trouvé.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, intention_id, environment_id, start_time, duration, end_time, status, created_at, metadata FROM events WHERE intention_id = ?", (intention_id,))
        rows = cursor.fetchall()
        events = []
        for row in rows:
            event = self._row_to_event(row)
            if event:
                events.append(event)
        return events


    def get_by_date(self, day:date) -> List[Event]:
        """
        Récupère tous les événements d'une journée donnée.
        Retourne une liste d'Event, vide si aucun trouvé.
        """
        cursor = self.connection.cursor()
        day_start = datetime.combine(day, datetime.min.time()).isoformat()
        day_end = datetime.combine(day, datetime.max.time()).isoformat()
        cursor.execute("SELECT id, intention_id, environment_id, start_time, duration, end_time, status, created_at, metadata FROM events WHERE start_time BETWEEN ? AND ?", (day_start, day_end))
        rows = cursor.fetchall()
        events = []
        for row in rows:
            event = self._row_to_event(row)
            if event:
                events.append(event)
        return events


    def get_by_environment_and_date(self, environment_id:str, day:date) -> List[Event]:
        """
        Récupère tous les événements d'un environnement donné pour une journée donnée.
        Retourne une liste d'Event, vide si aucun trouvé.
        Résultats triés par start_time croissant
        """
        cursor = self.connection.cursor()
        day_start = datetime.combine(day, datetime.min.time()).isoformat()
        day_end = datetime.combine(day, datetime.max.time()).isoformat()

        cursor.execute("""
            SELECT * FROM events 
            WHERE environment_id = ? 
            AND start_time BETWEEN ? AND ?
        """, (environment_id, day_start, day_end))

        rows = cursor.fetchall()
        return sorted([self._row_to_event(row) for row in rows], key=lambda e:e.start_time)


    def get_between(self, environment_id:str, start:datetime, end:datetime) -> List[Event]:
        """
        Récupère tous les événements d'un environnement donné entre deux dates.
        Retourne une liste d'Event, vide si aucun trouvé.
        Résultats triés par start_time croissant
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM events 
            WHERE environment_id = ? 
            AND start_time BETWEEN ? AND ?
        """, (environment_id, start.isoformat(), end.isoformat()))
        rows = cursor.fetchall()
        return sorted([self._row_to_event(row) for row in rows], key=lambda e:e.start_time)



