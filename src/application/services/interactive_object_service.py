# === INLINE/application/services/interactive_object_service.py ===
# Service pour gérer les objets interactifs : création, récupération, mise à jour, suppression.
# Utilise le repository pour la persistance et la factory pour la création d'instances.

from typing import List, Optional
from domain.entities.i_interactive_object import IInteractiveObject
from domain.repositories.i_environment_repository import IEnvironmentRepository
from factories.interactive_object_factory import InteractiveObjectFactory
from domain.enums.enums import ObjectCategory

class InteractiveObjectService:
    """
    Service de gestion des objets interactifs. Permet de créer, récupérer, mettre à jour et supprimer des objets interactifs.
    Utilise un repository pour la persistance et une factory pour la création d'instances.
    """

    # ==============================
    # CONSTRUCTEUR
    # ==============================

    def __init__(self, environment_repo:IEnvironmentRepository, factory:InteractiveObjectFactory):
        self.environment_repo = environment_repo
        self.factory = factory


    # ==============================
    # MÉTHODES CAS D'USAGE
    # ==============================

    def create_object(self, environment_id:str, type:str, id:str, name:str, position:tuple[int,int], category:ObjectCategory,
        suggested_intentions:Optional[List[str]]=None, metadata:Optional[dict]=None) -> IInteractiveObject:
        """
        Crée un nouvel objet interactif dans un environnement donné et le sauvegarde via le repository.
        Lève ValueError si l'environnement n'existe pas ou si les données sont invalides
        """
        env = self.environment_repo.get_by_id(environment_id)
        if not env:
            raise ValueError(f"Environment {environment_id} not found")

        obj = self.factory.create(
            type=type,
            id=id,
            environment_id=environment_id,
            name=name,
            position=position,
            category=category,
            suggested_intentions=suggested_intentions,
            metadata=metadata
        )
        env.add_interactive_object(obj)
        self.environment_repo.save(env)
        return obj


    def interact_with_object(self, environment_id:str, object_id:str, user_state, input_value:Optional[str]=None):
        """
        Interagit avec un objet interactif donné en fonction de son ID et de l'environnement.
        Lève ValueError si l'environnement ou l'objet n'existe pas.
        """
        env = self.environment_repo.get_by_id(environment_id)
        if not env:
            raise ValueError(f"Environment {environment_id} not found")
        obj = env.get_interactive_object(object_id)
        if not obj:
            raise ValueError(f"Object {object_id} not found in environment {environment_id}")
        return obj.interact(user_state, input_value)

    
    def update_object_position(self, environment_id:str, object_id:str, position:tuple[int, int]):
        """
        Met à jour la position d'un objet interactif donné.
        Lève ValueError si l'environnement ou l'objet n'existe pas.
        """
        env = self.environment_repo.get_by_id(environment_id)
        if not env:
            # return
            raise ValueError(f"Environment {environment_id} not found")
        obj = env.get_interactive_object(object_id)
        if not obj:
            # return
            raise ValueError(f"Object {object_id} not found in environment {environment_id}")
        obj.position = position
        self.environment_repo.save(env)


    def rename_object(self, environment_id:str, object_id:str, new_name:str):
        """
        Renomme un objet interactif donné.
        Lève ValueError si l'environnement ou l'objet n'existe pas, ou si le nouveau nom est invalide.
        """
        env = self.environment_repo.get_by_id(environment_id)
        if not env:
            # return
            raise ValueError(f"Environment {environment_id} not found")
        obj = env.get_interactive_object(object_id)
        if not obj:
            # return
            raise ValueError(f"Object {object_id} not found in environment {environment_id}")
        obj.rename(new_name)
        self.environment_repo.save(env)


    def delete_object(self, environment_id:str, object_id:str):
        """
        Supprime un objet interactif donné de l'environnement.
        Lève ValueError si l'environnement ou l'objet n'existe pas.
        """
        env = self.environment_repo.get_by_id(environment_id)
        if not env:
            # return
            raise ValueError(f"Environment {environment_id} not found")
        env.remove_interactive_object(object_id)
        self.environment_repo.save(env)
    

    def update_object_position(self, environment_id:str, object_id:str, position:tuple[int, int]):
        """
        Met à jour la position d'un objet interactif donné.
        Lève ValueError si l'environnement ou l'objet n'existe pas.
        """
        env = self.environment_repo.get_by_id(environment_id)
        if not env:
            # return
            raise ValueError(f"Environment {environment_id} not found")
        obj = env.get_interactive_object(object_id)
        if not obj:
            # return
            raise ValueError(f"Object {object_id} not found in environment {environment_id}")
        obj.position = position
        self.environment_repo.save(env)

    # ==============================
    # GETTERS ET AUTRES
    # ==============================

    def get_objects_for_environment(self, environment_id:str) -> List[IInteractiveObject]:
        env = self.environment_repo.get_by_id(environment_id)
        return env.objects if env else []