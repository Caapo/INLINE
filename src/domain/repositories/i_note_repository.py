# ====== INLINE/src/domain/repositories/i_note_repository.py =====

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.note import Note


class INoteRepository(ABC):

    @abstractmethod
    def save(self, note:Note) -> None:
        pass

    @abstractmethod
    def get_by_id(self, note_id:str) -> Optional[Note]:
        pass

    @abstractmethod
    def get_by_owner(self, owner_id:str) -> List[Note]:
        pass

    @abstractmethod
    def get_by_intention(self, intention_id: str) -> List[Note]:
        pass

    @abstractmethod
    def delete(self, note_id:str) -> None:
        pass