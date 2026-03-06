from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QFile, QIODevice
from pathlib import Path


class HomeView(QWidget):

    def __init__(self, user):
        super().__init__()

        loader = QUiLoader()

        base_dir = Path(__file__).resolve().parent
        ui_path = base_dir / "home_view.ui"
        ui_file = QFile(ui_path)

        if not ui_file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(f"Impossible d'ouvrir {ui_path}")

        self._ui = loader.load(ui_file, self)


        ui_file.close()