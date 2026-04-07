# ========= INLINE/src/domain/enums/enums.py =========

from enum import Enum

# -------- OBJECTS (Plus utilisé pour l'instant) --------
class ObjectCategory(Enum):
    """
    Catégorie d'objets dans un environnement.
    Permet de retrouver les objets plus facilement pour une extension future (ex: filtrer les objets physiques vs mentaux).
    """
    PHYSIQUE = 0
    MENTAL = 1        
    PSYCHE = 2             

# -------- EVENTS --------
class EventStatus(Enum):
    """
    Statut d'un événement dans la timeline.
    """
    PLANNED = "planned"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# -------- NOTES --------

class BlockType(Enum):
    """
    Enumération des types de blocs disponibles dans une note.
    Fermé à modification, nouveaux types via extension de l'enum.
    """
    TITLE = "title"
    TEXT = "text"
    CHECKLIST = "checklist"
    TABLE = "table"


# -------- MODULES --------
class ModuleType(Enum):
    """
    Enumération des types de modules disponibles.
    Chaque valeur correspond à une mini-application autonome.
    Extensible sans modifier les modules existants.
    """
    POMODORO = "pomodoro"

class SessionStatus(Enum):
    """
    Enumération des statuts possibles d'une session Pomodoro.
    COMPLETED - session menée à son terme.
    INTERRUPTED - session arrêtée ou passée avant la fin.
    """
    COMPLETED  = "completed"
    INTERRUPTED = "interrupted"