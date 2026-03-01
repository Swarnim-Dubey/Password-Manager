from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, Signal, Property
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class ToggleSwitch(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(50, 25)

        self._checked = False
        self._circle_position = 3

        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    # ---------------- Checked State ----------------

    def isChecked(self):
        return self._checked

    def setChecked(self, value):
        self._checked = value
        self._circle_position = 25 if value else 3
        self.update()

    # ---------------- Animation Property ----------------

    def get_circle_position(self):
        return self._circle_position

    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = Property(int, get_circle_position, set_circle_position)

    # ---------------- Mouse Click ----------------

    def mousePressEvent(self, event):
        self._checked = not self._checked

        self.animation.stop()
        if self._checked:
            self.animation.setStartValue(3)
            self.animation.setEndValue(25)
        else:
            self.animation.setStartValue(25)
            self.animation.setEndValue(3)

        self.animation.start()

        self.toggled.emit(self._checked)

        super().mousePressEvent(event)

    # ---------------- Paint ----------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        if self._checked:
            painter.setBrush(QColor("#238636"))
        else:
            painter.setBrush(QColor("#777"))

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRect(0, 0, 50, 25), 12, 12)

        # Circle
        painter.setBrush(QColor("white"))
        painter.drawEllipse(QRect(self._circle_position, 3, 19, 19))