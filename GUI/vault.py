from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QFrame, QListWidget,
    QHeaderView, QStackedWidget, QGraphicsOpacityEffect
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
from Security.auth import decrypt_data


class VaultWindow(QWidget):

    def __init__(self, user_id, key):
        super().__init__()

        self.user_id = user_id
        self.key = key
        self.credentials = []
        self.current_theme = "dark"
        self.accent_color = "#238636"

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("VaultX")
        self.setMinimumSize(1100, 650)

        self.init_ui()
        self.apply_theme()

        self.load_categories()
        self.load_data()

        self.showMaximized()
        # print("Vault key:", self.key)

    # ================= UI =================

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

    # ================= ADD =================

    def open_add_dialog(self):
        dialog = AddCredentialWindow(self.user_id, self.key)
        dialog.exec()
        self.load_data()
        self.load_categories()

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

    # ================= TABLE =================

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Website", "Username", "Password"])

        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Center align headers
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        table.itemSelectionChanged.connect(self.handle_selection_change)

        return table

    # ================= LOAD DATA =================

    def load_data(self):
        self.credentials = get_credentials(self.user_id)

        self.table.setRowCount(0)

        if not self.credentials:
            return

        self.table.setRowCount(len(self.credentials))

        for row, cred in enumerate(self.credentials):
            try:
                cred_id = cred["id"]
                website = cred["website"]
                encrypted_username = cred["email"]
                encrypted_password = cred["password"]

                try:
                    username = decrypt_data(encrypted_username, self.key)
                except Exception:
                    username = encrypted_username

                try:
                    password = decrypt_data(encrypted_password, self.key)
                except Exception:
                    password = encrypted_password

                # Mask password
                masked_password = "•" * len(password)

                website_item = QTableWidgetItem(str(website))
                username_item = QTableWidgetItem(str(username))
                password_item = QTableWidgetItem(masked_password)

                # Center alignment
                website_item.setTextAlignment(Qt.AlignCenter)
                username_item.setTextAlignment(Qt.AlignCenter)
                password_item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row, 0, website_item)
                self.table.setItem(row, 1, username_item)
                self.table.setItem(row, 2, password_item)

            except Exception as e:
                print("Error loading credential:", e)

    def load_categories(self):
        self.category_list.clear()
        categories = get_categories(self.user_id)
        for cat in categories:
            self.category_list.addItem(cat)

    # ================= ACTIONS =================

    def copy_username(self):
        row = self.table.currentRow()
        if row >= 0:
            QGuiApplication.clipboard().setText(
                self.table.item(row, 1).text()
            )

    def copy_password(self):
        row = self.table.currentRow()
        if row >= 0:
            QGuiApplication.clipboard().setText(
                self.table.item(row, 2).text()
            )

    def edit_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        cred_id = self.credentials[row]["id"]

        dialog = EditCredentialWindow(cred_id, self.user_id, self.key)
        dialog.exec()

        self.load_data()

        cred_id = self.credentials[row][0]
        dialog = EditCredentialWindow(cred_id, self.user_id, self.key)
        dialog.exec()
        self.load_data()

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        reply = QMessageBox.question(
            self,
            "⚠️ Delete ⚠️",
            "Are you sure you want to delete this credential?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            cred_id = self.credentials[row]["id"]
            delete_credential(cred_id)
            self.load_data()

    def delete_all_credentials_from_settings(self):
        reply = QMessageBox.warning(
            self,
            "Delete All",
            "This will permanently delete ALL credentials.\nContinue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            delete_all_user_credentials(self.user_id)
            self.load_data()
            self.load_categories()

    # ================= FILTER =================

    def filter_by_category(self, item):
        category = item.text()

        # Fetch filtered credentials
        self.credentials = get_credentials(self.user_id, category)

        self.table.setRowCount(0)

        if not self.credentials:
            return

        self.table.setRowCount(len(self.credentials))

        for row, cred in enumerate(self.credentials):
            try:
                website = cred["website"]
                encrypted_username = cred["email"]
                encrypted_password = cred["password"]

                try:
                    username = decrypt_data(encrypted_username, self.key)
                except Exception:
                    username = encrypted_username

                try:
                    password = decrypt_data(encrypted_password, self.key)
                except Exception:
                    password = encrypted_password

                masked_password = "•" * len(password)

                website_item = QTableWidgetItem(website)
                username_item = QTableWidgetItem(username)
                password_item = QTableWidgetItem(masked_password)

                website_item.setTextAlignment(Qt.AlignCenter)
                username_item.setTextAlignment(Qt.AlignCenter)
                password_item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row, 0, website_item)
                self.table.setItem(row, 1, username_item)
                self.table.setItem(row, 2, password_item)

            except Exception as e:
                print("Error loading filtered credential:", e)

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

    def handle_selection_change(self):
        if self.table.selectionModel().hasSelection():
            self.slide_action_bar(True)
        else:
            self.slide_action_bar(False)

    def slide_action_bar(self, show=True):
        start_height = self.action_bar.maximumHeight()
        end_height = 60 if show else 0

        self.action_anim = QPropertyAnimation(self.action_bar, b"maximumHeight")
        self.action_anim.setDuration(200)
        self.action_anim.setStartValue(start_height)
        self.action_anim.setEndValue(end_height)
        self.action_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.action_anim.start()

    # ================= PAGE SWITCH =================

    def toggle_settings_page(self):
        current = self.stack.currentIndex()
        self.stack.setCurrentIndex(1 if current == 0 else 0)

    # ================= LOGOUT =================

    def logout(self):
        from GUI.login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()

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
            header = "#21262d"
        else:
            bg = "#ffffff"
            card = "#f6f8fa"
            border = "#d0d7de"
            text = "#000000"
            header = "#eaeef2"

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
                color: {text};
            }}

            QPushButton:hover {{
                border: 1px solid {self.accent_color};
            }}

            QTableWidget {{
                background-color: {card};
                border: 1px solid {border};
                gridline-color: {border};
                color: {text};
            }}

            QHeaderView::section {{
                background-color: {header};
                border: 1px solid {border};
                padding: 6px;
                color: {text};
            }}

            QListWidget {{
                background-color: {card};
                border: 1px solid {border};
                color: {text};
            }}
        """)
    
        # print("Vault key:", self.key)