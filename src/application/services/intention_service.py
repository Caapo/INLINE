# ============ Imports ============ 
from domain.entities.intention import Intention
from domain.repositories.i_intention_repository import IIntentionRepository
from factories.intention_factory import IntentionFactory


# ============ Notes ============  
# Cette classe permet d'assurer la gestion des intentions, tels que la création, la mise à jour, l'activation et la désactivation.
# Elle interagit avec la base de données (SQLiteIntentionRepository)  pour stocker et récupérer les données des intentions.


class IntentionService:
    def __init__(self, intention_repository:IIntentionRepository, intention_factory:IntentionFactory):
        self._intention_repository = intention_repository
        self._intention_factory = intention_factory

    #----------------------

    def create_intention(self, user_id:str, title:str, category:str) -> Intention:
        intention = self._intention_factory.create_intention(user_id=user_id, title=title, category=category)
        self._intention_repository.save(intention)
        return intention

    #----------------------

    def _get_intention_or_raise(self, intention_id:str) -> Intention:
        intention = self._intention_repository.get_by_id(intention_id)
        if not intention:
            raise ValueError("Intention non trouvée.")
        return intention

    #----------------------

    def rename_intention(self, intention_id:str, new_title:str) -> Intention:
        intention = self._get_intention_or_raise(intention_id)
        intention.rename(new_title)
        self._intention_repository.save(intention)
        return intention

    #----------------------

    def activate_intention(self, intention_id:str) -> Intention:
        intention = self._get_intention_or_raise(intention_id)
        intention.activate()
        self._intention_repository.save(intention)
        return intention
        
    #----------------------

    def deactivate_intention(self, intention_id:str) -> Intention:
        intention = self._get_intention_or_raise(intention_id)
        intention.deactivate()
        self._intention_repository.save(intention)
        return intention
