from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt

from Security.auth import encrypt_data
from Database.db import add_credential, update_credential


# =========================
# 🎨 LIGHT THEME
# =========================
LIGHT_THEME = """
QDialog {
    background-color: #f6f8fa;
}

QLabel {
    font-size: 14px;
    font-weight: 600;
    color: #24292f;
}

QLineEdit, QComboBox {
    background-color: white;
    border: 1px solid #d0d7de;
    padding: 6px;
    border-radius: 6px;
    font-size: 14px;
    color: #24292f;
}

QPushButton {
    background-color: #2da44e;
    color: white;
    padding: 8px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2c974b;
}
"""


# =========================
# 🌑 GITHUB DARK THEME
# =========================
DARK_THEME = """
QDialog {
    background-color: #0d1117;
}

QLabel {
    font-size: 14px;
    font-weight: 600;
    color: #c9d1d9;
}

QLineEdit, QComboBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    padding: 6px;
    border-radius: 6px;
    font-size: 14px;
    color: #c9d1d9;
}

QPushButton {
    background-color: #30363d;
    color: #c9d1d9;
    padding: 8px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #484f58;
}
"""


class AddCredentialWindow(QDialog):
    def __init__(self, user_id, key, parent=None, cred=None, theme="light"):
        super().__init__(parent)

        self.user_id = user_id
        self.key = key
        self.cred = cred
        self.theme = theme

        self.setWindowTitle("Add Credential" if not cred else "Edit Credential")
        self.setMinimumWidth(420)

        self.init_ui()
        self.apply_theme()

        # Prefill if editing
        if self.cred:
            self.website_input.setText(self.cred[1])
            self.email_input.setText(self.cred[2])
            self.password_input.setText(self.cred[3])
            self.category_input.setCurrentText(self.cred[4])

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Website
        layout.addWidget(QLabel("Website"))
        self.website_input = QLineEdit()
        layout.addWidget(self.website_input)

        # Email / Username
        layout.addWidget(QLabel("Email / Username"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        # Password
        layout.addWidget(QLabel("Password"))
        self.password_input = QLineEdit()
        layout.addWidget(self.password_input)

        # Category
        layout.addWidget(QLabel("Category"))
        self.category_input = QComboBox()
        self.category_input.addItems(
            ["Social", "Work", "Finance", "Shopping", "Other"]
        )
        layout.addWidget(self.category_input)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_credential)
        layout.addWidget(self.save_button)

    def save_credential(self):
        website = self.website_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        category = self.category_input.currentText()

        if not website or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        # Encrypt password before storing
        encrypted_password = encrypt_data(password, self.key)

        try:
            if self.cred:
                update_credential(
                    self.cred[0],
                    website,
                    email,
                    encrypted_password,
                    category
                )
            else:
                add_credential(
                    self.user_id,
                    website,
                    email,
                    encrypted_password,
                    category
                )

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save credential:\n{str(e)}")

    def apply_theme(self):
        if self.theme == "light":
            self.setStyleSheet(LIGHT_THEME)
        else:
            self.setStyleSheet(DARK_THEME)