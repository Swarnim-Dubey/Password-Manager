from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QFrame
from PySide6.QtCore import Qt, Signal
from GUI.add_cred import AddCredentialWindow
from GUI.view_cred import ViewCredentialWindow
from GUI.login import LoginWindow
from GUI.titlebar import TitleBar


class Dashboard(QWidget):
    def __init__(self, key: bytes):
        super().__init__()

        self.key = key
        self.resize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Titlebar
        self.titlebar = TitleBar(self)

        # Sidebar (left panel)
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(160)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
            }
        """)

        self.add_btn = QPushButton("Add Credential")
        self.view_btn = QPushButton("View Credentials")
        self.logout_btn = QPushButton("Logout")

        self.add_btn.clicked.connect(self.open_add)
        self.view_btn.clicked.connect(self.open_view)
        self.logout_btn.clicked.connect(self.logout)

        # Sidebar layout
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 10)
        sidebar_layout.setSpacing(15)
        sidebar_layout.addWidget(self.add_btn)
        sidebar_layout.addWidget(self.view_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.logout_btn)

        # Credential list (main area)
        self.cred_list = QListWidget()
        self.cred_list.setStyleSheet("""
            QListWidget {
                background-color: #111827;
                color: #E5E7EB;
                border-radius: 6px;
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

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.cred_list)

        # Root layout
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.titlebar)
        root_layout.addLayout(main_layout)

        # Load existing credentials
        self.load_credentials()

    def load_credentials(self):
        from GUI.db import get_all_credentials  # adjust your db method
        creds = get_all_credentials(self.key)
        self.cred_list.clear()
        for cred in creds:
            self.cred_list.addItem(f"{cred['username']} | {cred['site']}")

    def open_add(self):
        self.add_window = AddCredentialWindow(self.key)
        # Connect signal from AddCredentialWindow to update the list
        self.add_window.credential_added.connect(self.add_credential_to_list)
        self.add_window.show()

    def add_credential_to_list(self, credential: dict):
        """Add a single credential to the list in real-time."""
        self.cred_list.addItem(f"{credential['username']} | {credential['site']}")

    def open_view(self):
        self.view_window = ViewCredentialWindow(self.key)
        self.view_window.show()

    def logout(self):
        self.close()
        self.login = LoginWindow()
        self.login.show()