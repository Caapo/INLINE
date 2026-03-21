# ======== clickable_object.py =========
from domain.entities.i_interactive_object import IInteractiveObject
from domain.enums.enums import ObjectCategory
from typing import List, Optional

class ClickableObject(IInteractiveObject):
    def __init__(self, id:str, environment_id:str, name:str, position:tuple[int,int], category:ObjectCategory, suggested_intentions:Optional[List[str]]=None, metadata:Optional[dict]=None):
        self.id = id
        self.environment_id = environment_id
        self.name = name
        self.position = position
        self.category = category
        self.suggested_intentions = suggested_intentions or []
        self.metadata = metadata or {}

    # --------------
    def interact(self, user_state, input_value: Optional[str] = None):
        if input_value:
            return {"custom_intention": input_value, "object_id": self.id}
        else:
            return {"suggestions": self.suggested_intentions, "object_id": self.id}

    # --------------

    def add_suggestion(self, intention: str):
        self.suggested_intentions.append(intention)

    def remove_suggestion(self, intention: str):
        if intention in self.suggested_intentions:
            self.suggested_intentions.remove(intention)

    # --------------

    

    # --------------
    
    def get_metadata(self) -> dict:
        return self.metadata

    def get_position(self) -> tuple[int,int]:
        return self.position

    def get_info(self) -> dict:
        return {
            "id": self.id,
            "environment_id": self.environment_id,
            "name": self.name,
            "position": self.position,
            "category": self.category.name,
            "suggested_intentions": self.suggested_intentions,
            "metadata": self.metadata
        }