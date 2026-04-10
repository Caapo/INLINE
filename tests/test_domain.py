# ==== INLINE/tests/test_domain.py ====
# Tests unitaires des entités du domaine.
# Vérifient la logique métier indépendamment des infrastructures. (Ni UI, ni DB)

import pytest
from datetime import datetime
from domain.entities.intention import Intention
from domain.entities.event import Event
from domain.entities.note import Note
from domain.entities.note_blocks import (TextBlock, TitleBlock, ChecklistBlock, TableBlock)
from domain.entities.pomodoro_module import PomodoroModule
from domain.entities.pomodoro_session import PomodoroSession
from domain.enums.enums import EventStatus
from domain.enums.module_enums import SessionStatus


# ======================================================
# INTENTION
# ======================================================

class TestIntention:
    """Tests unitaires de l'entité Intention."""

    def setup_method(self):
        """Crée une intention réutilisable avant chaque test."""
        self.intention = Intention(
            id="i1", user_id="u1",
            title="Faire du sport", category="Physique"
        )

    def test_intention_inactive_par_defaut(self):
        """Une intention doit être inactive à sa création."""
        assert self.intention.is_active is False

    def test_activation(self):
        """L'activation doit passer is_active à True."""
        self.intention.activate()
        assert self.intention.is_active is True

    def test_desactivation(self):
        """La désactivation doit passer is_active à False."""
        self.intention.activate()
        self.intention.deactivate()
        assert self.intention.is_active is False

    def test_renommage_valide(self):
        """Le renommage doit mettre à jour le titre."""
        self.intention.rename("Méditation")
        assert self.intention.title == "Méditation"

    def test_renommage_vide_leve_erreur(self):
        """Un titre vide doit lever ValueError."""
        with pytest.raises(ValueError):
            self.intention.rename("")

    def test_to_persistence_contient_champs_requis(self):
        """to_persistence doit retourner tous les champs nécessaires."""
        data = self.intention.to_persistence()
        assert "id" in data
        assert "user_id" in data
        assert "title" in data
        assert "is_active" in data
        assert "created_at" in data

    def test_from_persistence_restaure_etat(self):
        """from_persistence doit restaurer exactement l'état persisté."""
        intention = Intention.from_persistence(
            id="i2", user_id="u1",
            title="Lire", category="Mental",
            object_id=None, is_active=True,
            created_at=datetime(2026, 1, 1, 10, 0)
        )
        assert intention.is_active is True
        assert intention.title == "Lire"


# ======================================================
# EVENT
# ======================================================

class TestEvent:
    """Tests unitaires de l'entité Event."""

    def setup_method(self):
        """Crée un event planifié réutilisable avant chaque test."""
        self.event = Event(
            id="e1", intention_id="i1", environment_id="env1",
            start_time=datetime(2026, 4, 10, 9, 0),
            duration=30
        )

    def test_statut_planned_par_defaut(self):
        """Un event doit être PLANNED à sa création."""
        assert self.event.status == EventStatus.PLANNED.value

    def test_end_time_calcule_correctement(self):
        """end_time doit être start_time + duration minutes."""
        assert self.event.end_time == datetime(2026, 4, 10, 9, 30)

    def test_complete(self):
        """La complétion doit passer le statut à COMPLETED."""
        self.event.complete()
        assert self.event.status == EventStatus.COMPLETED.value

    def test_cancel(self):
        """L'annulation doit passer le statut à CANCELLED."""
        self.event.cancel()
        assert self.event.status == EventStatus.CANCELLED.value

    def test_complete_event_annule_leve_erreur(self):
        """Compléter un event annulé doit lever ValueError."""
        self.event.cancel()
        with pytest.raises(ValueError):
            self.event.complete()

    def test_cancel_event_complete_leve_erreur(self):
        """Annuler un event complété doit lever ValueError."""
        self.event.complete()
        with pytest.raises(ValueError):
            self.event.cancel()

    def test_update_time_valide(self):
        """update_time doit mettre à jour start_time et recalculer end_time."""
        new_start = datetime(2026, 4, 10, 14, 0)
        self.event.update_time(new_start, 60)
        assert self.event.start_time == new_start
        assert self.event.end_time == datetime(2026, 4, 10, 15, 0)
        assert self.event.duration == 60

    def test_update_time_duree_invalide_leve_erreur(self):
        """Une durée <= 0 doit lever ValueError."""
        with pytest.raises(ValueError):
            self.event.update_time(datetime(2026, 4, 10, 14, 0), 0)

    def test_update_time_event_non_planifie_leve_erreur(self):
        """Modifier un event complété doit lever ValueError."""
        self.event.complete()
        with pytest.raises(ValueError):
            self.event.update_time(datetime(2026, 4, 10, 14, 0), 30)


