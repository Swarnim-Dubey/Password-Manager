from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt

from Database.db import update_credential
from Security.auth import decrypt_data, encrypt_data


class EditCredentialWindow(QDialog):
    def __init__(self, app_username, key, credential, parent=None):
        super().__init__(parent)

        self.app_username = app_username
        self.key = key
        self.credential = credential

        self.setWindowTitle("Edit Credential")
        self.setMinimumWidth(400)

        self.init_ui()
        self.load_existing_data()

    # ================= UI =================

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Service
        layout.addWidget(QLabel("Service"))
        self.service_input = QLineEdit()
        layout.addWidget(self.service_input)

        # Username
        layout.addWidget(QLabel("Username"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Category
        layout.addWidget(QLabel("Category"))
        self.category_input = QLineEdit()
        layout.addWidget(self.category_input)

        # Buttons
        btn_layout = QHBoxLayout()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.save_changes)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    # ================= LOAD DATA =================

    def load_existing_data(self):
        self.service_input.setText(self.credential["service"])
        self.username_input.setText(self.credential["username"])

        decrypted_password = decrypt_data(
            self.credential["password"],
            self.key
        )
        self.password_input.setText(decrypted_password)

        self.category_input.setText(self.credential["category"])

    # ================= SAVE =================

    def save_changes(self):
        service = self.service_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        category = self.category_input.text().strip()

        if not service or not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        encrypted_password = encrypt_data(password, self.key)

        update_credential(
            self.credential["id"],
            service,
            username,
            encrypted_password,
            category
        )

        QMessageBox.information(self, "Success", "Credential updated.")
        self.accept()