from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import QFile, QIODevice
from pathlib import Path
from presentation.views.main.home_view import HomeView


# ====== Relatif à tout le dossier relatif à l'UI ======
# .ui contient le design d'une interface
# .py contient la logique d'une interface
# .css contient le style d'une interface



# === CLASS SignUpView ===
# Contient la logique de l'interface de connexion (récupération du design de l'ui depuis le fichier sign_up_view.ui))

class SignUpView(QWidget):

    def __init__(self, user_service):
        super().__init__()

        self._service = user_service

        loader = QUiLoader()

        #Chargement du fichier .ui (.ui créée depuis QtDesigner)
        base_dir = Path(__file__).resolve().parent
        ui_path = base_dir / "sign_up_view.ui"
        ui_file = QFile(ui_path)

        if not ui_file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(f"Impossible d'ouvrir {ui_path}")

        #Chargement du style depuis .css
        style_path = base_dir.parent.parent / "styles" / "main.css"
        with open(style_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        #QWidget contenant l'interface chargée depuis le fichier .ui (chargé en mémoire)
        self._ui = loader.load(ui_file, self)

        #Récupération des éléments de l'interface
        self._email_input = self._ui.findChild(QLineEdit, "emailInput")
        self._username_input = self._ui.findChild(QLineEdit, "usernameInput")
        self._sign_up_status_label = self._ui.findChild(QLabel, "signUpStatusLabel")
        self._create_account_button = self._ui.findChild(QPushButton, "createAccountButton")
        self._back_button = self._ui.findChild(QPushButton, "backButton")

        #Définition des actions sur les éléments de l'interface
        self._create_account_button.clicked.connect(self.create_account)
        self._back_button.clicked.connect(self.back_redirection)

        
        ui_file.close()

    # -------------------------------------------------------------------

    def create_account(self):
        email = self._email_input.text()
        username = self._username_input.text()

        try:
            user = self._service.create_user(email, username)
            self._sign_up_status_label.setVisible(True)
            self._sign_up_status_label.setText("Compte créé")

            #Succès de la connexion
            self.close()
            self._home = HomeView(user)
            self._home.show()

        except Exception as e:
            self._sign_up_status_label.setVisible(True)
            self._sign_up_status_label.setText(str(e))

    # -------------------------------------------------------------------

    def back_redirection(self):
        #Redirection vers la page d'authentification
        from presentation.views.authentification.authentification_view import AuthentificationView
        self.close()
        self._authentification = AuthentificationView(self._service)
        self._authentification.show()