# === INLINE/src/presentation/views/main/home/home_page.py ===

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QScrollArea, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QDate, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient, QPen
from datetime import datetime, date
from PySide6.QtWidgets import QSizePolicy

# -------------------------------------------------------
# Citations
# -------------------------------------------------------
QUOTES = [
    ("La discipline est le pont entre les objectifs et leurs accomplissements.", "Jim Rohn"),
    ("Ce n'est pas parce que les choses sont difficiles que nous n'osons pas,\nc'est parce que nous n'osons pas qu'elles sont difficiles.", "Sénèque"),
    ("Chaque matin, nous naissons à nouveau.\nCe que nous faisons aujourd'hui compte le plus.", "Bouddha"),
    ("Le succès, c'est d'aller d'échec en échec\nsans perdre son enthousiasme.", "Winston Churchill"),
    ("Fais de ta vie un rêve, et d'un rêve une réalité.", "Antoine de Saint-Exupéry"),
    ("La seule façon de faire du bon travail\nest d'aimer ce que vous faites.", "Steve Jobs"),
    ("Commence là où tu es.\nUtilise ce que tu as. Fais ce que tu peux.", "Arthur Ashe"),
    ("La clarté précède la maîtrise.", "Robin Sharma"),
    ("Ce que tu fais aujourd'hui\npeut améliorer tous tes lendemains.", "Ralph Marston"),
    ("Ne comptez pas les jours,\nfaites que les jours comptent.", "Muhammad Ali"),
    ("Agis comme si ce que tu fais fait une différence.\nÇa en fait une.", "William James"),
    ("Le secret pour avancer est de commencer.", "Mark Twain"),
    ("Chaque accomplissement commence\npar la décision d'essayer.", "John F. Kennedy"),
    ("La meilleure façon de prédire l'avenir\nest de le créer.", "Peter Drucker"),
    ("Tu n'as pas à être excellent pour commencer,\nmais tu dois commencer pour être excellent.", "Zig Ziglar"),
    ("L'énergie et la persistance\nconquièrent toutes choses.", "Benjamin Franklin"),
    ("Le progrès, pas la perfection.", "Anonyme"),
    ("Chaque jour est une nouvelle chance\nde changer ta vie.", "Anonyme"),
    ("La volonté de gagner est importante,\nla volonté de se préparer l'est encore plus.", "Vince Lombardi"),
    ("Un rêve n'est pas quelque chose que tu vois en dormant,\nc'est quelque chose qui ne te laisse pas dormir.", "A.P.J. Abdul Kalam"),
    ("Investis en toi-même.\nTa carrière est le moteur de ta richesse.", "Paul Clitheroe"),
    ("Vis comme si tu mourais demain.\nApprends comme si tu vivais éternellement.", "Gandhi"),
    ("Travaille en silence,\nlaisse le succès faire du bruit.", "Anonyme"),
    ("Ce n'est pas la montagne qui nous épuise,\nc'est le grain de sable dans la chaussure.", "Robert Service"),
    ("Fais aujourd'hui ce que les autres ne veulent pas faire,\nvis demain comme les autres ne peuvent pas.", "Anonyme"),
    ("Sois le changement\nque tu veux voir dans le monde.", "Gandhi"),
    ("La vie est 10% ce qui m'arrive\net 90% comment j'y réagis.", "Charles Swindoll"),
    ("Agis dans l'instant.\nC'est tout ce que tu as.", "Marc Aurèle"),
    ("Le talent ne suffit pas.\nL'habitude construit l'excellence.", "Anonyme"),
    ("Ce que tu répètes chaque jour\nte définit.", "Anonyme"),
]

MOODS = [
    ("", "Motivé"),
    ("", "Calme"),
    ("", "Fatigué"),
    ("", "Stressé"),
    ("", "Neutre"),
]

DAYS_FR    = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MONTHS_FR  = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre"
]

STATUS_COLORS = {
    "planned":   "#4a9eff",
    "completed": "#50c878",
    "cancelled": "#cc4444",
}


# -------------------------------------------------------
# Widget séparateur décoratif
# -------------------------------------------------------
class DividerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(1)
        self.setMinimumWidth(200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), 0)
        grad.setColorAt(0.0, QColor(26, 32, 53, 0))
        grad.setColorAt(0.3, QColor(200, 168, 74, 180))
        grad.setColorAt(0.7, QColor(200, 168, 74, 180))
        grad.setColorAt(1.0, QColor(26, 32, 53, 0))
        painter.fillRect(self.rect(), grad)


