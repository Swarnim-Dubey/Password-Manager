import sys
from PySide6.QtWidgets import QApplication

from Database.db import init_db
from GUI.login import LoginWindow
from config import apply_theme
# apply_theme(app, "dark")

def main():
    # Initialize database (VERY IMPORTANT)
    init_db()

    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()