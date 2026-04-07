# ===== INLINE/src/application/services/note_service.py =====
# Service applicatif de gestion des notes et de leurs blocs.
# Orchestre toutes les opérations sur les notes et notifie l'UI via Observer.

from typing import List, Optional

from domain.entities.note import Note
from domain.entities.i_note_block import INoteBlock
from domain.repositories.i_note_repository import INoteRepository
from factories.note_factory import NoteFactory
from factories.note_block_factory import NoteBlockFactory
from shared.observer import Observable
from domain.repositories.i_intention_repository import IIntentionRepository


class NoteService(Observable):
    """
    Service applicatif de gestion des notes et de leurs blocs.
    Orchestre toutes les opérations sur les notes et notifie l'UI via Observer.

    Attributs:
        - _note_repository : INoteRepository - Interface de persistance des notes.
        - _note_factory : NoteFactory - Factory pour créer des instances de Note.
        - _intention_repository : IIntentionRepository - Repository pour gérer les intentions liées aux notes.
    """

    # ==============================
    # CONSTRUCTEUR
    # ==============================

    def __init__(self, note_repository:INoteRepository, note_factory:NoteFactory, intention_repository:IIntentionRepository):
        super().__init__()
        self._note_repository = note_repository
        self._note_factory = note_factory
        self._intention_repository = intention_repository


    # ==============================
    # MÉTHODES CAS D'USAGE
    # ==============================

    def create_note(self, owner_id:str, title:str) -> Note:
        note = self._note_factory.create_note(owner_id=owner_id, title=title)
        self._note_repository.save(note)
        self.notify("note_created", note)
        return note
    

    def attach_to_intention(self, note_id:str, intention_id:str) -> Note:
        note      = self._get_or_raise(note_id)
        intention = self._intention_repository.get_by_id(intention_id)
        if not intention:
            raise ValueError(f"Intention introuvable : {intention_id}")
        note.attach_to_intention(intention_id)
        self._note_repository.save(note)
        self.notify("note_updated", note)
        return note


    def detach_from_intention(self, note_id:str) -> Note:
        note = self._get_or_raise(note_id)
        note.detach_from_intention()
        self._note_repository.save(note)
        self.notify("note_updated", note)
        return note

    

    def rename_note(self, note_id:str, new_title:str) -> Note:
        note = self._get_or_raise(note_id)
        note.rename(new_title)
        self._note_repository.save(note)
        self.notify("note_updated", note)
        return note



    def delete_note(self, note_id:str) -> None:
        note = self._get_or_raise(note_id)
        self._note_repository.delete(note_id)
        self.notify("note_deleted", note_id)

    

    def add_block(self, note_id:str, block_type:str, **kwargs) -> Note:
        note  = self._get_or_raise(note_id)
        block = NoteBlockFactory.create(block_type, **kwargs)
        note.add_block(block)
        self._note_repository.save(note)
        self.notify("note_updated", note)
        return note



    def update_block(self, note_id:str, block_id:str, data:dict) -> Note:
        note = self._get_or_raise(note_id)
        note.update_block(block_id, data)
        self._note_repository.save(note)
        self.notify("note_updated", note)
        return note

    

    def remove_block(self, note_id:str, block_id:str) -> Note:
        note = self._get_or_raise(note_id)
        note.remove_block(block_id)
        self._note_repository.save(note)
        self.notify("note_updated", note)
        return note

    

    def reorder_blocks(self, note_id:str, from_index:int, to_index:int) -> Note:
        note = self._get_or_raise(note_id)
        note.reorder_blocks(from_index, to_index)
        self._note_repository.save(note)
        self.notify("note_updated", note)
        return note


    # ==============================
    # GETTERS ET AUTRES
    # ==============================

    def _get_or_raise(self, note_id:str) -> Note:
        note = self._note_repository.get_by_id(note_id)
        if not note:
            raise ValueError(f"Note introuvable : {note_id}")
        return note


    
    def get_note(self, note_id:str) -> Optional[Note]:
        return self._note_repository.get_by_id(note_id)



    def get_notes_for_user(self, owner_id:str) -> List[Note]:
        return self._note_repository.get_by_owner(owner_id)



    def get_notes_for_intention(self, intention_id:str) -> list:
        return self._note_repository.get_by_intention(intention_id)