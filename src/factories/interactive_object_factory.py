# ====== INLINE/src/factories/interactive_object_factory.py ========
# Factory pour créer des objets interactifs à partir de données brutes.
# Permet d'abstraire la logique de création et de conversion des objets interactifs.

from domain.entities.clickable_object import ClickableObject
from domain.enums.enums import ObjectCategory

class InteractiveObjectFactory:
    """
    Factory pour créer des objets interactifs à partir de données brutes.
    Permet d'abstraire la logique de création et de conversion des objets interactifs.
    """

    @staticmethod
    def create(type:str, id:str, environment_id:str, name:str, position:tuple[int,int], category:ObjectCategory, suggested_intentions=None,
        metadata=None):
        """
        Crée un objet interactif selon son type.
        Lève ValueError si le type est inconnu.
        Actuellement supporte : 'clickable'.
        Extensible à 'draggable', 'inspectable', etc.
        """
        if type == "clickable":
            return ClickableObject(
                id=id,
                environment_id=environment_id,
                name=name,
                position=position,
                category=category,
                suggested_intentions=suggested_intentions or [],
                metadata=metadata or {}
            )
        # Futur: draggable, inspectable, etc.
        raise ValueError(f"Unknown object type: {type}")


    @staticmethod
    def from_dict(obj_dict:dict):
        """
        Reconstruit un objet interactif depuis un dictionnaire.
        Utilisé par Environment.from_persistence() pour restaurer
        les objets stockés en JSON dans la base.
        """
        obj_type = obj_dict.get("type")
        data = obj_dict.get("data", {})

        if obj_type == "clickable":
            return ClickableObject(
                id=data["id"],
                environment_id=data["environment_id"],
                name=data["name"],
                position=tuple(data["position"]),
                category=ObjectCategory[data["category"]],
                suggested_intentions=data.get("suggested_intentions", []),
                metadata=data.get("metadata", {})
            )

        raise ValueError(f"Unknown object type: {obj_type}")