# ============ Imports ============ 
from datetime import datetime
from uuid import uuid4

from domain.entities.intention import Intention
from domain.repositories.i_intention_repository import IIntentionRepository


# ============ Notes ============  
# Cette classe permet d'assurer la gestion des intentions, tels que la création, la mise à jour, l'activation et la désactivation.
# Elle interagit avec la base de données (SQLiteIntentionRepository)  pour stocker et récupérer les données des intentions.



# ============ Class ============  

class IntentionService:
    def __init__(self, intention_repository:IIntentionRepository):

        self._intention_repository = intention_repository

    #----------------------

    def create_intention(self, user_id:str, title:str, category:str) -> Intention:

        intention = Intention(
            intention_id = str(uuid4())
            user_id = user_id,
            title = title,
            category = category
            created_at = datetime.utcnow()
        )

        self._intention_repository.save(intention)

        return intention

    #----------------------

    def rename_intention(self, intention_id:str, new_title:str):

        intention = self._intention_repository.get_by_id(intention_id)

        if not intention:
            raise ValueError("Intention non trouvée.")

        intention.rename(new_title)
        self._intention_repository.save(intention)

        return intention

    #----------------------

    def activate_intention(self, intention_id:str):
        intention = self._intention_repository.get_by_id(intentention_id)

        if not intention: 
            raise ValueError("Intention non trouvée.")
        
        intention.activate()

        self._intention_repository.save(intention)
        return intention
        
    #----------------------

    def deactivate_intention(self, intention_id:str):
        intention = self._intention_repository.get_by_id(intentention_id)

        if not intention: 
            raise ValueError("Intention non trouvée.")
        
        intention.deactivate()

        self._intention_repository.save(intention)
        return intention
