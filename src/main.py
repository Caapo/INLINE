# === Général ===
from PySide6.QtWidgets import QApplication
import sys

# === Repositories ===
from infrastructure.repositories.sqlite.sqlite_user_repository import SQLiteUserRepository

# === Services===
from application.services.user_service import UserService


# === Views ===
from presentation.views.authentification.authentification_view import AuthentificationView
# from presentation.views.authentification.authentification_view import AuthentificationView


# === Others ===
from pathlib import Path


# ================ MAIN =================

def main():
    
    app = QApplication(sys.argv)

    #Dépendances
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "inline.db"

    user_repository = SQLiteUserRepository(db_path)
    user_service = UserService(user_repository)

    #Vue au lancement de l'application
    window = AuthentificationView(user_service)
    window.show()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()