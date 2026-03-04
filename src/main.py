# === Rendu UI ===
from PySide6.QtWidgets import QApplication
import sys

# === User/Connexion ===
from infrastructure.repositories.sqlite.sqlite_user_repository import SQLiteUserRepository
from application.services.user_service import UserService
from presentation.views.connexion_view import ConnexionView

# === Others ===
from pathlib import Path


# ================ MAIN =================

def main():
    
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "inline.db"
    user_repository = SQLiteUserRepository(db_path)
    user_service = UserService(user_repository)

    window = ConnexionView(user_service)
    window.show()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()