# ======================================================
# NOTE
# ======================================================

class TestNote:
    """Tests unitaires de l'entité Note."""

    def setup_method(self):
        """Crée une note vide réutilisable avant chaque test."""
        self.note = Note(id="n1", owner_id="u1", title="Ma note")

    def test_note_vide_par_defaut(self):
        """Une note doit être créée sans blocs."""
        assert len(self.note.blocks) == 0

    def test_ajout_bloc(self):
        """L'ajout d'un bloc doit augmenter le nombre de blocs."""
        block = TextBlock(id="b1", content="Contenu")
        self.note.add_block(block)
        assert len(self.note.blocks) == 1

    def test_suppression_bloc(self):
        """La suppression d'un bloc doit le retirer de la liste."""
        block = TextBlock(id="b1", content="Contenu")
        self.note.add_block(block)
        self.note.remove_block("b1")
        assert len(self.note.blocks) == 0

    def test_get_bloc_existant(self):
        """get_block doit retourner le bloc correspondant à l'id."""
        block = TextBlock(id="b1", content="Contenu")
        self.note.add_block(block)
        assert self.note.get_block("b1") is block

    def test_get_bloc_inexistant_retourne_none(self):
        """get_block doit retourner None si le bloc est absent."""
        assert self.note.get_block("inexistant") is None

    def test_reorder_blocs(self):
        """reorder_blocks doit déplacer un bloc à la bonne position."""
        b1 = TextBlock(id="b1", content="Premier")
        b2 = TextBlock(id="b2", content="Deuxième")
        self.note.add_block(b1)
        self.note.add_block(b2)
        self.note.reorder_blocks(0, 1)
        assert self.note.blocks[0].get_id() == "b2"
        assert self.note.blocks[1].get_id() == "b1"

    def test_renommage_valide(self):
        """Le renommage doit mettre à jour le titre."""
        self.note.rename("Nouveau titre")
        assert self.note.title == "Nouveau titre"

    def test_renommage_vide_leve_erreur(self):
        """Un titre vide doit lever ValueError."""
        with pytest.raises(ValueError):
            self.note.rename("")

    def test_lien_intention(self):
        """attach_to_intention doit mettre à jour intention_id."""
        self.note.attach_to_intention("i1")
        assert self.note.intention_id == "i1"

    def test_delier_intention(self):
        """detach_from_intention doit remettre intention_id à None."""
        self.note.attach_to_intention("i1")
        self.note.detach_from_intention()
        assert self.note.intention_id is None


# ======================================================
# BLOCS DE NOTE
# ======================================================

class TestNoteBlocks:
    """Tests unitaires des blocs de note."""

    def test_text_block_get_data(self):
        """TextBlock doit retourner son contenu via get_data."""
        block = TextBlock(id="b1", content="Hello")
        assert block.get_data() == {"content": "Hello"}

    def test_text_block_update_data(self):
        """update_data doit mettre à jour le contenu."""
        block = TextBlock(id="b1", content="Ancien")
        block.update_data({"content": "Nouveau"})
        assert block.get_data()["content"] == "Nouveau"

    def test_title_block_niveau_par_defaut(self):
        """TitleBlock doit avoir le niveau 1 par défaut."""
        block = TitleBlock(id="b1", text="Titre")
        assert block.get_data()["level"] == 1

    def test_checklist_add_item(self):
        """add_item doit ajouter un item non coché."""
        block = ChecklistBlock(id="b1", items=[])
        block.add_item("Tâche 1")
        items = block.get_data()["items"]
        assert len(items) == 1
        assert items[0]["text"] == "Tâche 1"
        assert items[0]["checked"] is False

    def test_checklist_toggle_item(self):
        """toggle_item doit inverser l'état coché d'un item."""
        block = ChecklistBlock(id="b1", items=[{"text": "Tâche", "checked": False}])
        block.toggle_item(0)
        assert block.get_data()["items"][0]["checked"] is True
        block.toggle_item(0)
        assert block.get_data()["items"][0]["checked"] is False

    def test_checklist_remove_item(self):
        """remove_item doit supprimer l'item à l'index donné."""
        block = ChecklistBlock(id="b1", items=[
            {"text": "T1", "checked": False},
            {"text": "T2", "checked": False}
        ])
        block.remove_item(0)
        assert len(block.get_data()["items"]) == 1
        assert block.get_data()["items"][0]["text"] == "T2"

    def test_table_block_add_row(self):
        """add_row doit ajouter une ligne au tableau."""
        block = TableBlock(id="b1", headers=["Col1", "Col2"], rows=[])
        block.add_row(["A", "B"])
        assert len(block.get_data()["rows"]) == 1

    def test_table_block_remove_row(self):
        """remove_row doit supprimer la ligne à l'index donné."""
        block = TableBlock(id="b1", headers=["Col1"], rows=[["A"], ["B"]])
        block.remove_row(0)
        assert len(block.get_data()["rows"]) == 1
        assert block.get_data()["rows"][0] == ["B"]

    def test_bloc_to_dict_contient_type_et_data(self):
        """to_dict doit contenir les clés 'type', 'id' et 'data'."""
        block = TextBlock(id="b1", content="Test")
        d = block.to_dict()
        assert "id" in d
        assert "type" in d
        assert "data" in d


