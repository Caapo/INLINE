# ======== INLINE/src/domain/entities/i_interactive_object.py =========
# Interface définissant le comportement minimal d'un objet interactif.
# Tout objet placé dans un environnement doit implémenter ce contrat.


from abc import ABC, abstractmethod
from typing import Any, Optional

class IInteractiveObject(ABC):
    """
    Interface définissant le comportement minimal d'un objet interactif.
    Tout objet placé dans un environnement doit implémenter ce contrat.
    """

    @abstractmethod
    def interact(self, user_state, input_value:Optional[str]=None) -> Any:
        """
        Définit l'interaction de l'objet avec l'utilisateur.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> dict:
        """
        Récupère les métadonnées de l'objet interactif.
        """
        pass

    @abstractmethod
    def get_position(self) -> tuple[int, int]:
        """
        Récupère la position de l'objet interactif dans l'environnement.
        """
        pass

    @abstractmethod
    def get_info(self) -> dict:
        """
        Récupère les informations de l'objet interactif sous forme de dictionnaire.
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Récupère le type de l'objet interactif.
        """
        pass