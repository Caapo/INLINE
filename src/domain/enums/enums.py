# ========= INLINE/src/domain/enums/enums.py =========

from enum import Enum

# -------- OBJECTS (Plus utilisé pour l'instant) --------
class ObjectCategory(Enum):
    PHYSIQUE = 0
    MENTAL = 1        
    PSYCHE = 2             

# -------- EVENTS --------
class EventStatus(Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# -------- NOTES --------
class BlockType(Enum):
    TITLE     = "title"
    TEXT      = "text"
    CHECKLIST = "checklist"
    TABLE     = "table"


# -------- MODULES --------
class ModuleType(Enum):
    POMODORO = "pomodoro"

class SessionStatus(Enum):
    COMPLETED  = "completed"
    INTERRUPTED = "interrupted"