# ==================== INLINE/src/main.py ==================

# === Général ===
from PySide6.QtWidgets import QApplication
from presentation.views.main.app import MainWindow
import sys
from pathlib import Path
from datetime import date, datetime

#Dossier racine du projet
root = Path(__file__).resolve().parents[1]
sys.path.append(str(root))


# === Repositories ===
from infrastructure.repositories.sqlite.sqlite_user_repository import SQLiteUserRepository
from infrastructure.repositories.sqlite.sqlite_intention_repository import SQLiteIntentionRepository
from infrastructure.repositories.sqlite.sqlite_event_repository import SQLiteEventRepository
from infrastructure.repositories.sqlite.sqlite_environment_repository import SQLiteEnvironmentRepository

# === Services===
from application.services.user_service import UserService
from application.services.intention_service import IntentionService
from application.services.event_service import EventService
from application.services.environment_service import EnvironmentService    
from application.services.interactive_object_service import InteractiveObjectService

# === Factories ===
from factories.intention_factory import IntentionFactory
from factories.event_factory import EventFactory
from factories.environment_factory import EnvironmentFactory
from factories.interactive_object_factory import InteractiveObjectFactory

# === Queries ===
from application.queries.event_query import EventQuery
from application.queries.timeline_query import TimelineQuery

# === Views ===
from presentation.views.authentification.authentification_view import AuthentificationView
# from presentation.views.authentification.authentification_view import AuthentificationView
import assets.resources_rc

#=== Objets === (Je n'ai pas encore / Je n'ai pas créer de Factory ou de service car c'est un simple objet sans grosse gestion)
from domain.entities.i_interactive_object import IInteractiveObject
from domain.entities.clickable_object import ClickableObject
from domain.enums.enums import ObjectCategory
from domain.enums.enums import EventStatus






# ================ MAIN =================


# ================== TEST VERSION TERMINAL AVANT DE FAIRE LA LIAISON FRONTEND <=> BACKEND ==================

# def main():

#     # === Initialisation des dépendances ===
#     print("Initialisation des dépendances...")
#     base_dir = Path(__file__).resolve().parent.parent
#     db_path = base_dir / "data" / "inline.db"  

#     #Repositories
#     user_repo = SQLiteUserRepository(db_path)
#     intention_repo = SQLiteIntentionRepository(db_path)
#     event_repo = SQLiteEventRepository(db_path)
#     environment_repo = SQLiteEnvironmentRepository(db_path)

#     #Factories
#     intention_factory = IntentionFactory()
#     event_factory = EventFactory()
#     environment_factory = EnvironmentFactory()

#     #Services
#     user_service = UserService(user_repo)
#     intention_service = IntentionService(intention_repo, intention_factory)
#     event_service = EventService(event_repo, event_factory)
#     environment_service = EnvironmentService(environment_repo, environment_factory)
#     interactive_object_service = InteractiveObjectService(environment_repo, InteractiveObjectFactory())
    
#     #Queries
#     event_query = EventQuery(event_repo, intention_repo)
#     timeline_query = TimelineQuery(event_repo)

#     print("Initialisation terminée.")


#     # ==== Test Utilisateur ====
#     print("\n=== Test utilisateur ===")
#     print("Création d'un utilisateur...")
#     user = user_service.create_user(email="usertest2@gmail.com", username="usertest2")
#     user_info = user.get_user_info()
#     # print(f"Utilisateur créé: {user_info}")
#     print(f"Utilisateur créé: {user}")


#     # ==== Test Intention ====
#     print("\n=== Test intention ===")
#     print("Création d'une intention...")
#     intention = intention_service.create_intention(user_id=user.id, title="Une Intention", category="Test")
#     print(f"Intention créée: {intention}")

#     print("\nActivation de l'intention...")
#     intention = intention_service.activate_intention(intention.id)
#     active_intention = intention_service.get_active_intention_by_user(user.id)
#     print(f"Intention en mémoire : {intention}")
#     print(f"Intention active pour l'utilisateur: {active_intention}")


