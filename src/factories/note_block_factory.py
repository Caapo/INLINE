# ========= INLINE/src/factories/note_block_factory.py ========
# Factory pour créer des instances de blocs de notes à partir de données brutes.
# Permet d'abstraire la logique de création et de conversion des blocs de notes.

from uuid import uuid4
from domain.entities.note_blocks import TitleBlock, TextBlock, ChecklistBlock, TableBlock
from domain.enums.enums import BlockType


class NoteBlockFactory:
    """
    Factory pour créer des instances de blocs de notes à partir de données brutes.
    Permet d'abstraire la logique de création et de conversion des blocs de notes.
    """
    @staticmethod
    def create(block_type:str, **kwargs):
        """
        Crée un bloc de note selon son type.
        Lève ValueError si le type est inconnu.
        kwargs est un dictionnaire de données spécifiques à chaque type de bloc :
        - TitleBlock : text (str), level (int)
        - TextBlock : content (str)
        - ChecklistBlock : items (list[str])
        - TableBlock : headers (list[str]), rows (list[list[str]])
        """
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
        """
        Reconstruit un bloc de note depuis un dictionnaire.
        Utilisé par Note.from_persistence() pour restaurer les blocs stockés en JSON dans la base.
        """
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