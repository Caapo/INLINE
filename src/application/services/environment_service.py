# ====== environment_service.py ======

# ===== Imports =====
from domain.repositories.i_environment_repository import IEnvironmentRepository
from domain.entities.environment import Environment
from factories.environment_factory import EnvironmentFactory
from typing import Optional, List
from uuid import uuid4

class EnvironmentService:
    def __init__(self, environment_repository:IEnvironmentRepository, environment_factory:EnvironmentFactory):
        self._environment_repository = environment_repository
        self._environment_factory = environment_factory

    def create_environment(self, owner_id:str, name:str) -> Environment:
        environment = self._environment_factory.create_environment(owner_id=owner_id, name=name)
        self._environment_repository.save(environment)
        return environment

    def get_environment(self, env_id:str) -> Optional[Environment]:
        return self._environment_repository.get_by_id(env_id)

    def get_environments_for_owner(self, owner_id:str) -> List[Environment]:
        return self._environment_repository.get_by_owner(owner_id)

    def list_all_environments(self) -> List[Environment]:
        return self._environment_repository.list_all()