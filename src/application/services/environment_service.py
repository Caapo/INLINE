# ====== INLINE/src/application/services/environment_service.py ======
# Service pour gérer les environnements : création, récupération, mise à jour, suppression.
# Utilise le repository pour la persistance et la factory pour la création d'instances.
# Hérite de Observable pour notifier les changements d'environnement aux autres composants.


from typing import Optional, List

from domain.repositories.i_environment_repository import IEnvironmentRepository
from domain.entities.environment import Environment
from factories.environment_factory import EnvironmentFactory
from shared.observer import Observable



class EnvironmentService(Observable):
    """
    Service de gestion des environnements. Permet de créer, récupérer, renommer et supprimer des environnements.
    Utilise un repository pour la persistance et une factory pour la création d'instances.
    Hérite de Observable pour notifier les autres composants des changements d'environnement.

    Attributs :
        - _environment_repository : IEnvironmentRepository - Repository pour la gestion des environnements.
        - _environment_factory : EnvironmentFactory - Factory pour créer des instances d'environnement.
    """

    # ==============================
    # CONSTRUCTEUR
    # ==============================

    def __init__(self, environment_repository: IEnvironmentRepository, environment_factory: EnvironmentFactory):
        super().__init__()
        self._environment_repository = environment_repository
        self._environment_factory = environment_factory

    # ==============================
    # MÉTHODES CAS D'USAGE
    # ==============================

    def create_environment(self, owner_id: str, name: str) -> Environment:
        """
        Crée un nouvel environnement pour un propriétaire donné et le sauvegarde via le repository.
        Notifie les observateurs de la création d'un nouvel environnement.
        """
        environment = self._environment_factory.create_environment(
            owner_id=owner_id,
            name=name
        )
        self._environment_repository.save(environment)
        self.notify("environment_created", environment)
        return environment



    def rename_environment(self, env_id: str, new_name: str) -> Environment:
        """
        Renomme un environnement existant et le sauvegarde via le repository.
        Notifie les observateurs du changement de nom de l'environnement.
        Lève ValueError si l'environnement n'existe pas.
        """
        env = self._environment_repository.get_by_id(env_id)
        if not env:
            raise ValueError("Environnement introuvable.")
        env._name = new_name
        self._environment_repository.save(env)
        self.notify("environment_renamed", {"env_id": env_id, "new_name": new_name})
        return env

    

    def delete_environment(self, env_id: str) -> None:
        """
        Supprime un environnement existant via le repository.
        Notifie les observateurs de la suppression de l'environnement.
        Lève ValueError si l'environnement n'existe pas.
        """
        env = self._environment_repository.get_by_id(env_id)
        if not env:
            raise ValueError("Environnement introuvable.")
        self._environment_repository.delete(env_id)
        self.notify("environment_deleted", env_id)
    

    # ==============================
    # GETTERS ET AUTRES
    # ==============================


    def get_environment(self, env_id: str) -> Optional[Environment]:
        """
        Récupère un environnement par son ID via le repository.
        """
        return self._environment_repository.get_by_id(env_id)

    

    def get_environments_for_owner(self, owner_id: str) -> List[Environment]:
        """
        Récupère tous les environnements d'un propriétaire donné via le repository.
        """
        return self._environment_repository.get_by_owner(owner_id)

    

    def list_all_environments(self) -> List[Environment]:
        """
        Récupère tous les environnements existants via le repository.
        """
        return self._environment_repository.list_all()

    
