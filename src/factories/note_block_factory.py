# ========= INLINE/src/factories/note_block_factory.py ========

from uuid import uuid4
from domain.entities.note_blocks import TitleBlock, TextBlock, ChecklistBlock, TableBlock
from domain.enums.enums import BlockType


class NoteBlockFactory:

    @staticmethod
    def create(block_type:str, **kwargs):
        bid = str(uuid4())
        if block_type == BlockType.TITLE.value:
            return TitleBlock(id=bid, text=kwargs.get("text", ""), level=kwargs.get("level", 1))
        if block_type == BlockType.TEXT.value:
            return TextBlock(id=bid, content=kwargs.get("content", ""))
        if block_type == BlockType.CHECKLIST.value:
            return ChecklistBlock(id=bid, items=kwargs.get("items", []))
        if block_type == BlockType.TABLE.value:
            return TableBlock(id=bid, headers=kwargs.get("headers", []), rows=kwargs.get("rows", []))
        raise ValueError(f"Type de bloc inconnu : {block_type}")

    #------------------------

    @staticmethod
    def from_dict(data:dict):
        block_type = data.get("type")
        block_data = data.get("data", {})
        bid = data.get("id", str(uuid4()))

        if block_type == BlockType.TITLE.value:
            return TitleBlock(id=bid, **block_data)
        if block_type == BlockType.TEXT.value:
            return TextBlock(id=bid, **block_data)
        if block_type == BlockType.CHECKLIST.value:
            return ChecklistBlock(id=bid, **block_data)
        if block_type == BlockType.TABLE.value:
            return TableBlock(id=bid, **block_data)
        raise ValueError(f"Type de bloc inconnu : {block_type}")