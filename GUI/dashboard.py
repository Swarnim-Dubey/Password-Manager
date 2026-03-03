from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QFrame, QStackedWidget,
    QLabel, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from GUI.add_cred import AddCredentialWindow
from GUI.view_cred import ViewCredentialWindow
from GUI.login import LoginWindow
from GUI.titlebar import TitleBar


class Dashboard(QWidget):
    def __init__(self, key: bytes):
        super().__init__()

        self.key = key
        self.setWindowTitle("SecureVault Dashboard")

        # ✅ NORMAL WINDOW (TASKBAR VISIBLE)
        self.resize(1200, 800)

        # ================= TITLEBAR =================
        self.titlebar = TitleBar(self)

        # ================= SIDEBAR =================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)

        self.add_btn = QPushButton("Add Credential")
        self.view_btn = QPushButton("View Credentials")
        self.settings_btn = QPushButton("Settings")
        self.logout_btn = QPushButton("Logout")

        self.add_btn.clicked.connect(self.open_add)
        self.view_btn.clicked.connect(self.open_view)
        self.settings_btn.clicked.connect(self.open_settings)
        self.logout_btn.clicked.connect(self.logout)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.addWidget(self.add_btn)
        sidebar_layout.addWidget(self.view_btn)
        sidebar_layout.addWidget(self.settings_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.logout_btn)

        # ================= STACK =================
        self.stack = QStackedWidget()

        self.dashboard_page = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_page)

        self.cred_list = QListWidget()
        dash_layout.addWidget(self.cred_list)

        self.settings_page = self.create_settings_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.settings_page)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        root_layout = QVBoxLayout(self)
        root_layout.addWidget(self.titlebar)
        root_layout.addLayout(main_layout)

        self.auto_lock_timer = QTimer()
        self.auto_lock_timer.timeout.connect(self.auto_lock_trigger)

        self.load_credentials()

        self.showMaximized()

    # ================= SETTINGS PAGE =================
    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.setChecked(True)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_dashboard)

        layout.addWidget(title)
        layout.addWidget(self.dark_mode_checkbox)
        layout.addWidget(back_btn)

        return page

    def open_settings(self):
        self.stack.setCurrentWidget(self.settings_page)

    def go_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)

    def auto_lock_trigger(self):
        QMessageBox.information(self, "Auto Lock", "Session Locked.")
        self.logout()

    def load_credentials(self):
        from Database.db import get_all_credentials
        creds = get_all_credentials(self.key)
        self.cred_list.clear()
        for cred in creds:
            self.cred_list.addItem(f"{cred['username']} | {cred['site']}")

    def open_add(self):
        self.add_window = AddCredentialWindow(self.key)
        self.add_window.show()

    def open_view(self):
        self.view_window = ViewCredentialWindow(self.key)
        self.view_window.show()

    def logout(self):
        self.close()
        self.login = LoginWindow()
        self.login.showMaximized()