#     print("\nDésactivation de l'intention...")
#     intention = intention_service.deactivate_intention(intention.id)
#     active_intention = intention_service.get_active_intention_by_user(user.id)
#     print(f"Intention en mémoire: {intention}")
#     print(f"Intention active pour l'utilisateur: {active_intention}")
    

#         # === Test Environnement ====
#     print("\n=== Test environnement ===")
#     print("Création d'un environnement...")
#     environment = environment_service.create_environment(owner_id=user.id, name="Mon Environnement")
#     print(f"Environnement créé: {environment}")

#     environments = environment_service.list_all_environments()
#     print(f"Tous les environnements: {environments}")

#     owner_environments = environment_service.get_environments_for_owner(user.id)
#     print(f"Environnements de l'utilisateur: {owner_environments}")

#     # events = event_query.get_events_for_day(today)
#     # print(events)


#     # # ==== Test ClickableObject ====
#     # print("\n=== Test ClickableObject ===")
#     # print("Création d'un objet cliquable...")
#     # clickable_obj1 = ClickableObject(
#     #     id="obj1",
#     #     environment_id=environment.id,
#     #     name="Objet1 test",
#     #     position=(10, 20),
#     #     category=ObjectCategory.PHYSIQUE,
#     #     suggested_intentions=["Aller à la salle", "Manger sainement"]
#     # )

#     # environment.add_interactive_object(clickable_obj1)
#     # print(f"Objet ajouté à l'environnement: {clickable_obj1.get_info()}\n")

#     # #Interaction sans valeur (suggestions)
#     # result_suggestions = clickable_obj1.interact(user_state=user)
#     # print(f"Interaction sans input: {result_suggestions}\n")

#     # #Interaction avec valeur personnalisée
#     # result_custom = clickable_obj1.interact(user_state=user, input_value="Continuer le projet de génie log")
#     # print(f"Interaction avec input personnalisé: {result_custom}\n")

    
#     # print(f"État de l'environnement: {environment.get_info()}\n")



#     # ==== Test ClickableObject via Service ====
#     print("\n=== Test ClickableObject via Service ===")

#     # Création d'un objet cliquable via le service et la factory
#     clickable_obj1 = interactive_object_service.create_object(
#         type="clickable",
#         environment_id=environment.id,
#         id="obj1",
#         name="Objet1 test",
#         position=(10, 20),
#         category=ObjectCategory.PHYSIQUE,
#         suggested_intentions=["Aller à la salle", "Manger sainement"]
#     )

#     print(f"Objet ajouté à l'environnement: {clickable_obj1.get_info()}\n")

#     # Interaction sans valeur (suggestions)
#     result_suggestions = interactive_object_service.interact_with_object(
#         environment_id=environment.id,
#         object_id="obj1",
#         user_state=user
#     )
#     print(f"Interaction sans input: {result_suggestions}\n")

#     # Interaction avec valeur personnalisée
#     result_custom = interactive_object_service.interact_with_object(
#         environment_id=environment.id,
#         object_id="obj1",
#         user_state=user,
#         input_value="Continuer le projet de génie log"
#     )
#     print(f"Interaction avec input personnalisé: {result_custom}\n")

#     # Vérification des objets via le service
#     objects_in_env = interactive_object_service.get_objects_for_environment(environment.id)
#     print("Objets présents dans l'environnement via le service:")
#     for obj in objects_in_env:
#         print(obj.get_info())
#     print()

#     # Affichage final de l'état complet de l'environnement
#     print(f"État final de l'environnement: {environment.get_info()}\n")







#     # ==== Test Event ====
#     print("\n=== Test event ===")
#     print("Création d'un événement...")
#     event = event_service.create_event(intention_id=intention.id, environment_id=environment.id, start_time=datetime.now(), duration=60)
#     print(f"Événement créé: {event}")

