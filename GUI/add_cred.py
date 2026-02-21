from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from Security.auth import encrypt_data
from Database.db import add_credential


class AddCredentialWindow(QDialog):
    def __init__(self, app_username, key, parent=None):
        super().__init__(parent)
        self.app_username = app_username
        self.key = key

        self.setWindowTitle("Add Credential")
        self.setFixedSize(400, 420)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Service Name")
        self.service_input.setFixedHeight(40)
        layout.addWidget(QLabel("Service"))
        layout.addWidget(self.service_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)

        # ---------- Category ----------
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Social", "Email", "Bank", "Work", "Other"])
        self.category_combo.setFixedHeight(35)
        self.category_combo.currentTextChanged.connect(self.toggle_custom_category)
        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_combo)

        self.custom_category_input = QLineEdit()
        self.custom_category_input.setPlaceholderText("Enter custom category")
        self.custom_category_input.setFixedHeight(40)
        self.custom_category_input.hide()
        layout.addWidget(self.custom_category_input)

        save_button = QPushButton("Save Credential")
        save_button.setFixedHeight(45)
        save_button.clicked.connect(self.save_credential)
        layout.addWidget(save_button)

    def toggle_custom_category(self, text):
        self.custom_category_input.setVisible(text == "Other")

    def save_credential(self):
        service = self.service_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if self.category_combo.currentText() == "Other":
            category = self.custom_category_input.text().strip()
        else:
            category = self.category_combo.currentText()

        if not service or not username or not password or not category:
            QMessageBox.warning(self, "Error", "All fields must be filled")
            return

        encrypted = encrypt_data(password, self.key)

        add_credential(
            self.app_username,
            service,
            username,
            encrypted,
            category
        )

        QMessageBox.information(self, "Success", f"Credential for '{service}' added.")
        self.accept()