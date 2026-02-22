# GUI/theme_manager.py

from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect


class ThemeManager:
    current_theme = "dark"

    DARK_THEME = """
    QWidget {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: "Segoe UI";
        font-size: 14px;
    }

    QFrame#sidebar {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    QPushButton {
        background-color: #21262d;
        border: 1px solid #30363d;
        padding: 8px;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #30363d;
    }

    QHeaderView::section {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 8px;
        font-weight: 600;
    }

    QTableWidget {
        background-color: #0d1117;
        gridline-color: #30363d;
    }

    QListWidget {
        background-color: #161b22;
        border: none;
    }
    """

    LIGHT_THEME = """
    QWidget {
        background-color: #f5f5f5;
        color: #111111;
        font-family: "Segoe UI";
        font-size: 14px;
    }

    QFrame#sidebar {
        background-color: #ffffff;
        border-right: 1px solid #cccccc;
    }

    QPushButton {
        background-color: #e0e0e0;
        border: 1px solid #cccccc;
        padding: 8px;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #d6d6d6;
    }

    QHeaderView::section {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        padding: 8px;
        font-weight: 600;
    }

    QTableWidget {
        background-color: #ffffff;
        gridline-color: #cccccc;
    }

    QListWidget {
        background-color: #ffffff;
        border: none;
    }
    """

    @classmethod
    def apply_theme(cls, widget):
        if cls.current_theme == "dark":
            widget.setStyleSheet(cls.DARK_THEME)
        else:
            widget.setStyleSheet(cls.LIGHT_THEME)

    @classmethod
    def toggle_theme(cls, widget):
        # Fade animation
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

        fade_out = QPropertyAnimation(effect, b"opacity")
        fade_out.setDuration(150)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)

        fade_in = QPropertyAnimation(effect, b"opacity")
        fade_in.setDuration(150)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)

        def switch_theme():
            cls.current_theme = "light" if cls.current_theme == "dark" else "dark"
            cls.apply_theme(widget)
            fade_in.start()

        fade_out.finished.connect(switch_theme)
        fade_out.start()