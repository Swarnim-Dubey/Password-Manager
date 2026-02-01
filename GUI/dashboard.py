from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from GUI.add_cred import AddCredentialWindow
from GUI.view_cred import ViewCredentialWindow


class Dashboard(QWidget):
    def __init__(self, key: bytes):
        super().__init__()
        self.key = key

        self.setWindowTitle("Password Manager")
        self.setFixedSize(250, 200)

        self.add_btn = QPushButton("Add Credential")
        self.view_btn = QPushButton("View Credentials")
        self.exit_btn = QPushButton("Exit")

        self.add_btn.clicked.connect(self.open_add)
        self.view_btn.clicked.connect(self.open_view)
        self.exit_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.add_btn)
        layout.addWidget(self.view_btn)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

    def open_add(self):
        self.add_window = AddCredentialWindow(self.key)
        self.add_window.show()

    def open_view(self):
        self.view_window = ViewCredentialWindow(self.key)
        self.view_window.show()
