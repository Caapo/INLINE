from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import QFile, QIODevice
from pathlib import Path
from presentation.views.authentification.sign_up_view import SignUpView
from presentation.views.authentification.log_in_view import LogInView


class AuthentificationView(QWidget):
    def __init__(self, user_service):
        super().__init__()
        self._service = user_service
        loader = QUiLoader()

        base_dir = Path(__file__).resolve().parent
        ui_path = base_dir / "authentification_view.ui"
        ui_file = QFile(ui_path)

        if not ui_file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(f"Impossible d'ouvrir {ui_path}")
    
        #Chargement du style depuis .css
        base_dir = Path(__file__).resolve().parent
        style_path = base_dir.parent.parent / "styles" / "main.css"
        with open(style_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self._ui = loader.load(ui_file, self)

        #Récupération des éléments de l'interface
        self._sign_up_button = self._ui.findChild(QPushButton, "signUpButton")
        self._log_in_button = self._ui.findChild(QPushButton, "logInButton")

        #Définition des actions sur les éléments de l'interface
        self._sign_up_button.clicked.connect(self.create_account_redirection)
        self._log_in_button.clicked.connect(self.log_in_redirection)



        ui_file.close()

    def create_account_redirection(self):
        #Redirection vers la page de création de compte
        self.close()
        self._sign_up = SignUpView(self._service)
        self._sign_up.show()

    def log_in_redirection(self):
        #Redirection vers la page de connexion
        self.close()
        self._log_in = LogInView(self._service)
        self._log_in.show()
