# =================== INLINE/src/domain/entities/intention.py ===================
# Entité métier centrale : représente une volonté déclarée
# par l'utilisateur. Unité fondamentale du système INLINE.


from datetime import datetime
from typing import Optional
from typing import Any
import json
   

class Intention:
    """
    Représente une volonté déclarée par l'utilisateur.

    Une intention est l'unité centrale du modèle INLINE.
    Elle peut exister sans horaire, être activée (focus) ou
    désactivée, et être enrichie par des notes, des modules
    ou des événements via les services associés.

    Attributs:
        _id (str): Identifiant unique de l'intention.
        _user_id (str): Identifiant de l'utilisateur propriétaire.
        _title (str): Titre déclaratif de l'intention.
        _category (str): Catégorie de l'intention (Retirer du projet, peut servir plus tard).
        _object_id (str | None): Objet interactif ayant déclenché
            la création de l'intention (optionnel).
        _is_active (bool): Indique si l'intention est le focus actuel.
        _created_at (datetime): Date de création.
        _metadata (dict): Données extensibles sans modifier la classe.
    """

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================

    def __init__(self, id:str, user_id:str, title:str, category:str, object_id:Optional[str]=None, created_at:Optional[datetime]=None, metadata:Optional[dict[str, Any]]=None):
        self._id = id
        self._user_id = user_id
        self._title = title
        self._category = category
        self._object_id = object_id
        self._is_active = False
        self._created_at = created_at or datetime.utcnow()
        self._metadata = metadata or {}

    # ==================================================
    # PERSISTANCE
    # ==================================================

    @classmethod
    def from_persistence(cls, id:str, user_id:str, title:str, category:str, object_id:Optional[str], is_active:bool, created_at:datetime, metadata:Optional[dict[str, Any]]=None) -> "Intention":
        """
        Reconstruit une intention depuis les données persistées en base.
        Contourne __init__ pour restaurer l'état exact sans réinitialiser
        les valeurs par défaut (ex: is_active).
        """
        intention = cls.__new__(cls)
        intention._id = id
        intention._user_id = user_id
        intention._title = title
        intention._category = category
        intention._object_id = object_id
        intention._is_active = is_active
        intention._created_at = created_at
        intention._metadata = metadata or {}
        return intention


    def to_persistence(self) -> dict:
        """
        Transforme l'intention en dictionnaire pour la sauvegarde en base.
        """
        return {
            "id": self._id,
            "user_id": self._user_id,
            "object_id": self._object_id,
            "category": self._category,
            "title": self._title,
            "is_active": self._is_active,
            "created_at": self._created_at.isoformat(),
            "metadata": json.dumps(self._metadata)
        }

    # ==================================================
    # MÉTHODES MÉTIER
    # ==================================================

    def rename(self, new_title:str):
        """
        Renomme l'intention.
        Lève ValueError si le nouveau titre est vide.
        """
        if not new_title:
            raise ValueError("Le titre de l'intention ne peut pas être vide.")
        self._title = new_title


    def activate(self):
        """
        Active l'intention — la désigne comme focus courant.
        Un seul focus actif par utilisateur est garanti par
        IntentionService qui désactive le précédent.
        """
        self._is_active = True


    def deactivate(self):
        """
        Désactive l'intention — la retire du focus courant.
        """
        self._is_active = False

    # ==================================================
    # REPRÉSENTATION
    # ==================================================

    def __repr__(self):
        """
        Représentation textuelle de l'intention pour le débogage.
        """
        return f"Intention(id={self._id}, title={self._title}, active={self._is_active})"


    # ==================================================
    # PROPRIÉTÉS (LECTURE SEULE)
    # ==================================================
    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def title(self):
        return self._title
    
    @property
    def category(self):
        return self._category
    
    @property
    def object_id(self):
        return self._object_id

    @property
    def is_active(self):
        return self._is_active

    @property
    def created_at(self):
        return self._created_at

    @property
    def metadata(self):
        return self._metadata

    # ==================================================
    # AUTRES
    # ==================================================

    def get_info(self):
        """
        Retourne un dictionnaire complet des données de l'intention.
        """
        return {
            "id": self._id,
            "user_id": self._user_id,
            "title": self._title,
            "category": self._category,
            "object_id": self._object_id,
            "is_active": self._is_active,
            "created_at": self._created_at,
            "metadata": self._metadata
        }