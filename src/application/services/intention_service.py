# ============ INLINE/src/application/services/intention_service.py ============
# Service applicatif des intentions.
# Orchestre les cas d'usage liés aux intentions et notifie
# les abonnés via le patron Observer.

from typing import Optional

from domain.entities.intention import Intention
from domain.repositories.i_intention_repository import IIntentionRepository
from factories.intention_factory import IntentionFactory
from shared.observer import Observable



class IntentionService(Observable):
    """
    Service applicatif responsable de la gestion des intentions.

    Orchestre les opérations métier sur les intentions :
    création, renommage, activation/désactivation, suppression.
    Notifie les composants abonnés (UI) via le patron Observer
    à chaque modification d'état.

    Attributs:
        _intention_repository (IIntentionRepository): Interface de persistance.
        _intention_factory (IntentionFactory): Factory pour créer des intentions.
    """

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================

    def __init__(self, intention_repository: IIntentionRepository, intention_factory: IntentionFactory):
        super().__init__()
        self._intention_repository = intention_repository
        self._intention_factory = intention_factory


    # =================================================
    # CAS D'USAGE
    # =================================================

    def create_intention(self, user_id: str, title: str, category: str) -> Intention:
        """
        Crée une nouvelle intention et la persiste.
        Notifie les abonnés avec l'événement "intention_created".
        """
        intention = self._intention_factory.create_intention(
            user_id=user_id,
            title=title,
            category=category
        )
        self._intention_repository.save(intention)
        self.notify("intention_created", intention)
        return intention


    def rename_intention(self, intention_id: str, new_title: str) -> Intention:
        """
        Renomme une intention existante et persiste le changement.
        Notifie les abonnés avec l'événement "intention_updated".
        """
        intention = self._get_intention_or_raise(intention_id)
        intention.rename(new_title)
        self._intention_repository.save(intention)
        self.notify("intention_updated", intention)
        return self._intention_repository.get_by_id(intention_id)


    def activate_intention(self, intention_id: str) -> Intention:
        """
        Active une intention comme focus courant.
        Désactive automatiquement le focus précédent si existant.
        Notifie les abonnés avec l'événement "intention_updated".
        """
        intention = self._get_intention_or_raise(intention_id)
        active = self._intention_repository.get_active(intention._user_id)
        if active and active._id != intention_id:
            active.deactivate()
            self._intention_repository.save(active)
        intention.activate()
        self._intention_repository.save(intention)
        self.notify("intention_updated", intention)
        return self._intention_repository.get_by_id(intention_id)


    def deactivate_intention(self, intention_id: str) -> Intention:
        """
        Désactive une intention — retire le statut de focus.
        Notifie les abonnés avec l'événement "intention_updated".
        """
        intention = self._get_intention_or_raise(intention_id)
        intention.deactivate()
        self._intention_repository.save(intention)
        self.notify("intention_updated", intention)
        return self._intention_repository.get_by_id(intention_id)


    def delete_intention(self, intention_id: str) -> None:
        """
        Supprime définitivement une intention.
        Notifie les abonnés avec l'événement "intention_deleted".
        """
        intention = self._get_intention_or_raise(intention_id)
        self._intention_repository.delete(intention_id)
        self.notify("intention_deleted", intention_id)
        

    # ==================================================
    # GETTERS & AUTRES
    # ==================================================

    def _get_intention_or_raise(self, intention_id: str) -> Intention:
        """
        Récupère une intention ou lève ValueError si introuvable.
        """
        intention = self._intention_repository.get_by_id(intention_id)
        if not intention:
            raise ValueError("Intention non trouvée.")
        return intention


    def get_active_intention_by_user(self, user_id: str) -> Optional[Intention]:
        return self._intention_repository.get_active(user_id)


    def get_all_intentions(self) -> list[Intention]:
        return self._intention_repository.get_all()

    
    def get_intentions_map(self) -> dict:
        intentions = self._intention_repository.get_all()
        return {i.id: i for i in intentions}


