# ======== INLINE/src/domain/entities/environment.py =========
# Un environnement est un conteneur d'objets interactifs (physiques ou mentaux) qui composent l'espace de vie de l'utilisateur.
# Par exemple : chambre, bureau, salle de sport, état mental...
# L'environnement est personnalisable et évolutif.

from typing import List, Optional, Any
from datetime import datetime
import json

from domain.entities.i_interactive_object import IInteractiveObject
from factories.interactive_object_factory import InteractiveObjectFactory


class Environment:
     """
    Conteneur d'objets interactifs représentant un espace de vie.
    Correspond à un environnement physique ou mental de l'utilisateur
    (chambre, bureau, salle de sport...) modélisé en 2D.
    Ne contient pas de logique métier — gère uniquement
    la composition de ses objets interactifs.

    Attributs:
        _id (str): Identifiant unique de l'environnement.
        _owner_id (str): Identifiant de l'utilisateur propriétaire.
        _name (str): Nom de l'environnement.
        _objects (List[IInteractiveObject]): Liste d'objets interactifs présents dans l'environnement.
        _created_at (datetime): Date de création de l'environnement.
        _metadata (dict): Données extensibles sans modifier la classe.
    """

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================
    def __init__(self, id:str, owner_id:str, name:str, objects:Optional[List[IInteractiveObject]]=None, metadata:Optional[dict[str, Any]]=None):
        self._id = id
        self._owner_id = owner_id
        self._name = name
        self._objects = objects or []
        self._created_at = datetime.utcnow()
        self._metadata = metadata or {}
        

    # ==================================================
    # PERSISTANCE
    # ==================================================

    def to_persistence(self) -> dict:
        """
        Prépare l'environnement pour la persistance en base.
        """
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "name": self.name,
            "objects": json.dumps([o.get_info() for o in self.objects]),
            "metadata": json.dumps(self._metadata),
            "created_at": self._created_at.isoformat()
        }


    @classmethod
    def from_persistence(cls, id, owner_id, name, objects, metadata, created_at):
        """
        Reconstruit un Environment depuis la base.
        """
        reconstructed_objects = []

        for obj_dict in objects:
            reconstructed_objects.append(
                InteractiveObjectFactory.from_dict(obj_dict)
            )

        env = cls(
            id=id,
            owner_id=owner_id,
            name=name,
            objects=reconstructed_objects,
            metadata=metadata
        )

        env._created_at = datetime.fromisoformat(created_at)

        return env

    # ==================================================
    # MÉTHODES MÉTIER
    # ==================================================

    def add_interactive_object(self, obj:IInteractiveObject):
        """
        Ajoute un objet interactif à l'environnement.
        """
        self._objects.append(obj)

    
    def remove_interactive_object(self, obj_id:str):
        """
        Supprime un objet interactif de l'environnement par son ID.
        """
        self._objects = [o for o in self._objects if o.id != obj_id]
    

    # ==================================================
    # REPRÉSENTATION
    # ==================================================

    def __repr__(self):
        """
        Représentation textuelle de l'environnement pour le débogage.
        """
        return f"Environment(id={self._id}, owner_id={self._owner_id}, name={self._name}, objects={len(self._objects)})"


    # ==================================================
    # PROPRIÉTÉS
    # ==================================================

    @property
    def id(self) -> str:
        return self._id

    @property
    def owner_id(self) -> str:
        return self._owner_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def objects(self) -> List[IInteractiveObject]:
        return self._objects


    # ==================================================
    # GETTERS ET AUTRES
    # ==================================================

    def get_interactive_object(self, obj_id:str) -> Optional[IInteractiveObject]:
        """
        Récupère un objet interactif de l'environnement par son ID.
        """
        for o in self._objects:
            if o.id == obj_id:
                return o
        return None


    def get_info(self):
        """
        Récupère les informations de l'environnement sous forme de dictionnaire.
        """
        return {
            "id": self._id,
            "owner_id": self._owner_id,
            "name": self._name,
            "objects": [o.get_info() for o in self._objects],
            "metadata": self._metadata,
            "created_at": self._created_at
        }