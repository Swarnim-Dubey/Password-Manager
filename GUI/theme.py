# GUI/theme.py

# =========================
# LIGHT THEME (GitHub Light Fixed)
# =========================
LIGHT_THEME = """
QWidget {
    font-size: 15px;
    color: #24292f;
}

QMainWindow, QWidget {
    background-color: #f6f8fa;
}

QFrame#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #d0d7de;
}

QFrame#sidebar QLabel {
    color: #24292f;
    font-size: 16px;
    font-weight: 500;
}

QListWidget {
    background-color: #ffffff;
    border: none;
    color: #24292f;
    font-size: 15px;
}

QListWidget::item {
    padding: 6px;
}

QListWidget::item:selected {
    background-color: #eaeef2;
    color: #000000;
    border-radius: 4px;
}

QLineEdit {
    padding: 8px;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    background-color: white;
    color: #24292f;
}

QPushButton {
    background-color: #eaeef2;
    color: #24292f;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #d0d7de;
}

QPushButton:hover {
    background-color: #d8dee4;
}

QTableWidget {
    background-color: white;
    border: 1px solid #d0d7de;
    color: #24292f;
    gridline-color: #d0d7de;
}

QHeaderView::section {
    background-color: #f6f8fa;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #d0d7de;
}
"""


# =========================
# GITHUB DARK THEME (Grey Button Edition)
# =========================
DARK_THEME = """
QWidget {
    font-size: 15px;
    color: #c9d1d9;
}

QMainWindow, QWidget {
    background-color: #0d1117;
}

QFrame#sidebar {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}

QFrame#sidebar QLabel {
    color: #c9d1d9;
    font-size: 16px;
    font-weight: 500;
}

QListWidget {
    background-color: #161b22;
    border: none;
    color: #c9d1d9;
    font-size: 15px;
}

QListWidget::item {
    padding: 6px;
}

QListWidget::item:selected {
    background-color: #30363d;
    color: #ffffff;
    border-radius: 4px;
}

QLineEdit {
    padding: 8px;
    border: 1px solid #30363d;
    border-radius: 6px;
    background-color: #0d1117;
    color: #c9d1d9;
}

QPushButton {
    background-color: #21262d;
    color: #c9d1d9;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #30363d;
}

QPushButton:hover {
    background-color: #30363d;
}

QPushButton:pressed {
    background-color: #3b434b;
}

QTableWidget {
    background-color: #0d1117;
    border: 1px solid #30363d;
    color: #c9d1d9;
    gridline-color: #30363d;
}

QHeaderView::section {
    background-color: #161b22;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #30363d;
}
"""