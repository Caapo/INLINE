# ==================== INLINE/src/infrastructure/repositories/sqlite/sqlite_intention_repository.py ====================
# Implémentation SQLite du repository des intentions.
# (Couche infrastructure)

# ============ Imports ============
import sqlite3
import json
from typing import List, Optional
from datetime import datetime

from domain.entities.intention import Intention
from domain.repositories.i_intention_repository import IIntentionRepository


class SQLiteIntentionRepository(IIntentionRepository):
    """
    Implémentation concrète du repository des intentions via SQLite.
    Gère la persistance des intentions dans une base de données
    SQLite locale. Traduit les objets domaine en données relationnelles
    et vice versa via les méthodes to_persistence() et from_persistence().

    Attributs:
        connection (sqlite3.Connection): Connexion à la base de données SQLite.
    """
    def __init__(self, db_path:str):
        """
        Initialise la connexion SQLite et crée la table si nécessaire.
        Args:
            db_path (str): Chemin vers le fichier de base de données.
        """
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    # ------------------

    def _create_table(self):
        """
        Crée la table "intentions" si elle n'existe pas déjà.
        """
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

        #Garantit une seule intention active par utilisateur
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_active_intention
            ON intentions(user_id)
            WHERE is_active = 1
        """)
        self.connection.commit()

    # ------------------

    def save(self, intention: Intention) -> None:
        """
        Insère ou remplace une intention en base.
        INSERT OR REPLACE gère à la fois la création et la mise à jour.
        """
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
        """
        Convertit une ligne SQLite en instance d'Intention.
        Utilise from_persistence() pour reconstruire l'état exact.
        """
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
        """
        Récupère une intention par son id. Retourne None si absente.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM intentions WHERE id = ?
        """, (intention_id,))

        row = cursor.fetchone()
        return self._row_to_intention(row) if row else None

    # ------------------

    def get_by_user(self, user_id: str) -> List[Intention]:
        """
        Récupère toutes les intentions d'un utilisateur.
        """
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
        """
        Retourne l'intention active (focus) d'un utilisateur.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM intentions 
            WHERE user_id = ? AND is_active = 1
            LIMIT 1
        """, (user_id,))

        row = cursor.fetchone()
        return self._row_to_intention(row) if row else None

    #------------------

    def get_all(self) -> list[Intention]:
        """
        Récupère toutes les intentions de tous les utilisateurs.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM intentions")
        rows = cursor.fetchall()
        return [self._row_to_intention(row) for row in rows]

    #------------------

    def delete(self, intention_id: str) -> None:
        """
        Supprime une intention de la base de données.
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM intentions WHERE id = ?", (intention_id,))
        self.connection.commit()