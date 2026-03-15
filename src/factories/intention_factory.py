from datetime import datetime
from uuid import uuid4

from domain.entities.intention import Intention

# ============ Notes ============  
# Cette classe permet de créer des instances d'intentions, en encapsulant la logique de création.

class IntentionFactory:

    def create_intention(self, user_id:str, title:str, category:str) -> Intention:

        return Intention(
            intention_id=str(uuid4()),
            user_id=user_id,
            title=title,
            category=category,
            created_at=datetime.utcnow(),
            is_active=False
        )