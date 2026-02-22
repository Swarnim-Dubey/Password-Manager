from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QRadioButton, QPushButton, QApplication
from config import apply_theme

class SettingsDialog(QDialog):
    def __init__(self, logout_callback):
        super().__init__()
        self.logout_callback = logout_callback

        self.setWindowTitle("Settings")
        self.setFixedWidth(260)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Appearance"))

        dark = QRadioButton("Dark Mode")
        light = QRadioButton("Light Mode")
        dark.setChecked(True)

        layout.addWidget(dark)
        layout.addWidget(light)

        layout.addSpacing(10)
        layout.addWidget(QLabel("Account"))

        logout_btn = QPushButton("Logout")
        layout.addWidget(logout_btn)

        dark.toggled.connect(lambda: apply_theme(QApplication.instance(), "dark"))
        light.toggled.connect(lambda: apply_theme(QApplication.instance(), "light"))
        logout_btn.clicked.connect(self.logout)

    def logout(self):
        self.close()
        self.logout_callback()