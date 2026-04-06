# ================ INLINE/src/factories/intention_factory.py ===============
# Factory de création des intentions.
# Centralise la logique de construction pour garantir
# la cohérence des objets créés (id, date, valeurs par défaut).


from datetime import datetime
from uuid import uuid4

from domain.entities.intention import Intention



class IntentionFactory:
    """
    Factory responsable de la création des instances d'Intention.
    Patron de conception : Factory.
    Centralise la logique de construction afin d'éviter
    la duplication et de garantir que chaque intention
    créée possède un identifiant unique et une date de création.
    """

    def create_intention(self, user_id:str, title:str, category:str) -> Intention:
        """
        Crée une nouvelle intention avec un UUID généré automatiquement.
        Args:
            user_id (str): Identifiant de l'utilisateur propriétaire.
            title (str): Titre déclaratif de l'intention.
            category (str): Catégorie de l'intention.
        Returns:
            Intention: Instance prête à être persistée.
        """
        return Intention(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            category=category,
            created_at=datetime.utcnow(),
            metadata={} 
        )