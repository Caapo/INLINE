# === Général ===
from PySide6.QtWidgets import QApplication
import sys
from pathlib import Path
from datetime import datetime

#Dossier racine du projet
root = Path(__file__).resolve().parents[1]
sys.path.append(str(root))


# === Repositories ===
from infrastructure.repositories.sqlite.sqlite_user_repository import SQLiteUserRepository
from infrastructure.repositories.sqlite.sqlite_intention_repository import SQLiteIntentionRepository
from infrastructure.repositories.sqlite.sqlite_event_repository import SQLiteEventRepository

# === Services===
from application.services.user_service import UserService
from application.services.intention_service import IntentionService
from application.services.event_service import EventService

# === Factories ===
from factories.intention_factory import IntentionFactory
from factories.event_factory import EventFactory


# === Views ===
from presentation.views.authentification.authentification_view import AuthentificationView
# from presentation.views.authentification.authentification_view import AuthentificationView
import assets.resources_rc



# ================ MAIN =================




def main():

    # === Initialisation des dépendances ===
    print("Initialisation des dépendances...")

    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "inline.db"  

    #Repositories
    user_repo = SQLiteUserRepository(db_path)
    intention_repo = SQLiteIntentionRepository(db_path)
    event_repo = SQLiteEventRepository(db_path)

    #Factories
    intention_factory = IntentionFactory()
    event_factory = EventFactory()

    #Services
    user_service = UserService(user_repo)
    intention_service = IntentionService(intention_repo, intention_factory)
    event_service = EventService(event_repo, event_factory)

    print("Initialisation terminée.")

    # ==== Test Utilisateur ====
    print("\nTest utilisateur")
    user = user_service.create_user(email="usertest2@gmail.com", username="usertest2")
    user_info = user.get_user_info()
    print(user_info["email"], user_info["username"])

    # ==== Test Intention ====
    print("\nTest intention")
    intention = intention_service.create_intention(user_id=user._id, title="Test Intention", category="Test")
    intention_info = intention.get_info()
    print(intention_info["title"], intention_info["category"], intention_info["is_active"])

    # #Activation
    # intention_service.activate_intention(intention.id)
    # intention_repo.save(intention)
    # print(f"Intention activée. Intention active pour l'utilisateur: {intention_service.get_active_intention(user.id)}")
    # print(intention_info["title"], intention_info["category"], intention_info["is_active"])
    # #Désactivation
    # intention_service.deactivate_intention(intention.id)
    # intention_repo.save(intention)
    # print(f"Intention désactivée. Intention active pour l'utilisateur: {intention_service.get_active_intention(user.id)}")
    # print(intention_info["title"], intention_info["category"], intention_info["is_active"])

    # # ==== Test Event ====
    # print("Test event")
    # event_test = event_service.create_event(intention_id=intention.id, start_time=datetime.now(), duration=60)
    # print(f"Event créé: {event_test.intention_id}, {event_test.start_time}, {event_test.duration}")





# def main():
    
#     app = QApplication(sys.argv)

#     #Dépendances
#     base_dir = Path(__file__).resolve().parent.parent
#     db_path = base_dir / "data" / "inline.db"

#     user_repository = SQLiteUserRepository(db_path)
#     user_service = UserService(user_repository)

#     #Vue au lancement de l'application
#     window = AuthentificationView(user_service)
#     window.show()

#     sys.exit(app.exec())



if __name__ == "__main__":
    main()