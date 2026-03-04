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

    #Permet de récupérer un user depuis la BDD à partir de son email (sert à la connexion)
    def find_user_by_email(self, email: str) -> Optional[User]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT id, email, username, created_at FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()

        if row:
            user_id, email, username, created_at = row
            created_at_dt = datetime.fromisoformat(created_at)

            #arguments nommés simplement pour la lisibilité du code
            return User.from_persistence(user_id=user_id, email=email, username=username, created_at=created_at_dt)

        return None