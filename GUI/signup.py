from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QMessageBox
)
from PySide6.QtCore import Qt

from Database.db import create_user


class SignupWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.setWindowTitle("Create Account")
        self.setFixedSize(420, 520)

        self.setStyleSheet("""
            QWidget {
                background-color: #0d1117;
                font-family: "Segoe UI";
                font-size: 14px;
                color: #c9d1d9;
            }

            QFrame#card {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 24px;
            }

            QLineEdit {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px;
                color: #c9d1d9;
            }

            QLineEdit:focus {
                border: 1px solid #58a6ff;
            }

            QPushButton#primary {
                background-color: #238636;
                color: white;
                border-radius: 6px;
                padding: 8px;
                font-weight: 600;
            }

            QPushButton#primary:hover {
                background-color: #2ea043;
            }

            QPushButton#secondary {
                background: none;
                border: none;
                color: #58a6ff;
            }
        """)

        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setSpacing(12)

        title = QLabel("Create New Account")
        title.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)

        create_btn = QPushButton("Create Account")
        create_btn.setObjectName("primary")
        create_btn.clicked.connect(self.create_account)

        back_btn = QPushButton("Back to Login")
        back_btn.setObjectName("secondary")
        back_btn.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_input)
        layout.addWidget(create_btn)
        layout.addWidget(back_btn)

        root.addWidget(card)

    # -------- CREATE ACCOUNT --------
    def create_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        success = create_user(username, password)

        if not success:
            QMessageBox.warning(self, "Error", "Username already exists.")
            return

        QMessageBox.information(self, "Success", "Account created successfully!")

        # Autofill login window
        self.login_window.username_input.setText(username)
        self.login_window.password_input.setText(password)

        self.close()