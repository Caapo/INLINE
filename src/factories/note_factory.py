# ======= INLINE/src/factories/note_factory.py =====
# Factory pour créer des instances de notes à partir de données brutes.
# Permet d'abstraire la logique de création et de conversion des notes.


from uuid import uuid4
from datetime import datetime

from domain.entities.note import Note


class NoteFactory:
    """
    Factory de création des notes.
    Garantit qu'une note créée possède un UUID unique,
    une date de création et aucun bloc initial.
    """
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