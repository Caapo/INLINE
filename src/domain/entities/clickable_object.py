# ======== INLINE/src/domain/entities/clickable_object.py =========
# Un objet interactif cliquable dans un environnement.
# Permet de représenter des éléments avec lesquels l'utilisateur peut interagir.


from domain.entities.i_interactive_object import IInteractiveObject
from domain.enums.enums import ObjectCategory
from typing import List, Optional


class ClickableObject(IInteractiveObject):
    """
    Objet interactif cliquable permettant de créer des intentions.
    Implémentation concrète de IInteractiveObject.
    Sert de point d'ancrage cognitif dans la visualisation.
    L'utilisateur clique sur un objet familier pour déclarer une intention.

    Attributs:
        id (str): Identifiant unique de l'objet.
        environment_id (str): Identifiant de l'environnement auquel l'objet appartient.
        name (str): Nom de l'objet.
        position (tuple[int, int]): Position de l'objet dans l'environnement (x, y).
        category (ObjectCategory): Catégorie de l'objet (ex: meuble, appareil, ...).
        suggested_intentions (List[str]): Liste d'intentions suggérées associées à l'objet.
        metadata (dict): Données extensibles sans modifier la classe.
    """

    # ===================================================
    # CONSTRUCTEUR
    # ===================================================
    def __init__(self, id:str, environment_id:str, name:str, position:tuple[int,int], category:ObjectCategory, suggested_intentions:Optional[List[str]]=None, metadata:Optional[dict]=None):
        self.id = id
        self.environment_id = environment_id
        self.name = name
        self.position = position
        self.category = category
        self.suggested_intentions = suggested_intentions or []
        self.metadata = metadata or {}


    # ===================================================
    # MÉTHODES MÉTIER
    # ===================================================

    def interact(self, user_state, input_value:Optional[str] = None):
        """
        Interagit avec l'objet cliquable.
        Retourne les suggestions associées à l'objet si aucune
        valeur saisie, ou la valeur personnalisée sinon.
        """
        if input_value:
            return {"custom_intention": input_value, "object_id": self.id}
        else:
            return {"suggestions": self.suggested_intentions, "object_id": self.id}


    def add_suggestion(self, intention:str):
        """
        Ajoute une intention suggérée à l'objet.
        """
        self.suggested_intentions.append(intention)


    def remove_suggestion(self, intention:str):
        """
        Retire une intention suggérée de l'objet.
        """
        if intention in self.suggested_intentions:
            self.suggested_intentions.remove(intention)

    
    def rename(self, new_name:str):
        """
        Renomme l'objet cliquable.
        """
        if not new_name:
            raise ValueError("Le nom ne peut pas être vide.")
        self.name = new_name

    

    def set_category(self, category:ObjectCategory):
        """
        Modifie la catégorie de l'objet cliquable.
        """
        self.category = category



    # ===================================================
    # GETTERS ET AUTRES
    # ===================================================
    
    def get_metadata(self) -> dict:
        return self.metadata
    
    #----------------------

    def get_position(self) -> tuple[int,int]:
        return self.position

    #----------------------

    def get_type(self):
        return "clickable"

    #----------------------

    def get_info(self) -> dict:
        return {
            "type": "clickable",
            "data": {
                "id": self.id,
                "environment_id": self.environment_id,
                "name": self.name,
                "position": self.position,
                "category": self.category.name,
                "suggested_intentions": self.suggested_intentions,
                "metadata": self.metadata
            }
        }