# -------------------------------------------------------
# Widget citation avec fade in/out
# -------------------------------------------------------
class QuoteWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)

        # Guillemet décoratif
        self.lbl_open = QLabel("❝")
        self.lbl_open.setAlignment(Qt.AlignCenter)
        self.lbl_open.setStyleSheet("color: #c8a84a; font-size: 36px; background: transparent;")
        layout.addWidget(self.lbl_open)

        # Texte de la citation
        self.lbl_quote = QLabel()
        self.lbl_quote.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_quote.setMinimumHeight(80)
        self.lbl_quote.setAlignment(Qt.AlignCenter)
        self.lbl_quote.setWordWrap(True)
        font_q = QFont("Segoe UI", 17)
        font_q.setItalic(True)
        font_q.setWeight(QFont.Light)
        self.lbl_quote.setFont(font_q)
        self.lbl_quote.setStyleSheet("color: #e8f0ff; background: transparent; line-height: 1.6;")
        layout.addWidget(self.lbl_quote)

        # Auteur
        self.lbl_author = QLabel()
        self.lbl_author.setAlignment(Qt.AlignCenter)
        font_a = QFont("Segoe UI", 11)
        self.lbl_author.setFont(font_a)
        self.lbl_author.setStyleSheet("color: #c8a84a; letter-spacing: 2px; background: transparent;")
        layout.addWidget(self.lbl_author)

        # Effet d'opacité pour le fade
        self._opacity = QGraphicsOpacityEffect(self)
        self._opacity.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity)

        # Animation fade out
        self._anim_out = QPropertyAnimation(self._opacity, b"opacity")
        self._anim_out.setDuration(600)
        self._anim_out.setStartValue(1.0)
        self._anim_out.setEndValue(0.0)
        self._anim_out.setEasingCurve(QEasingCurve.InOutSine)

        # Animation fade in
        self._anim_in = QPropertyAnimation(self._opacity, b"opacity")
        self._anim_in.setDuration(800)
        self._anim_in.setStartValue(0.0)
        self._anim_in.setEndValue(1.0)
        self._anim_in.setEasingCurve(QEasingCurve.InOutSine)

        self._pending_quote  = None
        self._pending_author = None
        self._anim_out.finished.connect(self._apply_and_fade_in)

    def set_quote(self, quote, author, animate=False):
        if animate:
            self._pending_quote  = quote
            self._pending_author = f"— {author} —"
            self._anim_out.start()
        else:
            self.lbl_quote.setText(quote)
            self.lbl_author.setText(f"— {author} —")

    def _apply_and_fade_in(self):
        if self._pending_quote:
            self.lbl_quote.setText(self._pending_quote)
            self.lbl_author.setText(self._pending_author)
            self._pending_quote  = None
            self._pending_author = None
        self._anim_in.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        painter.fillPath(path, QColor(25, 32, 55, 255))
        painter.setPen(QPen(QColor(240, 232, 216, 80), 1))
        painter.drawPath(path)
        super().paintEvent(event)
        