#     print("\nMise à jour de l'heure de l'événement...")
#     event = event_service.update_event_time(event_id=event.id, start_time=datetime.now(), duration=90)
#     print(f"Événement mis à jour: {event}")

#     print("\nComplétion de l'événement...")
#     event = event_service.complete_event(event_id=event.id)
#     print(f"Événement complété: {event}")

#     print("\nAnnulation de l'événement...")
#     try:
#         event = event_service.cancel_event(event_id=event.id)
#         print(f"Événement annulé: {event}")
#     except ValueError as e:
#         print(f"Erreur lors de l'annulation de l'événement: {e}")


#     print("\n=== Test Timeline ===")
#     events_today = timeline_query.get_events_for_environment_and_day(environment_id=environment.id, day=date.today())

#     print("Timeline:", events_today)





  
# =============== LANCEMENT DE L'APPLICATION (AVEC INTERFACE GRAPHIQUE) ==================


# ======= INLINE/src/main.py =======
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from presentation.views.main.app import MainWindow

from infrastructure.repositories.sqlite.sqlite_user_repository import SQLiteUserRepository
from infrastructure.repositories.sqlite.sqlite_intention_repository import SQLiteIntentionRepository
from infrastructure.repositories.sqlite.sqlite_event_repository import SQLiteEventRepository
from infrastructure.repositories.sqlite.sqlite_environment_repository import SQLiteEnvironmentRepository
from infrastructure.repositories.sqlite.sqlite_note_repository import SQLiteNoteRepository
from infrastructure.repositories.sqlite.modules.sqlite_module_repository import SQLiteModuleRepository
from infrastructure.repositories.sqlite.modules.pomodoro.sqlite_pomodoro_session_repository import SQLitePomodoroSessionRepository


from factories.intention_factory import IntentionFactory
from factories.event_factory import EventFactory
from factories.environment_factory import EnvironmentFactory
from factories.interactive_object_factory import InteractiveObjectFactory
from factories.note_factory import NoteFactory
from factories.modules.module_factory import ModuleFactory

from application.services.user_service import UserService
from application.services.intention_service import IntentionService
from application.services.event_service import EventService
from application.services.environment_service import EnvironmentService
from application.services.interactive_object_service import InteractiveObjectService
from application.services.note_service import NoteService
from application.services.modules.module_service import ModuleService



def main():
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent.parent
    db_path  = base_dir / "data" / "inline.db"

    # --- Repositories ---
    user_repo        = SQLiteUserRepository(db_path)
    intention_repo   = SQLiteIntentionRepository(db_path)
    event_repo       = SQLiteEventRepository(db_path)
    environment_repo = SQLiteEnvironmentRepository(db_path)
    note_repo        = SQLiteNoteRepository(db_path)
    module_repo  = SQLiteModuleRepository(db_path)
    session_repo = SQLitePomodoroSessionRepository(db_path)

    # --- Factories ---
    intention_factory = IntentionFactory()
    event_factory     = EventFactory()
    environment_factory = EnvironmentFactory()
    note_factory      = NoteFactory()
    module_factory = ModuleFactory()

    # --- Services ---
    user_service       = UserService(user_repo)
    intention_service  = IntentionService(intention_repo, intention_factory)
    event_service      = EventService(event_repo, event_factory)
    environment_service = EnvironmentService(environment_repo, environment_factory)
    interactive_object_service = InteractiveObjectService(environment_repo, InteractiveObjectFactory())
    note_service       = NoteService(note_repository=note_repo, note_factory=note_factory, intention_repository=intention_repo)
    module_service = ModuleService(module_repository=module_repo, session_repository=session_repo, module_factory=module_factory, intention_repository=intention_repo)

    # --- Fenêtre principale ---
    window = MainWindow(
        intention_service=intention_service,
        event_service=event_service,
        environment_service=environment_service,
        interactive_object_service=interactive_object_service,
        note_service=note_service,
        module_service=module_service
    )

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()