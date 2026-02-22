from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor


class ToggleSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(60, 30)
        self._position = 3
        self._checked = False

        self.animation = QPropertyAnimation(self, b"position", self)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setDuration(200)

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.animate()
        self.update()
        self.clicked()

    def animate(self):
        start = self._position
        end = 30 if self._checked else 3
        self.animation.stop()
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        bg_color = QColor("#30363d") if self._checked else QColor("#d0d7de")
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 60, 30, 15, 15)

        # Circle
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QRect(self._position, 3, 24, 24))

    def getPosition(self):
        return self._position

    def setPosition(self, pos):
        self._position = pos
        self.update()

    position = Property(int, getPosition, setPosition)

    def isChecked(self):
        return self._checked

    def setChecked(self, value):
        self._checked = value
        self._position = 30 if value else 3
        self.update()

    def clicked(self):
        # This will be overridden by connection
        pass