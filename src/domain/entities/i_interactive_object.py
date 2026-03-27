# ======== INLINE/src/domain/entities/i_interactive_object.py =========

from abc import ABC, abstractmethod
from typing import Any, Optional

class IInteractiveObject(ABC):

    @abstractmethod
    def interact(self, user_state, input_value:Optional[str]=None) -> Any:
        pass

    @abstractmethod
    def get_metadata(self) -> dict:
        pass

    @abstractmethod
    def get_position(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_info(self) -> dict:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass