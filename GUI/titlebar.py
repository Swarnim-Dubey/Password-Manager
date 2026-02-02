from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon

class TitleBar(QWidget):
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.parent = parent
        self.startPos = None

        self.setFixedHeight(38)
        self.setStyleSheet("""
            background-color: #1A1A1A;
            color: #EAEAEA;
            font-family: Segoe UI;
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Minimize button
        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(28, 28)
        self.min_btn.setCursor(Qt.PointingHandCursor)
        self.min_btn.setStyleSheet("""
            QPushButton { border: none; background-color: transparent; }
            QPushButton:hover { background-color: #333333; }
        """)
        self.min_btn.clicked.connect(self.minimize)
        layout.addWidget(self.min_btn)

        # Maximize/Restore button
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(28, 28)
        self.max_btn.setCursor(Qt.PointingHandCursor)
        self.max_btn.setStyleSheet("""
            QPushButton { border: none; background-color: transparent; }
            QPushButton:hover { background-color: #333333; }
        """)
        self.max_btn.clicked.connect(self.maximize_restore)
        layout.addWidget(self.max_btn)

        # Close button
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton { border: none; background-color: transparent; color: #EAEA00; }
            QPushButton:hover { background-color: #FF4C4C; color: white; }
        """)
        self.close_btn.clicked.connect(self.close_window)
        layout.addWidget(self.close_btn)

    # -------- Button actions --------
    def minimize(self):
        if self.parent:
            self.parent.showMinimized()

    def maximize_restore(self):
        if self.parent:
            if self.parent.isMaximized():
                self.parent.showNormal()
            else:
                self.parent.showMaximized()

    def close_window(self):
        if self.parent:
            self.parent.close()

    # -------- Drag window --------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.startPos:
            delta = event.globalPosition().toPoint() - self.startPos
            self.parent.move(self.parent.pos() + delta)
            self.startPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.startPos = None
