# ==================================== main.py ====================================

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
    print("\n=== Test utilisateur ===")
    print("Création d'un utilisateur...")
    user = user_service.create_user(email="usertest2@gmail.com", username="usertest2")
    user_info = user.get_user_info()
    # print(f"Utilisateur créé: {user_info}")
    print(f"Utilisateur créé: {user}")


    # ==== Test Intention ====
    print("\n=== Test intention ===")
    print("Création d'une intention...")
    intention = intention_service.create_intention(user_id=user._id, title="Une Intention", category="Test")
    print(f"Intention créée: {intention}")

    print("\nActivation de l'intention...")
    intention = intention_service.activate_intention(intention.id)
    active_intention = intention_service.get_active_intention_by_user(user._id)
    print(f"Intention en mémoire : {intention}")
    print(f"Intention active pour l'utilisateur: {active_intention}")


    print("\nDésactivation de l'intention...")
    intention = intention_service.deactivate_intention(intention.id)
    active_intention = intention_service.get_active_intention_by_user(user._id)
    print(f"Intention en mémoire: {intention}")
    print(f"Intention active pour l'utilisateur: {active_intention}")
    

    # ==== Test Event ====
    print("\n=== Test event ===")
    print("Création d'un événement...")
    event = event_service.create_event(intention_id=intention.id, start_time=datetime.now(), duration=60)
    print(f"Événement créé: {event}")

    print("\nMise à jour de l'heure de l'événement...")
    event = event_service.update_event_time(event_id=event.id, start_time=datetime.now(), duration=90)
    print(f"Événement mis à jour: {event}")

    print("\nComplétion de l'événement...")
    event = event_service.complete_event(event_id=event.id)
    print(f"Événement complété: {event}")

    print("\nAnnulation de l'événement...")
    try:
        event = event_service.cancel_event(event_id=event.id)
        print(f"Événement annulé: {event}")
    except ValueError as e:
        print(f"Erreur lors de l'annulation de l'événement: {e}")






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