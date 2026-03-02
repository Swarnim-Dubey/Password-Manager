from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QPushButton, QCheckBox,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt

from Database.db import delete_all_credentials


class SettingsWindow(QDialog):
    def __init__(self, user_id, current_theme="dark", parent=None):
        super().__init__(parent)

        self.user_id = user_id
        self.current_theme = current_theme
        self.auto_lock_enabled = False

        self.setWindowTitle("Settings")
        self.setMinimumWidth(420)

        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # ---------------- APPEARANCE ----------------
        layout.addWidget(QLabel("Appearance"))

        self.theme_toggle = QCheckBox("Enable Dark Mode")
        self.theme_toggle.setChecked(self.current_theme == "dark")
        layout.addWidget(self.theme_toggle)

        layout.addWidget(self.separator())

        # ---------------- SECURITY ----------------
        layout.addWidget(QLabel("Security"))

        self.auto_lock = QCheckBox("Enable Auto Lock (30 seconds)")
        self.auto_lock.stateChanged.connect(self.toggle_auto_lock)
        layout.addWidget(self.auto_lock)

        layout.addWidget(self.separator())

        # ---------------- DATA ----------------
        layout.addWidget(QLabel("Data Management"))

        self.clear_data_btn = QPushButton("Delete All Credentials")
        self.clear_data_btn.clicked.connect(self.clear_all_credentials)
        layout.addWidget(self.clear_data_btn)

        layout.addWidget(self.separator())

        # ---------------- ACCOUNT ----------------
        layout.addWidget(QLabel("Account"))

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        layout.addWidget(self.logout_btn)

        layout.addWidget(self.separator())

        # ---------------- NAVIGATION ----------------
        self.back_btn = QPushButton("⬅ Back to Vault")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        layout.addWidget(self.separator())

        # ---------------- ABOUT ----------------
        layout.addWidget(QLabel("About"))

        info = QLabel("VaultX v1.0\nSecure • Local • Encrypted")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

    def separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        return line

    # ================= FUNCTIONAL PART =================

    def toggle_auto_lock(self, state):
        self.auto_lock_enabled = state == Qt.Checked

    def clear_all_credentials(self):
        confirm = QMessageBox.question(
            self,
            "Confirm",
            "Are you sure you want to delete ALL credentials?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_all_credentials(self.user_id)
            QMessageBox.information(self, "Success", "All credentials deleted.")

    def logout(self):
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.accept()  # closes dialog and returns control

    def go_back(self):
        self.reject()  # closes settings and returns to vault

    def apply_theme(self):
        if self.current_theme == "dark":
            self.setStyleSheet("""
                QDialog { background-color: #0d1117; }
                QLabel { font-size: 15px; color: #c9d1d9; }
                QPushButton {
                    background-color: #30363d;
                    color: #c9d1d9;
                    padding: 8px;
                    border-radius: 6px;
                }
                QPushButton:hover { background-color: #484f58; }
                QCheckBox { color: #c9d1d9; font-size: 14px; }
                QFrame { background-color: #30363d; max-height: 1px; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background-color: #f6f8fa; }
                QLabel { font-size: 15px; color: #24292f; }
                QPushButton {
                    background-color: #2da44e;
                    color: white;
                    padding: 8px;
                    border-radius: 6px;
                }
                QPushButton:hover { background-color: #2c974b; }
                QCheckBox { color: #24292f; font-size: 14px; }
                QFrame { background-color: #d0d7de; max-height: 1px; }
            """)