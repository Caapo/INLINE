from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import QFile, QIODevice
from pathlib import Path


# ====== Relatif à tout le dossier relatif à l'UI ======
# .ui contient le design d'une interface
# .py contient la logique d'une interface
# .css contient le style d'une interface



# === CLASS ConnexionView ===
# Contient la logique de l'interface de connexion (récupération du design de l'ui depuis le fichier connexion_view.ui))

class ConnexionView(QWidget):

    def __init__(self, user_service):
        super().__init__()

        self._service = user_service

        loader = QUiLoader()

        #Chargement du fichier .ui (.ui créée depuis QtDesigner)
        base_dir = Path(__file__).resolve().parent
        ui_path = base_dir / "connexion_view.ui"
        ui_file = QFile(ui_path)

        if not ui_file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(f"Impossible d'ouvrir {ui_path}")

        #Chargement du style depuis .css
        base_dir = Path(__file__).resolve().parent
        style_path = base_dir.parent / "styles" / "main.css"
        with open(style_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        #QWidget contenant l'interface chargée depuis le fichier .ui
        self._ui = loader.load(ui_file, self)

        #Récupération des éléments de l'interface
        self._email_input = self._ui.findChild(QLineEdit, "emailInput")
        self._username_input = self._ui.findChild(QLineEdit, "usernameInput")
        self._connexion_status_label = self._ui.findChild(QLabel, "connexionStatusLabel")
        self._create_account_button = self._ui.findChild(QPushButton, "createAccountButton")

        #Définition des actions sur les éléments de l'interface
        self._create_account_button.clicked.connect(self.create_account)

        ui_file.close()

    # -------------------------------------------------------------------

    def create_account(self):
        email = self._email_input.text()
        username = self._username_input.text()

        try:
            user = self._service.create_user(email, username)
            self._connexion_status_label.setVisible(True)
            self._connexion_status_label.setText("Compte créé")
        except Exception as e:
            self._connexion_status_label.setVisible(True)
            self._connexion_status_label.setText(str(e))