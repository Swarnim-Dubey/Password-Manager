from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QFrame, QListWidget,
    QApplication, QHeaderView, QLineEdit,
    QStackedWidget, QInputDialog, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QGuiApplication

from GUI.toggle_switch import ToggleSwitch
from GUI.add_cred import AddCredentialWindow
from GUI.edit_cred import EditCredentialWindow
from Database.db import (
    get_credentials,
    delete_credential,
    get_categories,
    get_username,
    delete_all_user_credentials
)
from Security.auth import authenticate_user, decrypt_data


class VaultWindow(QWidget):

    def __init__(self, user_id, key):
        super().__init__()

        self.user_id = user_id
        self.key = key
        self.credentials = []
        self.setWindowFlags(Qt.Window)
        self.current_theme = "dark"
        self.accent_color = "#238636"

        # ✅ IMPORTANT — Makes it a normal app window (not dialog)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("VaultX")
        self.setMinimumSize(1100, 650)

        self.init_ui()
        self.apply_theme()

        self.load_categories()
        self.load_data()

        # ✅ Opens maximized (taskbar visible)
        self.showMaximized()

    # ================= UI =================

    def filter_by_category(self, item):
        # item is the QListWidgetItem that was clicked
        category = item.text()
        # your logic to filter the vault by category
        print(f"Filtering vault by category: {category}")

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)

        self.sidebar = self.create_sidebar()
        self.main_layout.addWidget(self.sidebar, 1)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack, 4)

        self.vault_page = self.create_vault_page()
        self.stack.addWidget(self.vault_page)

        self.settings_page = self.create_settings_page()
        self.stack.addWidget(self.settings_page)

    # ================= SIDEBAR =================

    def create_sidebar(self):
        sidebar = QFrame()
        layout = QVBoxLayout(sidebar)

        title = QLabel("VaultX")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        self.category_list = QListWidget()
        self.category_list.itemClicked.connect(self.filter_by_category)
        layout.addWidget(self.category_list)

        layout.addStretch()

        self.add_button = QPushButton("Add Credential")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.toggle_settings_page)
        layout.addWidget(self.settings_button)

        username = get_username(self.user_id)
        user_label = QLabel(username)
        user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_label)

        return sidebar

    # ================= VAULT PAGE =================

    def create_vault_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.theme_toggle = ToggleSwitch()
        self.theme_toggle.setChecked(True)
        self.theme_toggle.toggled.connect(self.on_toggle_changed)
        top_bar.addWidget(self.theme_toggle)

        layout.addLayout(top_bar)

        self.action_bar = self.create_action_bar()
        self.action_bar.setMaximumHeight(0)
        layout.addWidget(self.action_bar)

        self.table = self.create_table()
        layout.addWidget(self.table)

        return page

    # ================= SETTINGS PAGE =================

    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        layout.addSpacing(20)

        self.delete_all_btn = QPushButton("Delete All Credentials")
        self.delete_all_btn.clicked.connect(self.delete_all_credentials_from_settings)
        layout.addWidget(self.delete_all_btn)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.back_button = QPushButton("⬅ Back to Vault")
        self.back_button.clicked.connect(self.toggle_settings_page)
        layout.addWidget(self.back_button)

        layout.addStretch()

        return page

    # ================= PAGE SWITCH =================

    def toggle_settings_page(self):
        self.table.clearSelection()
        self.slide_action_bar(False)

        current = self.stack.currentIndex()
        new_index = 1 if current == 0 else 0
        self.fade_transition(new_index)

    def fade_transition(self, new_index):
        current_widget = self.stack.currentWidget()
        next_widget = self.stack.widget(new_index)

        fade_out = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(fade_out)

        self.anim = QPropertyAnimation(fade_out, b"opacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)

        def switch():
            self.stack.setCurrentIndex(new_index)

            fade_in = QGraphicsOpacityEffect(next_widget)
            next_widget.setGraphicsEffect(fade_in)

            self.anim2 = QPropertyAnimation(fade_in, b"opacity")
            self.anim2.setDuration(250)
            self.anim2.setStartValue(0)
            self.anim2.setEndValue(1)
            self.anim2.start()

        self.anim.finished.connect(switch)
        self.anim.start()

    # ================= TABLE =================

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Service", "Username", "Password"])
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        table.itemSelectionChanged.connect(self.handle_selection_change)
        return table

    # ================= ACTION BAR =================

    def create_action_bar(self):
        bar = QFrame()
        layout = QHBoxLayout(bar)

        copy_user = QPushButton("Copy Username")
        copy_pass = QPushButton("Copy Password")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")

        copy_user.clicked.connect(self.copy_username)
        copy_pass.clicked.connect(self.copy_password)
        edit_btn.clicked.connect(self.edit_selected)
        delete_btn.clicked.connect(self.delete_selected)

        layout.addWidget(copy_user)
        layout.addWidget(copy_pass)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addStretch()

        return bar

    def slide_action_bar(self, show=True):
        start_height = self.action_bar.maximumHeight()
        end_height = 60 if show else 0

        self.action_anim = QPropertyAnimation(self.action_bar, b"maximumHeight")
        self.action_anim.setDuration(200)
        self.action_anim.setStartValue(start_height)
        self.action_anim.setEndValue(end_height)
        self.action_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.action_anim.start()

    def handle_selection_change(self):
        if self.table.selectionModel().hasSelection():
            self.slide_action_bar(True)
        else:
            self.slide_action_bar(False)

    # ================= LOGOUT =================

    def logout(self):
        from GUI.login import LoginWindow

        self.login_window = LoginWindow()

        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        self.logout_anim = QPropertyAnimation(effect, b"opacity")
        self.logout_anim.setDuration(300)
        self.logout_anim.setStartValue(1)
        self.logout_anim.setEndValue(0)

        def show_login():
            self.login_window.showMaximized()
            self.close()

        self.logout_anim.finished.connect(show_login)
        self.logout_anim.start()

    # ================= THEME =================

    def on_toggle_changed(self, checked):
        self.current_theme = "dark" if checked else "light"
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == "dark":
            bg = "#0d1117"
            card = "#161b22"
            border = "#30363d"
            text = "#c9d1d9"
        else:
            bg = "#ffffff"
            card = "#f6f8fa"
            border = "#d0d7de"
            text = "#24292f"

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg};
                color: {text};
            }}
            QFrame {{
                background-color: {card};
                border: 1px solid {border};
                border-radius: 8px;
            }}
            QPushButton {{
                background-color: {card};
                border: 1px solid {border};
                padding: 8px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                border: 1px solid {self.accent_color};
            }}
            QTableWidget {{
                background-color: {card};
                border: 1px solid {border};
            }}
            QListWidget {{
                background-color: {card};
                border: 1px solid {border};
            }}
        """)