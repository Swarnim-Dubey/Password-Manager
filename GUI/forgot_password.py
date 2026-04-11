# from PySide6.QtWidgets import (
#     QWidget, QLabel, QLineEdit, QPushButton,
#     QVBoxLayout, QMessageBox
# )
# from PySide6.QtCore import Qt

# from Security.auth import send_otp_to_email, verify_otp, reset_password


# class ForgotPasswordWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Forgot Password")
#         self.setFixedSize(400, 300)

#         self.layout = QVBoxLayout(self)
#         self.layout.setAlignment(Qt.AlignCenter)

#         self.init_email_stage()

#     # ---------- STEP 1: ENTER EMAIL ----------
#     def init_email_stage(self):
#         self.clear_layout()

#         title = QLabel("Enter your email")
#         title.setAlignment(Qt.AlignCenter)

#         self.email_input = QLineEdit()
#         self.email_input.setPlaceholderText("Email")

#         send_btn = QPushButton("Send OTP")
#         send_btn.clicked.connect(self.send_otp)

#         self.layout.addWidget(title)
#         self.layout.addWidget(self.email_input)
#         self.layout.addWidget(send_btn)

#     def send_otp(self):
#         email = self.email_input.text().strip()

#         if not email:
#             QMessageBox.warning(self, "Error", "Please enter email")
#             return

#         success, message = send_otp_to_email(email)

#         if success:
#             QMessageBox.information(self, "Success", message)
#             self.init_otp_stage(email)
#         else:
#             QMessageBox.warning(self, "Error", message)

#     # ---------- STEP 2: VERIFY OTP ----------
#     def init_otp_stage(self, email):
#         self.clear_layout()
#         self.email = email

#         title = QLabel("Enter OTP")
#         title.setAlignment(Qt.AlignCenter)

#         self.otp_input = QLineEdit()
#         self.otp_input.setPlaceholderText("6-digit OTP")

#         verify_btn = QPushButton("Verify OTP")
#         verify_btn.clicked.connect(self.verify_otp_action)

#         self.layout.addWidget(title)
#         self.layout.addWidget(self.otp_input)
#         self.layout.addWidget(verify_btn)

#     def verify_otp_action(self):
#         otp = self.otp_input.text().strip()

#         if not otp:
#             QMessageBox.warning(self, "Error", "Enter OTP")
#             return

#         success, message = verify_otp(self.email, otp)

#         if success:
#             QMessageBox.information(self, "Success", message)
#             self.init_reset_stage()
#         else:
#             QMessageBox.warning(self, "Error", message)

#     # ---------- STEP 3: RESET PASSWORD ----------
#     def init_reset_stage(self):
#         self.clear_layout()

#         title = QLabel("Set New Password")
#         title.setAlignment(Qt.AlignCenter)

#         self.new_password = QLineEdit()
#         self.new_password.setPlaceholderText("New Password")
#         self.new_password.setEchoMode(QLineEdit.Password)

#         reset_btn = QPushButton("Reset Password")
#         reset_btn.clicked.connect(self.reset_password_action)

#         self.layout.addWidget(title)
#         self.layout.addWidget(self.new_password)
#         self.layout.addWidget(reset_btn)

#     def reset_password_action(self):
#         new_pass = self.new_password.text().strip()

#         if not new_pass:
#             QMessageBox.warning(self, "Error", "Enter new password")
#             return

#         success, message = reset_password(self.email, new_pass)

#         if success:
#             QMessageBox.information(self, "Success", message)
#             self.close()
#         else:
#             QMessageBox.warning(self, "Error", message)

#     # ---------- HELPER ----------
#     def clear_layout(self):
#         while self.layout.count():
#             item = self.layout.takeAt(0)
#             widget = item.widget()
#             if widget:
#                 widget.deleteLater()

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QMessageBox
)
from PySide6.QtCore import Qt

from Security.auth import send_otp_to_email, verify_otp, reset_password


class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Forgot Password")
        self.setFixedSize(500, 400)

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

        self.root = QVBoxLayout(self)
        self.root.setAlignment(Qt.AlignCenter)

        self.card = QFrame()
        self.card.setObjectName("card")
        self.card.setFixedWidth(350)

        self.layout = QVBoxLayout(self.card)
        self.layout.setSpacing(15)

        self.root.addWidget(self.card)

        self.init_email_stage()

    # ---------- STEP 1 ----------
    def init_email_stage(self):
        self.clear_layout()

        title = QLabel("Forgot Password")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Enter your registered email")
        subtitle.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        send_btn = QPushButton("Send OTP")
        send_btn.setObjectName("primary")
        send_btn.clicked.connect(self.send_otp)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("secondary")
        back_btn.clicked.connect(self.close)

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(send_btn)
        self.layout.addWidget(back_btn)

    def send_otp(self):
        email = self.email_input.text().strip()

        if not email:
            QMessageBox.warning(self, "Error", "Please enter email")
            return

        success, message = send_otp_to_email(email)

        if success:
            QMessageBox.information(self, "Success", message)
            self.init_otp_stage(email)
        else:
            QMessageBox.warning(self, "Error", message)

    # ---------- STEP 2 ----------
    def init_otp_stage(self, email):
        self.clear_layout()
        self.email = email

        title = QLabel("Verify OTP")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Enter the OTP sent to your email")
        subtitle.setAlignment(Qt.AlignCenter)

        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("6-digit OTP")

        verify_btn = QPushButton("Verify OTP")
        verify_btn.setObjectName("primary")
        verify_btn.clicked.connect(self.verify_otp_action)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("secondary")
        back_btn.clicked.connect(self.init_email_stage)

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)
        self.layout.addWidget(self.otp_input)
        self.layout.addWidget(verify_btn)
        self.layout.addWidget(back_btn)

    def verify_otp_action(self):
        otp = self.otp_input.text().strip()

        if not otp:
            QMessageBox.warning(self, "Error", "Enter OTP")
            return

        success, message = verify_otp(self.email, otp)

        if success:
            QMessageBox.information(self, "Success", message)
            self.init_reset_stage()
        else:
            QMessageBox.warning(self, "Error", message)

    # ---------- STEP 3 ----------
    def init_reset_stage(self):
        self.clear_layout()

        title = QLabel("Reset Password")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Enter your new password")
        subtitle.setAlignment(Qt.AlignCenter)

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("New Password")
        self.new_password.setEchoMode(QLineEdit.Password)

        reset_btn = QPushButton("Reset Password")
        reset_btn.setObjectName("primary")
        reset_btn.clicked.connect(self.reset_password_action)

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)
        self.layout.addWidget(self.new_password)
        self.layout.addWidget(reset_btn)

    def reset_password_action(self):
        new_pass = self.new_password.text().strip()

        if not new_pass:
            QMessageBox.warning(self, "Error", "Enter new password")
            return

        success, message = reset_password(self.email, new_pass)

        if success:
            QMessageBox.information(self, "Success", message)
            self.close()
        else:
            QMessageBox.warning(self, "Error", message)

    # ---------- HELPER ----------
    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()