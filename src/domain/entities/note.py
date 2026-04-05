# ======= INLINE/src/domain/entities/note.py =====

from datetime import datetime
from typing import Optional, List
import json
from domain.entities.i_note_block import INoteBlock


class Note:
    def __init__(self, id:str, owner_id:str, title:str, blocks: Optional[List[INoteBlock]] = None, intention_id: Optional[str] = None, created_at: Optional[datetime] = None,
    updated_at: Optional[datetime] = None, metadata: Optional[dict] = None):
        self._id = id
        self._owner_id = owner_id
        self._title = title
        self._blocks = blocks or []
        self._intention_id = intention_id
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
        self._metadata = metadata or {}

    # -------------- Persistance --------------
    def to_persistence(self) -> dict:
        return {
            "id": self._id,
            "owner_id": self._owner_id,
            "title": self._title,
            "blocks": json.dumps([b.to_dict() for b in self._blocks]),
            "intention_id": self._intention_id,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "metadata": json.dumps(self._metadata)
        }

    #------------------------

    @classmethod
    def from_persistence(cls, id: str, owner_id: str, title: str, blocks_json: str, created_at: str, updated_at: str, metadata_json: str, intention_id: str = None) -> "Note":
        from factories.note_block_factory import NoteBlockFactory
        raw_blocks = json.loads(blocks_json) if blocks_json else []
        blocks = [NoteBlockFactory.from_dict(b) for b in raw_blocks]

        note = cls.__new__(cls)
        note._id = id
        note._owner_id = owner_id
        note._title = title
        note._blocks = blocks
        note._intention_id = intention_id
        note._created_at = datetime.fromisoformat(created_at)
        note._updated_at = datetime.fromisoformat(updated_at)
        note._metadata = json.loads(metadata_json) if metadata_json else {}
        return note

    # --------------- Métier --------------
    def rename(self, new_title: str) -> None:
        if not new_title:
            raise ValueError("Le titre ne peut pas être vide.")
        self._title = new_title
        self._touch()

    #------------------------

    def add_block(self, block: INoteBlock) -> None:
        self._blocks.append(block)
        self._touch()

    #------------------------

    def remove_block(self, block_id: str) -> None:
        self._blocks = [b for b in self._blocks if b.get_id() != block_id]
        self._touch()

    #------------------------

    def reorder_blocks(self, from_index: int, to_index: int) -> None:
        if 0 <= from_index < len(self._blocks) and 0 <= to_index < len(self._blocks):
            block = self._blocks.pop(from_index)
            self._blocks.insert(to_index, block)
            self._touch()

    #------------------------

    def get_block(self, block_id: str) -> Optional[INoteBlock]:
        for b in self._blocks:
            if b.get_id() == block_id:
                return b
        return None

    #------------------------

    def update_block(self, block_id: str, data: dict) -> None:
        block = self.get_block(block_id)
        if block:
            block.update_data(data)
            self._touch()

    #------------------------

    def _touch(self) -> None:
        self._updated_at = datetime.utcnow()

    #------------------------

    def attach_to_intention(self, intention_id: str) -> None:
        self._intention_id = intention_id
        self._touch()

    #------------------------

    def detach_from_intention(self) -> None:
        self._intention_id = None
        self._touch()


    # ---------- Propriétés ----------
    @property
    def id(self) -> str: return self._id

    @property
    def owner_id(self) -> str: return self._owner_id

    @property
    def title(self) -> str: return self._title

    @property
    def blocks(self) -> List[INoteBlock]: return self._blocks

    @property
    def intention_id(self) -> Optional[str]:
        return self._intention_id

    @property
    def created_at(self) -> datetime: return self._created_at

    @property
    def updated_at(self) -> datetime: return self._updated_at

    @property
    def metadata(self) -> dict: return self._metadata

    #------------------------

    def get_info(self) -> dict:
        return {
            "id": self._id,
            "owner_id": self._owner_id,
            "title": self._title,
            "blocks": [b.to_dict() for b in self._blocks],
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "metadata": self._metadata
        }

    def __repr__(self):
        return f"Note(id={self._id}, title={self._title}, blocks={len(self._blocks)})"