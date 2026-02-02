# import sys
# from PySide6.QtWidgets import QApplication
# from GUI.login import LoginWindow
# from Database.db import init_db


# def main():
#     init_db()
#     app = QApplication(sys.argv)

#     login = LoginWindow()
#     login.show()

#     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()

import sys
from PySide6.QtWidgets import QApplication

from Database.db import init_db
from GUI.login import LoginWindow


def main():
    init_db()

    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
