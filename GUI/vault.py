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

        self.current_theme = "dark"
        self.accent_color = "#238636"

        self.setWindowTitle("VaultX")
        self.setMinimumSize(1100, 650)

        self.init_ui()
        self.apply_theme()

        self.load_categories()
        self.load_data()

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
        self.anim.setDuration(200)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)

        def switch():
            self.stack.setCurrentIndex(new_index)

            fade_in = QGraphicsOpacityEffect(next_widget)
            next_widget.setGraphicsEffect(fade_in)

            self.anim2 = QPropertyAnimation(fade_in, b"opacity")
            self.anim2.setDuration(200)
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

    # ================= ADD =================

    def open_add_dialog(self):
        self.add_window = AddCredentialWindow(
            self.user_id,
            self.key,
            theme=self.current_theme
        )
        self.add_window.credential_added.connect(self.refresh_after_add)
        self.add_window.exec()

    def refresh_after_add(self):
        self.load_categories()
        self.load_data()

    # ================= DATA =================

    def load_categories(self):
        self.category_list.clear()
        categories = get_categories(self.user_id)
        self.category_list.addItems(categories)

    def load_data(self, category=None):
        self.credentials = get_credentials(self.user_id, category)
        self.table.setRowCount(len(self.credentials))

        for row, cred in enumerate(self.credentials):
            cred_id, website, email, password, category = cred

            service_item = QTableWidgetItem(website)
            username_item = QTableWidgetItem(email)
            password_item = QTableWidgetItem("•••••••")

            service_item.setTextAlignment(Qt.AlignCenter)
            username_item.setTextAlignment(Qt.AlignCenter)
            password_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, service_item)
            self.table.setItem(row, 1, username_item)
            self.table.setItem(row, 2, password_item)

    def filter_by_category(self, item):
        self.load_data(item.text())

    # ================= COPY =================

    def copy_username(self):
        row = self.table.currentRow()
        if row >= 0:
            QApplication.clipboard().setText(self.credentials[row][2])

    def copy_password(self):
        row = self.table.currentRow()
        if row >= 0:
            encrypted_password = self.credentials[row][3]
            decrypted = decrypt_data(encrypted_password, self.key)
            QGuiApplication.clipboard().setText(decrypted)
            QMessageBox.information(self, "Copied", "Password copied to clipboard!")

    # ================= DELETE =================

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this credential?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        cred_id = self.credentials[row][0]
        delete_credential(cred_id)

        self.load_categories()
        self.load_data()

    def delete_all_credentials_from_settings(self):
        confirm = QMessageBox.question(
            self,
            "Warning",
            "You are about to delete ALL credentials.\nAre you sure?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        password, ok = QInputDialog.getText(
            self,
            "Master Password Required",
            "Enter your master password:",
            QLineEdit.Password
        )

        if not ok:
            return

        username = get_username(self.user_id)
        auth = authenticate_user(username, password)

        if auth:
            delete_all_user_credentials(self.user_id)
            self.load_categories()
            self.load_data()
            QMessageBox.information(self, "Deleted", "All credentials deleted.")
        else:
            QMessageBox.warning(self, "Error", "Incorrect master password.")

    # ================= EDIT =================

    def edit_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        cred_id, service, username, password, category = self.credentials[row]

        credential_dict = {
            "id": cred_id,
            "service": service,
            "username": username,
            "password": password,
            "category": category
        }

        app_username = get_username(self.user_id)

        dialog = EditCredentialWindow(
            app_username,
            self.key,
            credential_dict,
            parent=self
        )

        if dialog.exec():
            self.load_categories()
            self.load_data()

    # ================= LOGOUT =================

    def logout(self):
        self.close()
        from GUI.login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

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