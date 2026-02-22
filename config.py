# config.py

APP_THEME = "dark"

DARK = """
QWidget {
    background-color: #0B1220;
    color: #E5E7EB;
    font-family: Segoe UI;
    font-size: 14px;
}

QPushButton {
    background-color: #1F2937;
    border-radius: 6px;
    padding: 6px;
}
QPushButton:hover { background-color: #374151; }

QLineEdit {
    background-color: #020617;
    border: 1px solid #1F2937;
    border-radius: 6px;
    padding: 6px;
}
"""

LIGHT = """
QWidget {
    background-color: #F8FAFC;
    color: #0F172A;
    font-family: Segoe UI;
    font-size: 14px;
}

QPushButton {
    background-color: #E2E8F0;
    border-radius: 6px;
    padding: 6px;
}
QPushButton:hover { background-color: #CBD5E1; }

QLineEdit {
    background-color: white;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px;
}
"""

def apply_theme(app, theme):
    global APP_THEME
    APP_THEME = theme
    app.setStyleSheet(DARK if theme == "dark" else LIGHT)