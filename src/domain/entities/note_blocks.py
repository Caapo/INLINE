# ====== INLINE/src/domain/entities/note_blocks.py =====
# Implémentations concrètes de blocs de notes.
# Chaque bloc implémente l'interface INoteBlock, permettant une composition flexible dans la


from domain.entities.i_note_block import INoteBlock
from domain.enums.enums import BlockType


class TitleBlock(INoteBlock):
    """
    Bloc de titre avec niveau hiérarchique (H1, H2, H3).
    Permet de structurer visuellement une note.
    """

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================

    def __init__(self, id:str, text:str = "", level:int = 1):
        self._id = id
        self._text = text
        self._level = level 

    # ==================================================
    # MÉTHODES INTERFACE INoteBlock
    # ==================================================


    def update_data(self, data:dict) -> None:
        self._text  = data.get("text",  self._text)
        self._level = data.get("level", self._level)

    def to_dict(self) -> dict:
        return {"id": self._id, "type": self.get_type(), "data": self.get_data()}


    def get_id(self) -> str:
        return self._id


    def get_type(self) -> str: 
         return BlockType.TITLE.value


    def get_data(self) -> dict:
        return {"text": self._text, "level": self._level}

   


class TextBlock(INoteBlock):
    """
    Bloc de texte libre multi-lignes.
    Contenu principal d'une note.
    """

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================

    def __init__(self, id:str, content:str = ""):
        self._id = id
        self._content = content

    # ==================================================
    # MÉTHODES INTERFACE INoteBlock
    # ==================================================

    def update_data(self, data:dict) -> None:
        self._content = data.get("content", self._content)


    def to_dict(self) -> dict:
        return {"id": self._id, "type": self.get_type(), "data": self.get_data()}


    def get_id(self) -> str:
        return self._id

  
    def get_type(self) -> str:
        return BlockType.TEXT.value



    def get_data(self) -> dict:
        return {"content": self._content}





class ChecklistBlock(INoteBlock):
    """
    Bloc de liste de tâches avec cases à cocher.
    Chaque item est un dictionnaire {text, checked}.
    """

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================

    def __init__(self, id:str, items:list[dict] = None):
        # items = [{"text": "...", "checked": False}, ...]
        self._id = id
        self._items = items or []

    # ==================================================
    # MÉTHODES INTERFACE INoteBlock
    # ==================================================

    def get_id(self) -> str:  
        return self._id


    def get_type(self) -> str:  
        return BlockType.CHECKLIST.value

    

    def get_data(self) -> dict:
        return {"items": self._items}

    

    def update_data(self, data:dict) -> None:
        self._items = data.get("items", self._items)



    def to_dict(self) -> dict:
        return {"id": self._id, "type": self.get_type(), "data": self.get_data()}

    # ==================================================
    # AUTRES
    # ==================================================

    def add_item(self, text:str) -> None:
        self._items.append({"text": text, "checked": False})


    def toggle_item(self, index:int) -> None:
        if 0 <= index < len(self._items):
            self._items[index]["checked"] = not self._items[index]["checked"]


    def remove_item(self, index:int) -> None:
        if 0 <= index < len(self._items):
            self._items.pop(index)




class TableBlock(INoteBlock):
    """
    Bloc tableau avec en-têtes et lignes dynamiques.
    Headers et rows sont des listes de strings.
    """

    # ==================================================
    # CONSTRUCTEUR
    # ==================================================

    def __init__(self, id:str, headers:list[str]=None, rows:list[list[str]]=None):
        self._id = id
        self._headers = headers or []
        self._rows = rows or []
    
    # ==================================================
    # MÉTHODES INTERFACE INoteBlock
    # ==================================================

    def get_id(self) -> str:  
        return self._id

    
    def get_type(self) -> str:  
        return BlockType.TABLE.value

    

    def get_data(self) -> dict:
        return {"headers": self._headers, "rows": self._rows}


    def update_data(self, data:dict) -> None:
        self._headers = data.get("headers", self._headers)
        self._rows = data.get("rows",    self._rows)


    def to_dict(self) -> dict:
        return {"id": self._id, "type": self.get_type(), "data": self.get_data()}

    def add_row(self, row:list[str]) -> None:
        self._rows.append(row)
  

    def remove_row(self, index:int) -> None:
        if 0 <= index < len(self._rows):
            self._rows.pop(index)


