from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsOpacityEffect

from Security.auth import authenticate_user
from GUI.vault import VaultWindow
from GUI.signup import SignupWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SecureVault")
        self.setMinimumSize(1000, 700)

        # Remove dialog feel
        self.setWindowFlags(Qt.Window)

        # -------- Background --------
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("assets/login_bg.jpg"))
        self.background.setScaledContents(True)

        # -------- Styling --------
        self.setStyleSheet("""
            QWidget {
                font-family: "Segoe UI";
                font-size: 14px;
                color: white;
            }

            QFrame#card {
                background-color: rgba(22, 27, 34, 220);
                border-radius: 12px;
                padding: 24px;
            }

            QLineEdit {
                background-color: rgba(13, 17, 23, 220);
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px;
                color: white;
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
        self.showMaximized()

    # Make background cover full window
    def resizeEvent(self, event):
        self.background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(420)

        layout = QVBoxLayout(card)
        layout.setSpacing(15)

        title = QLabel("SecureVault Login")
        title.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("primary")
        login_btn.clicked.connect(self.login)

        signup_btn = QPushButton("Create Account")
        signup_btn.setObjectName("secondary")
        signup_btn.clicked.connect(self.signup)

        self.password_input.returnPressed.connect(self.login)
        self.username_input.returnPressed.connect(self.login)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addWidget(signup_btn)

        root.addWidget(card)

    # 🔥 Smooth Fade Transition
    def fade_transition(self, next_window):
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)

        def on_finished():
            next_window.showMaximized()
            self.close()

        self.animation.finished.connect(on_finished)
        self.animation.start()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        result = authenticate_user(username, password)

        if result:
            user_id, key = result
            self.vault = VaultWindow(user_id, key)
            self.fade_transition(self.vault)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")

    def signup(self):
        self.signup_window = SignupWindow(self)
        self.signup_window.show()