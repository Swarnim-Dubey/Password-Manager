from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from GUI.settings_dialog import SettingsDialog

class TitleBar(QWidget):
    def __init__(self, parent=None, title="SecureVault"):
        super().__init__(parent)
        self.parent = parent
        self.startPos = None

        self.setFixedHeight(36)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)

        self.title_label = QLabel(title)
        layout.addWidget(self.title_label)
        layout.addStretch()

        # SETTINGS
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setFixedSize(28,28)
        self.settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_btn)

        # MIN
        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(28,28)
        self.min_btn.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.min_btn)

        # MAX
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(28,28)
        self.max_btn.clicked.connect(self.toggle_max)
        layout.addWidget(self.max_btn)

        # CLOSE
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(28,28)
        self.close_btn.clicked.connect(self.parent.close)
        layout.addWidget(self.close_btn)

    def toggle_max(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def open_settings(self):
        dialog = SettingsDialog(self.parent.logout)
        dialog.exec()

    # drag window
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.startPos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        if self.startPos:
            delta = e.globalPosition().toPoint() - self.startPos
            self.parent.move(self.parent.pos() + delta)
            self.startPos = e.globalPosition().toPoint()

    def mouseReleaseEvent(self, e):
        self.startPos = None