# ==================================== INLINE/src/application/services/intention_service.py ====================================

# ============ Imports ============ 
from domain.entities.intention import Intention
from domain.repositories.i_intention_repository import IIntentionRepository
from factories.intention_factory import IntentionFactory
from shared.observer import Observable
from typing import Optional


class IntentionService(Observable):

    def __init__(self, intention_repository: IIntentionRepository, intention_factory: IntentionFactory):
        super().__init__()
        self._intention_repository = intention_repository
        self._intention_factory = intention_factory

    #----------------------

    def create_intention(self, user_id: str, title: str, category: str) -> Intention:
        intention = self._intention_factory.create_intention(
            user_id=user_id,
            title=title,
            category=category
        )
        self._intention_repository.save(intention)
        self.notify("intention_created", intention)
        return intention

    #----------------------

    def _get_intention_or_raise(self, intention_id: str) -> Intention:
        intention = self._intention_repository.get_by_id(intention_id)
        if not intention:
            raise ValueError("Intention non trouvée.")
        return intention

    #----------------------

    def get_active_intention_by_user(self, user_id: str) -> Optional[Intention]:
        return self._intention_repository.get_active(user_id)

    #----------------------

    def rename_intention(self, intention_id: str, new_title: str) -> Intention:
        intention = self._get_intention_or_raise(intention_id)
        intention.rename(new_title)
        self._intention_repository.save(intention)
        self.notify("intention_updated", intention)
        return self._intention_repository.get_by_id(intention_id)

    #----------------------

    def activate_intention(self, intention_id: str) -> Intention:
        intention = self._get_intention_or_raise(intention_id)
        active = self._intention_repository.get_active(intention._user_id)
        if active and active._id != intention_id:
            active.deactivate()
            self._intention_repository.save(active)
        intention.activate()
        self._intention_repository.save(intention)
        self.notify("intention_updated", intention)
        return self._intention_repository.get_by_id(intention_id)

    #----------------------

    def deactivate_intention(self, intention_id: str) -> Intention:
        intention = self._get_intention_or_raise(intention_id)
        intention.deactivate()
        self._intention_repository.save(intention)
        self.notify("intention_updated", intention)
        return self._intention_repository.get_by_id(intention_id)

    #----------------------

    def get_all_intentions(self) -> list[Intention]:
        return self._intention_repository.get_all()

    #----------------------

    def get_intentions_map(self) -> dict:
        intentions = self._intention_repository.get_all()
        return {i.id: i for i in intentions}