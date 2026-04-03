# ====== INLINE/src/application/services/environment_service.py ======

from domain.repositories.i_environment_repository import IEnvironmentRepository
from domain.entities.environment import Environment
from factories.environment_factory import EnvironmentFactory
from shared.observer import Observable
from typing import Optional, List


class EnvironmentService(Observable):

    def __init__(self, environment_repository: IEnvironmentRepository, environment_factory: EnvironmentFactory):
        super().__init__()
        self._environment_repository = environment_repository
        self._environment_factory = environment_factory

    #----------------------

    def create_environment(self, owner_id: str, name: str) -> Environment:
        environment = self._environment_factory.create_environment(
            owner_id=owner_id,
            name=name
        )
        self._environment_repository.save(environment)
        self.notify("environment_created", environment)
        return environment

    #----------------------

    def get_environment(self, env_id: str) -> Optional[Environment]:
        return self._environment_repository.get_by_id(env_id)

    #----------------------

    def get_environments_for_owner(self, owner_id: str) -> List[Environment]:
        return self._environment_repository.get_by_owner(owner_id)

    #----------------------

    def list_all_environments(self) -> List[Environment]:
        return self._environment_repository.list_all()

    #----------------------

    def rename_environment(self, env_id: str, new_name: str) -> Environment:
        env = self._environment_repository.get_by_id(env_id)
        if not env:
            raise ValueError("Environnement introuvable.")
        env._name = new_name
        self._environment_repository.save(env)
        self.notify("environment_renamed", {"env_id": env_id, "new_name": new_name})
        return env

    #----------------------

    def delete_environment(self, env_id: str) -> None:
        env = self._environment_repository.get_by_id(env_id)
        if not env:
            raise ValueError("Environnement introuvable.")
        self._environment_repository.delete(env_id)
        self.notify("environment_deleted", env_id)