# ======================================================
# POMODORO MODULE
# ======================================================

class TestPomodoroModule:
    """Tests unitaires de l'entité PomodoroModule."""

    def setup_method(self):
        """Crée un module Pomodoro réutilisable avant chaque test."""
        self.module = PomodoroModule(
            id="m1", owner_id="u1", name="Focus session"
        )

    def test_valeurs_par_defaut(self):
        """Les paramètres doivent correspondre à la technique Pomodoro standard."""
        assert self.module.work_minutes         == 25
        assert self.module.break_minutes        == 5
        assert self.module.long_break_minutes   == 15
        assert self.module.sessions_before_long == 4

    def test_renommage_valide(self):
        """Le renommage doit mettre à jour le nom."""
        self.module.rename("Deep Work")
        assert self.module.name == "Deep Work"

    def test_renommage_vide_leve_erreur(self):
        """Un nom vide doit lever ValueError."""
        with pytest.raises(ValueError):
            self.module.rename("")

    def test_update_config_partiel(self):
        """update_config doit modifier uniquement les paramètres fournis."""
        self.module.update_config(work_minutes=50)
        assert self.module.work_minutes  == 50
        assert self.module.break_minutes == 5  # inchangé

    def test_update_config_invalide_leve_erreur(self):
        """Une valeur <= 0 doit lever ValueError."""
        with pytest.raises(ValueError):
            self.module.update_config(work_minutes=0)

    def test_lien_intention(self):
        """attach_to_intention doit mettre à jour intention_id."""
        self.module.attach_to_intention("i1")
        assert self.module.intention_id == "i1"

    def test_delier_intention(self):
        """detach_from_intention doit remettre intention_id à None."""
        self.module.attach_to_intention("i1")
        self.module.detach_from_intention()
        assert self.module.intention_id is None

    def test_to_persistence_contient_config(self):
        """to_persistence doit inclure la configuration sérialisée."""
        data = self.module.to_persistence()
        assert "config" in data
        assert "id" in data
        assert "owner_id" in data


# ======================================================
# POMODORO SESSION
# ======================================================

class TestPomodoroSession:
    """Tests unitaires de l'entité PomodoroSession."""

    def test_creation_session_completed(self):
        """Une session créée avec COMPLETED doit avoir le bon statut."""
        session = PomodoroSession(
            id="s1", module_id="m1",
            work_duration=25, break_duration=0,
            status=SessionStatus.COMPLETED.value,
            started_at=datetime(2026, 4, 6, 10, 0),
            ended_at=datetime(2026, 4, 6, 10, 25)
        )
        assert session.status      == SessionStatus.COMPLETED.value
        assert session.work_duration == 25

    def test_creation_session_interrupted(self):
        """Une session interrompue doit avoir le statut INTERRUPTED."""
        session = PomodoroSession(
            id="s2", module_id="m1",
            work_duration=10, break_duration=0,
            status=SessionStatus.INTERRUPTED.value
        )
        assert session.status == SessionStatus.INTERRUPTED.value

    def test_to_persistence_ended_at_none(self):
        """to_persistence doit gérer ended_at=None sans erreur."""
        session = PomodoroSession(
            id="s3", module_id="m1",
            work_duration=25, break_duration=0,
            status=SessionStatus.COMPLETED.value
        )
        data = session.to_persistence()
        assert data["ended_at"] is None

    def test_from_persistence_restaure_etat(self):
        """from_persistence doit restaurer exactement l'état persisté."""
        session = PomodoroSession.from_persistence(
            id="s4", module_id="m1",
            work_duration=25, break_duration=0,
            status=SessionStatus.COMPLETED.value,
            started_at=datetime(2026, 4, 6, 10, 0).isoformat(),
            ended_at=datetime(2026, 4, 6, 10, 25).isoformat()
        )
        assert session.work_duration == 25
        assert session.ended_at      == datetime(2026, 4, 6, 10, 25)