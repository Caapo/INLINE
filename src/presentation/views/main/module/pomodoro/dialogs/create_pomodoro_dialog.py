# INLINE/src/presentation/views/main/module/dialogs/create_pomodoro_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QSpinBox,
    QDialogButtonBox, QLineEdit
)


class CreatePomodoroDialog(QDialog):
    """
    Dialog de création d'un nouveau module Pomodoro.
    Permet à l'utilisateur de configurer les paramètres
    avant la création.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau module Pomodoro")
        self.resize(360, 280)

        layout = QVBoxLayout(self)
        form   = QFormLayout()
        form.setSpacing(12)

        self.name_edit = QLineEdit("Mon Pomodoro")

        self.work_spin = QSpinBox()
        self.work_spin.setRange(1, 120)
        self.work_spin.setValue(25)
        self.work_spin.setSuffix(" min")

        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 60)
        self.break_spin.setValue(5)
        self.break_spin.setSuffix(" min")

        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 120)
        self.long_break_spin.setValue(15)
        self.long_break_spin.setSuffix(" min")

        self.sessions_spin = QSpinBox()
        self.sessions_spin.setRange(1, 20)
        self.sessions_spin.setValue(4)
        self.sessions_spin.setSuffix(" sessions")

        form.addRow("Nom :",                         self.name_edit)
        form.addRow("Travail :",                     self.work_spin)
        form.addRow("Pause courte :",                self.break_spin)
        form.addRow("Pause longue :",                self.long_break_spin)
        form.addRow("Sessions avant longue pause :", self.sessions_spin)

        layout.addLayout(form)
        layout.addStretch()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_values(self) -> dict:
        """Retourne les valeurs saisies par l'utilisateur."""
        return {
            "name":                 self.name_edit.text().strip() or "Mon Pomodoro",
            "work_minutes":         self.work_spin.value(),
            "break_minutes":        self.break_spin.value(),
            "long_break_minutes":   self.long_break_spin.value(),
            "sessions_before_long": self.sessions_spin.value()
        }