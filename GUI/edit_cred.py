from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from Database.db import get_credentials, update_credential, get_categories
from Security.auth import decrypt_data, encrypt_data


class EditCredentialWindow(QDialog):
    def __init__(self, cred_id, user_id, key):
        super().__init__()

        self.cred_id = cred_id
        self.user_id = user_id
        self.key = key
        self.credential = None

        self.setWindowTitle("Edit Credential")
        self.setFixedSize(400, 420)

        self.setStyleSheet("""
            QDialog {
                background-color: #0d1117;
                color: #c9d1d9;
                font-family: Segoe UI;
            }

            QLabel {
                font-size: 13px;
            }

            QLineEdit, QComboBox {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 6px;
                color: white;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #58a6ff;
            }

            QPushButton {
                padding: 8px;
                border-radius: 6px;
            }

            QPushButton#save {
                background-color: #238636;
                color: white;
                font-weight: bold;
            }

            QPushButton#save:hover {
                background-color: #2ea043;
            }

            QPushButton#cancel {
                background-color: transparent;
                color: #58a6ff;
            }
        """)

        self.init_ui()
        self.load_existing_data()

    # ================= UI =================

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Service
        layout.addWidget(QLabel("Service"))
        self.service_input = QLineEdit()
        layout.addWidget(self.service_input)

        # Username
        layout.addWidget(QLabel("Username / Email"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Category Dropdown
        layout.addWidget(QLabel("Category"))
        self.category_dropdown = QComboBox()
        layout.addWidget(self.category_dropdown)

        # Buttons
        btn_layout = QHBoxLayout()

        save_btn = QPushButton("Save Changes")
        save_btn.setObjectName("save")

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel")

        save_btn.clicked.connect(self.save_changes)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    # ================= LOAD DATA =================

    def load_existing_data(self):
        credentials = get_credentials(self.user_id)

        for cred in credentials:
            if cred["id"] == self.cred_id:
                self.credential = cred
                break

        if not self.credential:
            return

        # Fill fields
        self.service_input.setText(self.credential["website"])

        decrypted_username = decrypt_data(self.credential["email"], self.key)
        decrypted_password = decrypt_data(self.credential["password"], self.key)

        self.username_input.setText(decrypted_username)
        self.password_input.setText(decrypted_password)

        # Load categories
        categories = get_categories(self.user_id)
        self.category_dropdown.addItems(categories)

        current_category = self.credential["category"]

        # Set current category as selected
        index = self.category_dropdown.findText(current_category)
        if index >= 0:
            self.category_dropdown.setCurrentIndex(index)
        else:
            # If custom category not in list
            self.category_dropdown.addItem(current_category)
            self.category_dropdown.setCurrentText(current_category)

    # ================= SAVE =================

    def save_changes(self):
        service = self.service_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        category = self.category_dropdown.currentText().strip()

        if not service or not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        encrypted_username = encrypt_data(username, self.key)
        encrypted_password = encrypt_data(password, self.key)

        update_credential(
            self.credential["id"],
            service,
            encrypted_username,
            encrypted_password,
            category
        )

        QMessageBox.information(self, "Success", "Credential updated successfully!")
        self.accept()