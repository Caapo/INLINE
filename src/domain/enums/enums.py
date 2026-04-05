# ========= INLINE/src/domain/enums/enums.py =========

from enum import Enum

class ObjectCategory(Enum):
    PHYSIQUE = 0
    MENTAL = 1        
    PSYCHE = 2             

class EventStatus(Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    CANCELLED = "cancelled"



class BlockType(Enum):
    TITLE     = "title"
    TEXT      = "text"
    CHECKLIST = "checklist"
    TABLE     = "table"