# -------------------------------------------------------
# HomePage
# -------------------------------------------------------
class HomePage(QWidget):
    """
    Page d'accueil INLINE.
    Affiche date, citation animée, mood, focus, events du jour et journaling.
    """

    def __init__(self, intention_service=None, event_service=None,
                 environment_service=None, parent=None):
        super().__init__(parent)
        self.intention_service   = intention_service
        self.event_service       = event_service
        self.environment_service = environment_service
        self.today               = date.today()
        self._selected_mood      = None
        self._mood_buttons       = []
        self._quote_index        = self.today.toordinal() % len(QUOTES)

        self._init_ui()
        self._subscribe()
        self._refresh()

    # -------------------------------------------------------
    # Observer
    # -------------------------------------------------------

    def _subscribe(self):
        if self.intention_service:
            for ev in ("intention_updated", "intention_created", "intention_deleted"):
                self.intention_service.subscribe(ev, lambda _: self._refresh_focus())
        if self.event_service:
            for ev in ("event_created", "event_updated", "event_deleted"):
                self.event_service.subscribe(ev, lambda _: self._refresh_events())

    # -------------------------------------------------------
    # UI
    # -------------------------------------------------------

    def _init_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        main = QVBoxLayout(container)
        main.setContentsMargins(80, 50, 80, 50)
        main.setSpacing(0)

        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        # ---- DATE ----
        self.lbl_date = QLabel()
        self.lbl_date.setAlignment(Qt.AlignCenter)
        font_date = QFont("Segoe UI", 13)
        font_date.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        self.lbl_date.setFont(font_date)
        self.lbl_date.setStyleSheet("color: #8090b0; background: transparent; letter-spacing: 3px;")
        main.addWidget(self.lbl_date)
        main.addSpacing(6)

        # ---- SEPARATION ----
        main.addWidget(DividerWidget())
        main.addSpacing(32)

        # ---- CITATION ----
        self.quote_widget = QuoteWidget()
        main.addWidget(self.quote_widget)
        main.addSpacing(12)

        # Navigation citation
        nav_row = QHBoxLayout()
        nav_row.setAlignment(Qt.AlignCenter)
        nav_row.setSpacing(16)

        btn_prev = QPushButton("←")
        btn_prev.setFixedSize(32, 32)
        btn_prev.setStyleSheet(self._nav_btn_style())
        btn_prev.clicked.connect(self._prev_quote)

        btn_next = QPushButton("→")
        btn_next.setFixedSize(32, 32)
        btn_next.setStyleSheet(self._nav_btn_style())
        btn_next.clicked.connect(self._next_quote)

        nav_row.addWidget(btn_prev)
        nav_row.addWidget(btn_next)
        main.addLayout(nav_row)

        main.addSpacing(40)
        main.addWidget(DividerWidget())
        main.addSpacing(36)

        # ---- MOOD ----
        lbl_mood = QLabel("COMMENT TU TE SENS AUJOURD'HUI")
        lbl_mood.setAlignment(Qt.AlignCenter)
        lbl_mood.setStyleSheet(
            "color: #5a6a8a; font-size: 10px; letter-spacing: 3px; background: transparent;"
        )
        main.addWidget(lbl_mood)
        main.addSpacing(16)

        mood_row = QHBoxLayout()
        mood_row.setAlignment(Qt.AlignCenter)
        mood_row.setSpacing(10)

        for emoji, label in MOODS:
            btn = QPushButton(f"{emoji}\n{label}")
            btn.setFixedSize(86, 72)
            btn.setStyleSheet(self._mood_style_inactive())
            btn.clicked.connect(lambda _, e=emoji, l=label, b=btn: self._select_mood(e, l, b))
            mood_row.addWidget(btn)
            self._mood_buttons.append((emoji, label, btn))

        main.addLayout(mood_row)

        main.addSpacing(40)
        main.addWidget(DividerWidget())
        main.addSpacing(36)

        # ---- FOCUS ----
        lbl_focus_title = QLabel("INTENTION FOCUS")
        lbl_focus_title.setStyleSheet(
            "color: #5a6a8a; font-size: 10px; letter-spacing: 3px; background: transparent;"
        )
        main.addWidget(lbl_focus_title)
        main.addSpacing(12)

        self.focus_frame = QFrame()
        self.focus_frame.setStyleSheet("""
            QFrame {
                background-color: #141828;
                border: 1px solid #252d45;
                border-radius: 8px;
                padding: 4px;
            }
        """)
        focus_layout = QHBoxLayout(self.focus_frame)
        focus_layout.setContentsMargins(20, 16, 20, 16)

        self.lbl_focus_dot = QLabel("★")
        self.lbl_focus_dot.setStyleSheet("color: #c8a84a; font-size: 16px; background: transparent;")
        self.lbl_focus_dot.setFixedWidth(24)

        self.lbl_focus = QLabel("Aucune intention active")
        font_focus = QFont("Segoe UI", 14)
        font_focus.setWeight(QFont.Light)
        self.lbl_focus.setFont(font_focus)
        self.lbl_focus.setStyleSheet("color: #5a6a8a; background: transparent;")

        focus_layout.addWidget(self.lbl_focus_dot)
        focus_layout.addWidget(self.lbl_focus)
        focus_layout.addStretch()
        main.addWidget(self.focus_frame)

        main.addSpacing(40)
        main.addWidget(DividerWidget())
        main.addSpacing(36)

        # ---- EVENTS DU JOUR ----
        lbl_ev_title = QLabel("AU PROGRAMME AUJOURD'HUI")
        lbl_ev_title.setStyleSheet(
            "color: #5a6a8a; font-size: 10px; letter-spacing: 3px; background: transparent;"
        )
        main.addWidget(lbl_ev_title)
        main.addSpacing(14)

        self.events_frame = QFrame()
        self.events_frame.setStyleSheet("""
            QFrame {
                background-color: #141828;
                border: 1px solid #252d45;
                border-radius: 8px;
            }
        """)
        self.events_layout = QVBoxLayout(self.events_frame)
        self.events_layout.setContentsMargins(20, 16, 20, 16)
        self.events_layout.setSpacing(10)
        main.addWidget(self.events_frame)

        main.addSpacing(40)
        main.addWidget(DividerWidget())
        main.addSpacing(36)

        # ---- JOURNALING ----
        lbl_journal = QLabel("MON INTENTION POUR AUJOURD'HUI")
        lbl_journal.setStyleSheet(
            "color: #5a6a8a; font-size: 10px; letter-spacing: 3px; background: transparent;"
        )
        main.addWidget(lbl_journal)
        main.addSpacing(14)

        self.journal_edit = QTextEdit()
        self.journal_edit.setPlaceholderText(
            "Qu'est-ce que tu veux accomplir aujourd'hui ?\nComment tu veux te sentir ce soir ?"
        )
        self.journal_edit.setMinimumHeight(110)
        self.journal_edit.setMaximumHeight(160)
        self.journal_edit.setStyleSheet("""
            QTextEdit {
                background-color: #141828;
                border: 1px solid #252d45;
                border-radius: 8px;
                padding: 14px 18px;
                color: #d0d8e8;
                font-size: 13px;
                font-family: "Segoe UI";
                line-height: 1.6;
            }
            QTextEdit:focus {
                border: 1px solid #c8a84a;
            }
        """)
        main.addWidget(self.journal_edit)
        main.addSpacing(40)
        main.addStretch()

        self.focus_frame.hide()
        self.events_frame.hide()

    # -------------------------------------------------------
    # Styles helpers
    # -------------------------------------------------------

    def _nav_btn_style(self):
        return """
            QPushButton {
                background: transparent;
                border: 1px solid #2a3555;
                border-radius: 16px;
                color: #5a6a8a;
                font-size: 14px;
            }
            QPushButton:hover {
                border: 1px solid #c8a84a;
                color: #c8a84a;
            }
        """

    def _mood_style_inactive(self):
        return """
            QPushButton {
                background-color: #141828;
                border: 1px solid #252d45;
                border-radius: 10px;
                color: #5a6a8a;
                font-size: 11px;
                padding: 4px;
            }
            QPushButton:hover {
                border: 1px solid #4a5a80;
                color: #a0b0cc;
                background-color: #1a2240;
            }
        """

    def _mood_style_active(self):
        return """
            QPushButton {
                background-color: #1e3060;
                border: 2px solid #c8a84a;
                border-radius: 10px;
                color: #e8f0ff;
                font-size: 11px;
                padding: 4px;
            }
        """

    # -------------------------------------------------------
    # Citations navigation
    # -------------------------------------------------------

    def _prev_quote(self):
        self._quote_index = (self._quote_index - 1) % len(QUOTES)
        q, a = QUOTES[self._quote_index]
        self.quote_widget.set_quote(q, a, animate=True)

    def _next_quote(self):
        self._quote_index = (self._quote_index + 1) % len(QUOTES)
        q, a = QUOTES[self._quote_index]
        self.quote_widget.set_quote(q, a, animate=True)

    # -------------------------------------------------------
    # Mood
    # -------------------------------------------------------

    def _select_mood(self, emoji, label, clicked_btn):
        self._selected_mood = (emoji, label)
        for _, _, btn in self._mood_buttons:
            btn.setStyleSheet(self._mood_style_inactive())
        clicked_btn.setStyleSheet(self._mood_style_active())

    # -------------------------------------------------------
    # Refresh
    # -------------------------------------------------------

    def _refresh(self):
        self._refresh_date()
        self._refresh_quote()
        self._refresh_focus()
        self._refresh_events()

    def _refresh_date(self):
        d = self.today
        self.lbl_date.setText(
            f"{DAYS_FR[d.weekday()]}  {d.day}  {MONTHS_FR[d.month - 1]}  {d.year}".upper()
        )

    def _refresh_quote(self):
        q, a = QUOTES[self._quote_index]
        self.quote_widget.set_quote(q, a, animate=False)

    def _refresh_focus(self):
        if not self.intention_service:
            return
        active = self.intention_service.get_active_intention_by_user("1")
        if active:
            self.lbl_focus.setText(active.title)
            self.lbl_focus.setStyleSheet(
                "color: #e8f0ff; font-size: 14px; background: transparent;"
            )
            self.lbl_focus_dot.setStyleSheet(
                "color: #c8a84a; font-size: 16px; background: transparent;"
            )
            self.focus_frame.setStyleSheet("""
                QFrame {
                    background-color: #141828;
                    border: 1px solid #c8a84a;
                    border-radius: 8px;
                }
            """)
        else:
            self.lbl_focus.setText("Aucune intention active")
            self.lbl_focus.setStyleSheet(
                "color: #3a4a6a; font-size: 14px; background: transparent;"
            )
            self.lbl_focus_dot.setStyleSheet(
                "color: #3a4a6a; font-size: 16px; background: transparent;"
            )
            self.focus_frame.setStyleSheet("""
                QFrame {
                    background-color: #141828;
                    border: 1px solid #252d45;
                    border-radius: 8px;
                }
            """)

    def _refresh_events(self):
        while self.events_layout.count():
            item = self.events_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.event_service or not self.environment_service:
            self._add_empty_event_label()
            return

        envs = self.environment_service.get_environments_for_owner("1")
        start = datetime.combine(self.today, datetime.min.time())
        end   = datetime.combine(self.today, datetime.max.time())

        all_events = []
        for env in envs:
            all_events.extend(self.event_service.get_events_between(env.id, start, end))

        all_events.sort(key=lambda e: e.start_time)

        if not all_events:
            self._add_empty_event_label()
            return

        intentions_map = self.intention_service.get_intentions_map() if self.intention_service else {}

        for i, ev in enumerate(all_events):
            intention = intentions_map.get(ev.intention_id)
            name      = intention.title if intention else "Événement"
            color     = STATUS_COLORS.get(ev.status, "#5a6a8a")
            time_str  = ev.start_time.strftime("%H:%M")

            row = QHBoxLayout()
            row.setSpacing(14)

            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 10px; background: transparent;")
            dot.setFixedWidth(12)

            lbl_time = QLabel(time_str)
            lbl_time.setStyleSheet("color: #5a6a8a; font-size: 11px; background: transparent;")
            lbl_time.setFixedWidth(42)

            lbl_sep = QLabel("—")
            lbl_sep.setStyleSheet("color: #2a3555; font-size: 11px; background: transparent;")
            lbl_sep.setFixedWidth(14)

            lbl_name = QLabel(name)
            style_name = (
                "color: #d0d8e8;" if ev.status == "planned"
                else "color: #5a6a8a; text-decoration: line-through;"
                if ev.status == "cancelled"
                else "color: #50c878;"
            )
            lbl_name.setStyleSheet(f"{style_name} font-size: 13px; background: transparent;")

            row.addWidget(dot)
            row.addWidget(lbl_time)
            row.addWidget(lbl_sep)
            row.addWidget(lbl_name)
            row.addStretch()

            wrapper = QWidget()
            wrapper.setStyleSheet("background: transparent;")
            wrapper.setLayout(row)
            self.events_layout.addWidget(wrapper)

            if i < len(all_events) - 1:
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setStyleSheet("color: #1e2840; background: #1e2840;")
                sep.setFixedHeight(1)
                self.events_layout.addWidget(sep)

    def _add_empty_event_label(self):
        lbl = QLabel("Aucun événement planifié aujourd'hui.")
        lbl.setStyleSheet("color: #3a4a6a; font-size: 12px; background: transparent;")
        lbl.setAlignment(Qt.AlignCenter)
        self.events_layout.addWidget(lbl)