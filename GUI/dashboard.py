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
        self.resize(900, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # ================= TITLEBAR =================
        self.titlebar = TitleBar(self)

        # ================= SIDEBAR =================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
            }
            QPushButton {
                background-color: #334155;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)

        self.add_btn = QPushButton("Add Credential")
        self.view_btn = QPushButton("View Credentials")
        self.settings_btn = QPushButton("Settings")
        self.logout_btn = QPushButton("Logout")

        self.add_btn.clicked.connect(self.open_add)
        self.view_btn.clicked.connect(self.open_view)
        self.settings_btn.clicked.connect(self.open_settings)
        self.logout_btn.clicked.connect(self.logout)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 30, 15, 15)
        sidebar_layout.setSpacing(15)
        sidebar_layout.addWidget(self.add_btn)
        sidebar_layout.addWidget(self.view_btn)
        sidebar_layout.addWidget(self.settings_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.logout_btn)

        # ================= STACKED CONTENT =================
        self.stack = QStackedWidget()

        # Main dashboard page
        self.dashboard_page = QWidget()
        dash_layout = QVBoxLayout(self.dashboard_page)
        dash_layout.setContentsMargins(20, 20, 20, 20)

        self.cred_list = QListWidget()
        self.cred_list.setStyleSheet("""
            QListWidget {
                background-color: #111827;
                color: #E5E7EB;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
            }
            QListWidget::item:selected {
                background-color: #2563EB;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #1F2937;
            }
        """)

        dash_layout.addWidget(self.cred_list)

        # Settings page
        self.settings_page = self.create_settings_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.settings_page)

        # ================= MAIN LAYOUT =================
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.titlebar)
        root_layout.addLayout(main_layout)

        # Auto Lock Timer
        self.auto_lock_timer = QTimer()
        self.auto_lock_timer.timeout.connect(self.auto_lock_trigger)

        # Load credentials
        self.load_credentials()

    # ================= SETTINGS UI =================
    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(80, 40, 80, 40)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(500)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 15px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(25)
        card_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white;")
        card_layout.addWidget(title)

        # Dark Mode
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.setChecked(True)
        self.dark_mode_checkbox.setStyleSheet("color: white; font-size: 14px;")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        card_layout.addWidget(self.dark_mode_checkbox)

        # Auto Lock
        self.auto_lock_checkbox = QCheckBox("Enable Auto Lock (30 seconds)")
        self.auto_lock_checkbox.setStyleSheet("color: white; font-size: 14px;")
        self.auto_lock_checkbox.stateChanged.connect(self.toggle_auto_lock)
        card_layout.addWidget(self.auto_lock_checkbox)

        # Delete All
        delete_btn = QPushButton("Delete All Credentials")
        delete_btn.setStyleSheet(self.red_button())
        delete_btn.clicked.connect(self.delete_all_credentials)
        card_layout.addWidget(delete_btn)

        # Back Button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet(self.gray_button())
        back_btn.clicked.connect(self.go_dashboard)
        card_layout.addWidget(back_btn)

        layout.addWidget(card)

        return page

    # ================= BUTTON STYLES =================
    def red_button(self):
        return """
            QPushButton {
                background-color: #c0392b;
                color: white;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """

    def gray_button(self):
        return """
            QPushButton {
                background-color: #555;
                color: white;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """

    # ================= NAVIGATION =================
    def open_settings(self):
        self.stack.setCurrentWidget(self.settings_page)

    def go_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)

    # ================= FUNCTIONALITY =================
    def toggle_dark_mode(self):
        if self.dark_mode_checkbox.isChecked():
            self.setStyleSheet("")
        else:
            self.setStyleSheet("background-color: white; color: black;")

    def toggle_auto_lock(self):
        if self.auto_lock_checkbox.isChecked():
            self.auto_lock_timer.start(30000)
        else:
            self.auto_lock_timer.stop()

    def auto_lock_trigger(self):
        QMessageBox.information(self, "Auto Lock", "Session Locked.")
        self.logout()

    def delete_all_credentials(self):
        from Database.db import delete_all_credentials

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete ALL saved credentials?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_all_credentials()
            self.load_credentials()
            QMessageBox.information(self, "Deleted", "All credentials removed.")

    # ================= EXISTING FEATURES =================
    def load_credentials(self):
        from Database.db import get_all_credentials
        creds = get_all_credentials(self.key)
        self.cred_list.clear()
        for cred in creds:
            self.cred_list.addItem(f"{cred['username']} | {cred['site']}")

    def open_add(self):
        self.add_window = AddCredentialWindow(self.key)
        self.add_window.credential_added.connect(self.add_credential_to_list)
        self.add_window.show()

    def add_credential_to_list(self, credential: dict):
        self.cred_list.addItem(f"{credential['username']} | {credential['site']}")

    def open_view(self):
        self.view_window = ViewCredentialWindow(self.key)
        self.view_window.show()

    def logout(self):
        self.close()
        self.login = LoginWindow()
        self.login.show()