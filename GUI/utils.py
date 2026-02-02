from PySide6.QtWidgets import QMessageBox, QLabel
from PySide6.QtCore import Qt


def show_centered_message(parent, title, text, icon=QMessageBox.Information):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setIcon(icon)

    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setWordWrap(True)

    msg.layout().addWidget(label, 0, 1)
    msg.exec()
