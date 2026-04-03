# ======= INLINE/src/presentation/views/main/app.py =======

# ===== Importation générale =====
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from pathlib import Path

# === Importation des pages ===
from presentation.views.main.home.home_page import HomePage
from presentation.views.main.visualization.visualization_page import VisualizationPage
from presentation.views.main.notes.notes_page import NotesPage
from presentation.views.main.module.modules_page import ModulesPage
from presentation.views.main.activity.activity_page import ActivityPage


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, intention_service, event_service, environment_service, interactive_object_service, parent=None):
        super().__init__(parent)

        #Initialisation des services
        self.intention_service = intention_service
        self.event_service = event_service
        self.environment_service = environment_service
        self.interactive_object_service = interactive_object_service

        #Initialisation de l'UI et du style
        self._load_ui()
        self._apply_styles()

        #Initialisation des pages et de la navigation
        self._setup_pages()
        self._setup_navigation()

        #Cache la barre de navigation avec uniquement les icônes
        icon_menu = self.ui.findChild(QtWidgets.QWidget, "iconOnlyMenu")
        icon_menu.hide()

        #Page d'accueil = page par défaut
        self.switch_page(self.home_page)

        #Affichage de la fenêtre
        self.resize(1080, 651)
        self.show()

    # -------------------------
    def _apply_styles(self):
        css_path = Path(__file__).parent.parent.parent / "styles" / "main_window.css"
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print("Fichier CSS introuvable :", css_path)

    # -------------------------
    def _load_ui(self):
        ui_path = Path(__file__).resolve().parent / "app.ui"
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(f"Impossible d'ouvrir {ui_path}")

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(self.ui)
        self.stacked_widget = self._get_widget("stackedWidget", QtWidgets.QStackedWidget)

        self.ui.quitFullButton.clicked.connect(self.close)
        self.ui.quitIconButton.clicked.connect(self.close)

    # -------------------------
    def _setup_pages(self):

        #Construction des pages avec les services associés
        self.home_page = HomePage()
        self.visualization_page = VisualizationPage(intention_service=self.intention_service, event_service=self.event_service, environment_service=self.environment_service, 
        interactive_object_service=self.interactive_object_service)
        self.notes_page = NotesPage()
        self.modules_page = ModulesPage()
        self.activity_page = ActivityPage()
        
        #Mapping des pages avec les placeholders correspondants dans le .ui
        self.pages = {
            "home": ("homePage", self.home_page),
            "visualization": ("visualizationPage", self.visualization_page),
            "notes": ("notesPage", self.notes_page),
            "modules": ("modulesPage", self.modules_page),
            "activity": ("activityPage", self.activity_page),
        }

        #Remplacement des placeholders par les pages réelles
        for key, (placeholder_name, page) in self.pages.items():
            placeholder = self._get_widget(placeholder_name, QtWidgets.QWidget)
            index = self.stacked_widget.indexOf(placeholder)
            if index == -1:
                raise RuntimeError(f"Placeholder introuvable: {placeholder_name}")
            self.stacked_widget.removeWidget(placeholder)
            self.stacked_widget.insertWidget(index, page)

    # -------------------------
    def _setup_navigation(self):
        #Mapping des boutons de navigation
        self.navigation = {
            "home": ("homeFullButton", "homeIconButton"),
            "visualization": ("visualizationFullButton", "visualizationIconButton"),
            "notes": ("notesFullButton", "notesIconButton"),
            "modules": ("modulesFullButton", "modulesIconButton"),
            "activity": ("activityFullButton", "activityIconButton"),
        }

        #Pour chaque bouton de navigation, on connecte le signal clicked à la page correspondante
        for key in self.navigation:
            full_name, icon_name = self.navigation[key]
            page = self.pages[key][1]
            full_btn = self._get_widget(full_name, QtWidgets.QPushButton)
            icon_btn = self._get_widget(icon_name, QtWidgets.QPushButton)
            full_btn.clicked.connect(lambda _, p=page: self.switch_page(p))
            icon_btn.clicked.connect(lambda _, p=page: self.switch_page(p))

    # -------------------------
    def _get_widget(self, name, widget_type):
        #Recherche un widget dans l'interface par son nom et son type
        widget = self.ui.findChild(widget_type, name)
        if widget is None:
            raise RuntimeError(f"Widget introuvable: {name}")
        return widget

    # -------------------------
    def switch_page(self, page):
        self.stacked_widget.setCurrentWidget(page)