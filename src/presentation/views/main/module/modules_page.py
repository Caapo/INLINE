# ==== INLINE/src/presentation/views/main/module/modules_page.py ====

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QSplitter, QFrame,
    QInputDialog, QMessageBox, QDialog, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from presentation.views.main.module.module_detail_panel import ModuleDetailPanel
from presentation.views.main.module.pomodoro.dialogs.create_pomodoro_dialog import CreatePomodoroDialog
from presentation.views.main.module.pomodoro.dialogs.configure_pomodoro_dialog import ConfigurePomodoroDialog


class ModulesPage(QWidget):
    """
    Page principale de gestion des modules.
    Affiche la liste des modules à gauche et le panneau
    de détail interactif à droite.
    S'abonne aux événements du ModuleService via Observer
    pour se mettre à jour automatiquement.
    """

    def __init__(self, module_service=None, intention_service=None, parent=None):
        super().__init__(parent)
        self.module_service    = module_service
        self.intention_service = intention_service
        self._init_ui()
        self._subscribe()
        self._load_modules()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- Panneau gauche ----
        left_panel = QFrame()
        left_panel.setFixedWidth(260)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 16, 12, 12)
        left_layout.setSpacing(8)

        lbl = QLabel("Modules")
        left_layout.addWidget(lbl)

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Tous les modules", None)
        self.filter_combo.currentIndexChanged.connect(self._apply_filter)
        left_layout.addWidget(self.filter_combo)

        self.module_list = QListWidget()
        self.module_list.currentItemChanged.connect(self._on_module_selected)
        left_layout.addWidget(self.module_list, stretch=1)

        btn_new = QPushButton("+ Nouveau Pomodoro")
        btn_new.clicked.connect(self._create_module)
        left_layout.addWidget(btn_new)

        action_layout = QHBoxLayout()
        btn_rename = QPushButton("✎")
        btn_rename.setToolTip("Renommer")
        btn_rename.setFixedHeight(32)
        btn_rename.clicked.connect(self._rename_module)

        btn_link = QPushButton("🔗")
        btn_link.setToolTip("Lier à une intention")
        btn_link.setFixedHeight(32)
        btn_link.clicked.connect(self._link_intention)

        btn_unlink = QPushButton("✕🔗")
        btn_unlink.setToolTip("Délier l'intention")
        btn_unlink.setFixedHeight(32)
        btn_unlink.clicked.connect(self._unlink_intention)

        btn_delete = QPushButton("🗑")
        btn_delete.setToolTip("Supprimer")
        btn_delete.setFixedHeight(32)
        btn_delete.clicked.connect(self._delete_module)

        action_layout.addWidget(btn_rename)
        action_layout.addWidget(btn_link)
        action_layout.addWidget(btn_unlink)
        action_layout.addWidget(btn_delete)
        left_layout.addLayout(action_layout)

        btn_config = QPushButton("⚙  Configurer")
        btn_config.clicked.connect(self._configure_module)
        left_layout.addWidget(btn_config)

        # ---- Panneau droit ----
        self.detail_panel = ModuleDetailPanel(
            module_service=self.module_service,
            intention_service=self.intention_service
        )

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.detail_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setHandleWidth(1)
        main_layout.addWidget(splitter)

    def _subscribe(self):
        """Abonne la page aux événements du ModuleService via Observer."""
        if self.module_service:
            self.module_service.subscribe("module_created", self._on_module_changed)
            self.module_service.subscribe("module_updated", self._on_module_updated)
            self.module_service.subscribe("module_deleted", self._on_module_changed)

    def _on_module_changed(self, payload):
        """Recharge la liste complète lors d'une création ou suppression."""
        self._load_modules()

    def _on_module_updated(self, module):
        """Met à jour uniquement l'item concerné dans la liste."""
        for i in range(self.module_list.count()):
            item = self.module_list.item(i)
            if item.data(Qt.UserRole) == module.id:
                suffix = " 🔗" if module.intention_id else ""
                item.setText(f"🍅 {module.name}{suffix}")
                break

    def _load_modules(self):
        """Recharge la liste et le filtre par intention."""
        self.module_list.clear()
        if not self.module_service:
            return

        current_filter = self.filter_combo.currentData()
        self.filter_combo.blockSignals(True)
        self.filter_combo.clear()
        self.filter_combo.addItem("Tous les modules", None)
        if self.intention_service:
            for i in self.intention_service.get_all_intentions():
                self.filter_combo.addItem(f"📌 {i.title}", i.id)
        self.filter_combo.blockSignals(False)

        for i in range(self.filter_combo.count()):
            if self.filter_combo.itemData(i) == current_filter:
                self.filter_combo.setCurrentIndex(i)
                break

        self._apply_filter()

    def _apply_filter(self):
        """Applique le filtre par intention sur la liste des modules."""
        self.module_list.clear()
        if not self.module_service:
            return

        intention_id = self.filter_combo.currentData()
        modules = (
            self.module_service.get_modules_for_intention(intention_id)
            if intention_id
            else self.module_service.get_modules_for_user("1")
        )

        for module in modules:
            suffix = " 🔗" if module.intention_id else ""
            item   = QListWidgetItem(f"🍅 {module.name}{suffix}")
            item.setData(Qt.UserRole, module.id)
            if module.intention_id:
                item.setForeground(QColor("#4A90D9"))
            self.module_list.addItem(item)

    def _on_module_selected(self, item):
        """Charge le module sélectionné dans le panneau de détail."""
        if not item:
            return
        module = self.module_service.get_module(item.data(Qt.UserRole))
        if module:
            self.detail_panel.load_module(module)

    def _selected_module(self):
        """Retourne le module actuellement sélectionné ou None."""
        item = self.module_list.currentItem()
        if not item:
            return None
        return self.module_service.get_module(item.data(Qt.UserRole))

    def _create_module(self):
        """Ouvre le dialog de création et crée le module via le service."""
        dialog = CreatePomodoroDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.module_service.create_pomodoro(owner_id="1", **dialog.get_values())

    def _rename_module(self):
        """Renomme le module sélectionné."""
        module = self._selected_module()
        if not module:
            return
        new_name, ok = QInputDialog.getText(
            self, "Renommer", "Nouveau nom :", text=module.name
        )
        if ok and new_name:
            self.module_service.rename_module(module.id, new_name)
            if (self.detail_panel.current_module and
                    self.detail_panel.current_module.id == module.id):
                self.detail_panel.pomodoro_widget.lbl_module_name.setText(new_name)

    def _link_intention(self):
        """Lie le module sélectionné à une intention."""
        module = self._selected_module()
        if not module or not self.intention_service:
            return
        intentions = self.intention_service.get_all_intentions()
        if not intentions:
            QMessageBox.information(self, "Info", "Aucune intention disponible.")
            return
        choice, ok = QInputDialog.getItem(
            self, "Lier à une intention", "Choisir :",
            [i.title for i in intentions], 0, False
        )
        if ok and choice:
            intention = next(i for i in intentions if i.title == choice)
            self.module_service.attach_to_intention(module.id, intention.id)

    def _unlink_intention(self):
        """Délie le module sélectionné de son intention."""
        module = self._selected_module()
        if not module or not module.intention_id:
            return
        self.module_service.detach_from_intention(module.id)

    def _delete_module(self):
        """Supprime le module sélectionné après confirmation."""
        module = self._selected_module()
        if not module:
            return
        confirm = QMessageBox.question(
            self, "Supprimer",
            f"Supprimer le module « {module.name} » et tout son historique ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.module_service.delete_module(module.id)
            self.detail_panel.stack.setCurrentIndex(0)

    def _configure_module(self):
        """Ouvre le dialog de configuration et applique les nouvelles valeurs."""
        module = self._selected_module()
        if not module:
            return
        dialog = ConfigurePomodoroDialog(module, self)
        if dialog.exec() == QDialog.Accepted:
            self.module_service.update_config(module.id, **dialog.get_values())
            if (self.detail_panel.current_module and
                    self.detail_panel.current_module.id == module.id):
                updated = self.module_service.get_module(module.id)
                self.detail_panel.load_module(updated)