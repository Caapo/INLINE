

# ======= INLINE/src/presentation/views/main/app.py =======
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from pathlib import Path

from presentation.views.main.home.home_page import HomePage
from presentation.views.main.visualization.visualization_page import VisualizationPage
from presentation.views.main.notes.notes_page import NotesPage
from presentation.views.main.module.modules_page import ModulesPage
from presentation.views.main.activity.activity_page import ActivityPage


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._load_ui()
        self._apply_styles()
        self._setup_pages()
        self._setup_navigation()
        icon_menu = self.ui.findChild(QtWidgets.QWidget, "iconOnlyMenu")
        icon_menu.hide()

        self.switch_page(self.home_page)

        self.resize(1080, 651)
        self.show()


    def _apply_styles(self):
        css_path = Path(__file__).parent.parent.parent / "styles" / "main_window.css"
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                style = f.read()
                self.setStyleSheet(style) 
        else:
            print("Fichier CSS introuvable :", css_path)


    #Chargement de l'interface depuis le fichier .ui
    def _load_ui(self):
        base_dir = Path(__file__).resolve().parent
        ui_path = base_dir / "app.ui"

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
   
    #Définition des pages
    def _setup_pages(self):
        self.home_page = HomePage()
        self.visualization_page = VisualizationPage()
        self.notes_page = NotesPage()
        self.modules_page = ModulesPage()
        self.activity_page = ActivityPage()

        #Mapping pages
        self.pages = {
            "home": ("homePage", self.home_page),
            "visualization": ("visualizationPage", self.visualization_page),
            "notes": ("notesPage", self.notes_page),
            "modules": ("modulesPage", self.modules_page),
            "activity": ("activityPage", self.activity_page),
        }

        #Remplacement des placeholders
        for key, (placeholder_name, page) in self.pages.items():
            placeholder = self._get_widget(placeholder_name, QtWidgets.QWidget)
            index = self.stacked_widget.indexOf(placeholder)

            if index == -1:
                raise RuntimeError(f"Placeholder introuvable dans stackedWidget: {placeholder_name}")

            self.stacked_widget.removeWidget(placeholder)
            self.stacked_widget.insertWidget(index, page)

    #Navigation
    def _setup_navigation(self):
        #Mapping boutons
        self.navigation = {
            "home": ("homeFullButton", "homeIconButton"),
            "visualization": ("visualizationFullButton", "visualizationIconButton"),
            "notes": ("notesFullButton", "notesIconButton"),
            "modules": ("modulesFullButton", "modulesIconButton"),
            "activity": ("activityFullButton", "activityIconButton"),
        }

        for key in self.navigation:
            full_name, icon_name = self.navigation[key]
            page = self.pages[key][1]

            full_btn = self._get_widget(full_name, QtWidgets.QPushButton)
            icon_btn = self._get_widget(icon_name, QtWidgets.QPushButton)

            full_btn.clicked.connect(lambda _, p=page: self.switch_page(p))
            icon_btn.clicked.connect(lambda _, p=page: self.switch_page(p))

    #Utilitaires
    def _get_widget(self, name, widget_type):
        widget = self.ui.findChild(widget_type, name)
        if widget is None:
            raise RuntimeError(f"Widget introuvable: {name}")
        return widget

    def switch_page(self, page):
        self.stacked_widget.setCurrentWidget(page)