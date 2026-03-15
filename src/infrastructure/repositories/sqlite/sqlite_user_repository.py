import sqlite3
from typing import Optional
from domain.entities.user import User
from domain.repositories.i_user_repository import IUserRepository
from datetime import datetime
import json


# ================ CLASS SQLiteUserRepository ================ (Implémente l'interface IUserRepository pour la persistance des utilisateurs dans la BDD)

class SQLiteUserRepository(IUserRepository):

    #Permet d'initialiser la connexion a la BDD
    def __init__(self, db_path:str):
        self.__connection = sqlite3.connect(db_path)
        self.__connection.row_factory = sqlite3.Row
        self.__create_table()

    # ---------------------------------------------------

    #Permet de créer la table users dans la BDD (si elle n'existe pas déjà)
    def __create_table(self):
        cursor = self.__connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users 
            (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            )
        """)
        self.__connection.commit()

    # ---------------------------------------------------

    #Permet d'enregistrer/mettre à jour un user dans la BDD
    def save_user(self, user:User) -> None:
        cursor = self.__connection.cursor()
        user_info = user.to_persistence()
        cursor.execute("""
            INSERT OR REPLACE INTO users (id, email, username, created_at, metadata)
            VALUES (?, ?, ?, ?, ?)""", 
            (user_info["id"], user_info["email"], user_info["username"], user_info["created_at"], user_info["metadata"])
        ) 
        self.__connection.commit()

    # ---------------------------------------------------

    def _row_to_user(self, row) -> User:
        return User.from_persistence(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            created_at=datetime.fromisoformat(row["created_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
        )

    # ---------------------------------------------------

    #Permet de récupérer un user depuis la BDD à partir de son email (sert à la connexion)
    def find_user_by_email(self, email: str) -> Optional[User]:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT id, email, username, created_at, metadata FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()

        return self._row_to_user(row) if row else None