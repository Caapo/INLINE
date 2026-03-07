from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QFile, QIODevice
from pathlib import Path


class HomeView(QMainWindow):

    def __init__(self, user):
        super().__init__()

        self._user = user

        loader = QUiLoader()

        base_dir = Path(__file__).resolve().parent
        ui_path = base_dir / "home_view2.ui"
        ui_file = QFile(str(ui_path))

        if not ui_file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(f"Impossible d'ouvrir {ui_path}")

        self._ui = loader.load(ui_file)
        self.setCentralWidget(self._ui)
        

        # #Récupération des éléments de l'interface
        # self._stack = self._ui.findChild(QStackedWidget, "stackedWidget")
        # self._visualization_button = self._ui.findChild(QPushButton, "visualizationButton")
        # self._notes_button = self._ui.findChild(QPushButton, "notesButton")
        # self._modules_button = self._ui.findChild(QPushButton, "modulesButton")
        # self._state_button = self._ui.findChild(QPushButton, "stateButton")
        # self._user_button = self._ui.findChild(QPushButton, "userButton")
        # self._menu_button = self._ui.findChild(QPushButton, "menuButton")


        ui_file.close()