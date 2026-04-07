# =============== INLINE/src/domain/entities/i_note_block.py ===============
# Interface définissant le comportement d'un bloc de notes.
# Permet d'abstraire les différentes implémentations possibles de blocs de notes (ex

from abc import ABC, abstractmethod

class INoteBlock(ABC):
    """
    Interface abstraite définissant le contrat minimal d'un bloc de note.
    Chaque bloc est une unité de contenu indépendante et configurable.
    La composition de blocs permet de construire des notes flexibles
    sans modifier la classe Note.
    """

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def update_data(self, data: dict) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass