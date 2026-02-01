from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt

from GUI.vault import VaultWindow
from Security.auth import hash_password, verify_password, derive_key
from Database.db import get_master_password_hash, set_master_password_hash


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setFixedSize(520, 300)
        self.build_ui()

    # ---------- LOGIC (UNCHANGED) ----------
    def unlock_vault(self):
        master_password = self.password_input.text().strip()

        if not master_password:
            QMessageBox.warning(self, "Error", "Please enter the master password.")
            return

        try:
            stored_hash = get_master_password_hash()

            # First-time setup
            if stored_hash is None:
                password_hash = hash_password(master_password)
                set_master_password_hash(password_hash)

                QMessageBox.information(
                    self,
                    "Success",
                    "Master password created.\nPlease restart the app and login."
                )
                self.password_input.clear()
                return

            # Verify password
            if not verify_password(master_password, stored_hash):
                QMessageBox.critical(self, "Error", "Incorrect master password.")
                return

            # Correct password → derive key & open vault
            key = derive_key(master_password)
            self.vault = VaultWindow(key)
            self.vault.show()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ---------- FORGOT PASSWORD (PLACEHOLDER) ----------
    def forgot_password(self):
        QMessageBox.information(
            self,
            "Forgot Password",
            "Password recovery will be added in future updates."
        )

    # ---------- UI ----------
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(440)
        card.setStyleSheet("""
            QFrame {
                background-color: #0F0F0F;
                border-radius: 16px;
                border: 1px solid #1F1F1F;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(18)

        title = QLabel("🔐 Password Manager")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 22px;
                font-weight: 700;
            }
        """)

        subtitle = QLabel("Unlock your vault")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #A0A0A0;
                font-size: 13px;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Master Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(44)
        self.password_input.returnPressed.connect(self.unlock_vault)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #151515;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #2A2A2A;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3A86FF;
            }
        """)

        unlock_btn = QPushButton("Unlock")
        unlock_btn.setFixedHeight(44)
        unlock_btn.setCursor(Qt.PointingHandCursor)
        unlock_btn.clicked.connect(self.unlock_vault)
        unlock_btn.setStyleSheet("""
            QPushButton {
                background-color: #3A86FF;
                color: white;
                border-radius: 12px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5A9BFF;
            }
        """)

        forgot_btn = QPushButton("Forgot password?")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.clicked.connect(self.forgot_password)
        forgot_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #8AB4FF;
                font-size: 12px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(12)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(10)
        card_layout.addWidget(unlock_btn)
        card_layout.addWidget(forgot_btn, alignment=Qt.AlignCenter)

        root.addWidget(card)

        self.setStyleSheet("""
            QWidget {
                background-color: #0B0B0B;
            }
        """)
