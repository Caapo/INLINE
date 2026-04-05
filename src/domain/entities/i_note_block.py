# =============== INLINE/src/domain/entities/i_note_block.py ===============

from abc import ABC, abstractmethod

class INoteBlock(ABC):

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