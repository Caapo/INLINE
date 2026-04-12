# INLINE - Application de gestion quotidienne

INLINE est une application desktop développée en Python (avec PySide6 pour l'UI). L'idée centrale est de permettre à un utilisateur de modéliser sa vie quotidienne à travers la puissance de la visualisation mentale et la création d'intentions, d'événements, de notes et de modules fonctionnels.

L'application repose sur une architecture Clean Architecture, les patrons de conception Factory et Observer, et respecte les principes SOLID.

---


## Fonctionnalités principales


Visualisation
  - Créer plusieurs environnements représentant des espaces de vie (bureau, chambre, salle de sport...)
  - Ajouter des objets interactifs dans chaque environnement et les déplacer librement
  - Cliquer sur un objet pour créer une intention liée à ce contexte
  - Naviguer entre les jours pour consulter ou planifier des événements
  - Définir une intention comme focus : les événements liés apparaissent en surbrillance dorée sur la timeline
  - Cliquer sur un événement dans la timeline pour le compléter, annuler, reprogrammer ou supprimer

Notes
  - Créer des notes composées de blocs : titre (H1/H2/H3), texte libre, checklist, tableau
  - Réordonner les blocs par glisser-déposer
  - Lier une note à une intention pour retrouver facilement les informations associées
  - Filtrer les notes par intention

Modules
    POMODORO
  - Créer un module Pomodoro avec des paramètres personnalisés (durée de travail, pauses)
  - Démarrer, mettre en pause, passer ou arrêter une session depuis l'interface
  - Consulter l'historique des sessions du jour directement dans le module
  - Lier un module à une intention pour organiser les sessions de travail

    Ajouts à venir :
    PLANIFICATEUR DE REPAS
    ...


---


## Prérequis

- Python 3.12 ou supérieur
- pip 23+
- Git
- Docker Desktop 24+ (pour exécuter les tests dans un conteneur)

---

## Installation

Cloner le repository :

    git clone https://github.com/Caapo/INLINE.git
    cd INLINE

Créer et activer un environnement virtuel :

    python -m venv venv

    # Windows
    venv\Scripts\activate

    # Linux / macOS
    source venv/bin/activate

Installer les dépendances :

    pip install -r requirements.txt

---

## Lancer l'application

    python src/main.py

La base de données SQLite est créée automatiquement dans le dossier data/ au premier lancement. Aucune configuration n'est nécessaire.

---

## Exécuter les tests

Sans Docker :

    cd src
    pytest ../tests/ -v

Avec Docker :

    # Construire l'image (première fois uniquement)
    docker build -t inline-app .

    # Lancer les tests
    docker-compose up

Les tests couvrent les entités du domaine : Intention, Event, Note, les blocs de notes, PomodoroModule et PomodoroSession. 47 tests unitaires, 0 échec.
Les warnings présents ne représentent pas de dangers (ils sont liés à la dispiration de datetime.utcnow() dans les futures versions de python).

---

## Structure du projet

    INLINE/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── README.md
    ├── data/                        Base de données SQLite (générée automatiquement)
    ├── tests/
    │   └── test_domain.py           Tests unitaires des entités du domaine (sert notamment au Docker)
    └── src/
        ├── main.py                  Point d'entrée de l'application
        ├── shared/
        │   └── observer.py          Patron Observer - classe Observable
        ├── domain/
        │   ├── entities/            Entités métier (Intention, Event, Note, Environment...)
        │   ├── repositories/        Interfaces des repositories (DIP)
        │   └── enums/               Énumérations métier
        ├── factories/               Patron Factory - création des objets du domaine
        ├── application/
        │   └── services/            Services applicatifs - orchestration des cas d'usage
        ├── infrastructure/
        │   └── repositories/sqlite/ Implémentations SQLite des repositories
        └── presentation/
            └── views/               Interface graphique PySide6

---

## Architecture

L'application est organisée en quatre couches indépendantes :

    Présentation  ->  Application  ->  Domaine  <-  Infrastructure

- La couche Domaine contient la logique métier pure, sans aucune dépendance externe.
- La couche Application orchestre les cas d'usage via des services.
- La couche Infrastructure gère la persistance (SQLite) en implémentant les interfaces définies dans le domaine.
- La couche Présentation affiche les données et réagit aux événements via le patron Observer.

Patrons de conception utilisés :

- Factory : centralise la création des objets métier (IntentionFactory, EventFactory, NoteFactory, NoteBlockFactory, ModuleFactory, EnvironmentFactory, InteractiveObjectFactory)
- Observer : découple les services de l'interface graphique. Chaque service hérite de Observable et notifie les composants UI abonnés lors de chaque modification.

---

## Dépendances

- PySide6 6.10.2 - interface graphique Qt
- pytest 8.3.5 - tests unitaires

---

## Base de données

INLINE utilise SQLite. La base est créée automatiquement au premier lancement dans data/inline.db. Les tables suivantes sont gérées automatiquement : intentions, events, environments, notes, modules, pomodoro_sessions.

Tables principales :

intentions
  - id, user_id, title, category, object_id, is_active, created_at, metadata
  - Une seule intention peut être active (focus) par utilisateur à la fois
  - Contrainte unique en base : idx_unique_active_intention sur (user_id) WHERE is_active = 1

events
  - id, intention_id, environment_id, start_time, duration, end_time, status, created_at, metadata
  - status peut valoir : planned, completed, cancelled
  - end_time est calculé automatiquement depuis start_time + duration

environments
  - id, owner_id, name, objects, created_at, metadata
  - Les objets interactifs sont sérialisés en JSON dans la colonne objects

notes
  - id, owner_id, title, blocks, intention_id, created_at, updated_at, metadata
  - Les blocs sont sérialisés en JSON dans la colonne blocks
  - intention_id est nullable - une note peut exister sans intention associée

modules
  - id, owner_id, name, type, intention_id, config, created_at, updated_at, metadata
  - La configuration du module (durées, paramètres) est sérialisée en JSON dans config

pomodoro_sessions
  - id, module_id, work_duration, break_duration, status, started_at, ended_at
  - Chaque session correspond à une phase de travail complétée ou interrompue



## Étendre l'application (Pour développeurs)

Ajouter un nouveau type de module
  1. Créer la classe dans domain/entities/modules/<nom>/
  2. Ajouter la valeur correspondante dans l'enum ModuleType
  3. Ajouter la méthode de création dans ModuleFactory
  4. Ajouter la méthode dans ModuleService
  5. Créer le widget UI dans presentation/views/main/module/

Ajouter un nouveau type de bloc de note
  1. Créer la classe dans domain/entities/note_blocks.py en implémentant INoteBlock
  2. Ajouter la valeur dans l'enum BlockType
  3. Enregistrer le type dans NoteBlockFactory.create() et from_dict()
  4. Créer le widget UI correspondant dans presentation/views/main/notes/blocks/

Changer le système de persistance
  1. Créer une nouvelle implémentation du repository concerné (ex: PostgreSQLIntentionRepository)
  2. La faire implémenter l'interface correspondante (ex: IIntentionRepository)
  3. L'injecter dans main.py à la place de SQLiteIntentionRepository
