# ============== INLINE/src/shared/observer.py =============

class Observable:
    """
    Classe de base implémentant le patron de conception Observer.

    Permet à n'importe quel service de notifier des abonnés
    (composants UI, autres services) lors de changements d'état,
    sans connaître ni dépendre de ces abonnés.

    Utilisation :
        - Les services héritent d'Observable (IntentionService, EventService, etc.)
        - Les pages UI s'abonnent via subscribe() au démarrage
        - Les services appellent notify() après chaque modification

    Patron de conception : Observer (Comportement)
        Observable = Sujet (Subject)
        Les callbacks enregistrés = Observateurs (Observers)

    Attributs :
        _subscribers (dict[str, list]): Dictionnaire associant
            chaque nom d'événement à une liste de callbacks.

    Exemple d'utilisation :
        # Côté service (sujet)
        self.notify("intention_created", intention)

        # Côté UI (observateur)
        intention_service.subscribe("intention_created", self._on_intention_created)
    """

    # ==========================
    # CONSTRUCTEUR
    # ==========================

    def __init__(self):
        self._subscribers: dict[str, list] = {}


    # ==========================
    # MÉTHODES DE GESTION DES ABONNÉS
    # ==========================

    def subscribe(self, event: str, callback):
        """
        Abonne un callback à un événement donné.
        Crée la liste des abonnés si l'événement n'existe pas encore.
        Args:
            event (str): Nom de l'événement à écouter
                         (ex: 'intention_created', 'event_updated').
            callback: Fonction appelée lors de la notification.
                      Reçoit le payload en argument.
        """
        self._subscribers.setdefault(event, []).append(callback)


    def unsubscribe(self, event: str, callback):
        """
        Désabonne un callback d'un événement.
        Ne fait rien si le callback n'est pas abonné.
        Args:
            event (str): Nom de l'événement.
            callback: Fonction à retirer des abonnés.
        """
        if event in self._subscribers:
            self._subscribers[event].remove(callback)


    def notify(self, event: str, payload=None):
        """
        Notifie tous les abonnés d'un événement donné.
        Appelle chaque callback avec le payload fourni.
        Ne fait rien si aucun abonné n'est enregistré pour cet événement.
        Args:
            event (str): Nom de l'événement à émettre.
            payload: Données associées à l'événement
                     (entité modifiée, id supprimé, etc.).
                     None par défaut.
        """
        for callback in self._subscribers.get(event, []):
            callback(payload)


# ======================================================
# Référence des événements notifiés
# ======================================================

# IntentionService
# "intention_created"  -> payload: Intention
# "intention_updated"  -> payload: Intention
# "intention_deleted"  -> payload: intention_id (str)

# EventService
# "event_created"      -> payload: Event
# "event_updated"      -> payload: Event
# "event_deleted"      -> payload: event_id (str)

# EnvironmentService
# "environment_created" -> payload: Environment
# "environment_renamed" -> payload: Environment
# "environment_deleted" -> payload: env_id (str)

# NoteService
# "note_created"       -> payload: Note
# "note_updated"       -> payload: Note
# "note_deleted"       -> payload: note_id (str)
# "note_linked"        -> payload: dict {note_id, intention_id}

# ModuleService
# "module_created"     -> payload: PomodoroModule
# "module_updated"     -> payload: PomodoroModule
# "module_deleted"     -> payload: module_id (str)
# "session_recorded"   -> payload: PomodoroSession