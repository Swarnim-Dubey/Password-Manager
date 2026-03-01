from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from Security.auth import encrypt_data
from Database.db import add_credential, update_credential, get_categories


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
# 🌑 DARK THEME
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
    credential_added = Signal()

    def __init__(self, user_id, key, parent=None, cred=None, theme="dark"):
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
            self.password_input.setText(self.cred[3])  # assuming decrypted before passing
            self.category_combo.setCurrentText(self.cred[4])

    # =========================
    # UI
    # =========================
    def init_ui(self):
        layout = QVBoxLayout(self)

        # Website
        layout.addWidget(QLabel("Website"))
        self.website_input = QLineEdit()
        layout.addWidget(self.website_input)

        # Email
        layout.addWidget(QLabel("Email / Username"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        # Password
        layout.addWidget(QLabel("Password"))

        password_layout = QHBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")

        self.eye_button = QPushButton("👁")
        self.eye_button.setFixedWidth(40)
        self.eye_button.setCheckable(True)
        self.eye_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.eye_button)

        layout.addLayout(password_layout)

        # Category
        layout.addWidget(QLabel("Category"))

        self.category_combo = QComboBox()
        self.load_categories()
        layout.addWidget(self.category_combo)

        # Custom Category Input
        self.custom_category_input = QLineEdit()
        self.custom_category_input.setPlaceholderText("Enter new category")
        self.custom_category_input.hide()
        layout.addWidget(self.custom_category_input)

        self.category_combo.currentTextChanged.connect(self.toggle_custom_category)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_credential)
        layout.addWidget(self.save_button)

    # =========================
    # CATEGORY HANDLING
    # =========================
    def load_categories(self):
        categories = get_categories(self.user_id)

        if not categories:
            categories = ["Social", "Work", "Finance", "Shopping"]

        self.category_combo.clear()
        self.category_combo.addItems(categories)
        self.category_combo.addItem("Other")

    def toggle_custom_category(self, text):
        if text == "Other":
            self.custom_category_input.show()
        else:
            self.custom_category_input.hide()

    # =========================
    # PASSWORD VISIBILITY
    # =========================
    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.eye_button.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.eye_button.setText("👁")

    # =========================
    # SAVE LOGIC
    # =========================
    def save_credential(self):
        website = self.website_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        category = self.category_combo.currentText()

        # Handle custom category
        if category == "Other":
            category = self.custom_category_input.text().strip()
            if not category:
                QMessageBox.warning(self, "Error", "Please enter category name.")
                return

            # Add new category to dropdown immediately
            self.category_combo.insertItem(
                self.category_combo.count() - 1, category
            )
            self.category_combo.setCurrentText(category)

        if not website or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

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

            self.credential_added.emit()
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save credential:\n{str(e)}")

    # =========================
    # THEME
    # =========================
    def apply_theme(self):
        if self.theme == "light":
            self.setStyleSheet(LIGHT_THEME)
        else:
            self.setStyleSheet(DARK_THEME)

    # Allow live theme update
    def update_theme(self, theme):
        self.theme = theme
        self.apply_theme()