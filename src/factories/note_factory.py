# ======= INLINE/src/factories/note_factory.py =====

from uuid import uuid4
from datetime import datetime
from domain.entities.note import Note


class NoteFactory:

    def create_note(self, owner_id:str, title:str) -> Note:
        return Note(
            id=str(uuid4()),
            owner_id=owner_id,
            title=title,
            blocks=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            metadata={}
        )