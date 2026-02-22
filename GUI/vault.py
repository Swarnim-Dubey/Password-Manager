from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QFrame, QListWidget,
    QApplication, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from GUI.toggle_switch import ToggleSwitch
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation
from GUI.theme import LIGHT_THEME, DARK_THEME
from Database.db import (
    get_credentials,
    delete_credential,
    get_categories,
    get_username
)
from GUI.add_cred import AddCredentialWindow
from GUI.settings import SettingsWindow


class VaultWindow(QWidget):
    def __init__(self, user_id, key):
        super().__init__()

        self.user_id = user_id
        self.key = key
        self.credentials = []
        self.current_theme = "dark"

        self.setWindowTitle("VaultX")
        self.setMinimumSize(1100, 650)

        self.init_ui()
        self.apply_theme()

        self.load_categories()
        self.load_data()

    # ================= UI =================

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar, 1)

        # Right Side Layout
        right_layout = QVBoxLayout()

        # Top Bar (for toggle in corner)
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.theme_toggle = ToggleSwitch()
        self.theme_toggle.setChecked(True)  # Dark default
        self.theme_toggle.clicked = self.toggle_theme

        top_bar.addWidget(self.theme_toggle)
        right_layout.addLayout(top_bar)

        # Action bar
        self.action_bar = self.create_action_bar()
        self.action_bar.hide()
        right_layout.addWidget(self.action_bar)

        # Table
        self.table = self.create_table()
        right_layout.addWidget(self.table)

        main_layout.addLayout(right_layout, 4)

    # ================= SIDEBAR =================

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        layout = QVBoxLayout(sidebar)

        title = QLabel("VaultX")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        self.category_list = QListWidget()
        self.category_list.itemClicked.connect(self.filter_by_category)
        layout.addWidget(self.category_list)

        layout.addStretch()

        # + Add Credential (with icon)
        self.add_button = QPushButton("  Add Credential")
        self.add_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        # Settings (with icon)
        self.settings_button = QPushButton("  Settings")
        self.settings_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)

        # 🌗 Animated Toggle Switch
        # self.theme_toggle = ToggleSwitch()
        # self.theme_toggle.setChecked(False)
        # self.theme_toggle.clicked = self.toggle_theme

        # layout.addWidget(self.theme_toggle, alignment=Qt.AlignCenter)

        username = get_username(self.user_id)
        user_label = QLabel(username)
        user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_label)

        return sidebar

    # ================= TABLE =================

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Service", "Username", "Password"])
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setSectionResizeMode(QHeaderView.Stretch)

        table.itemSelectionChanged.connect(self.toggle_action_bar)
        return table

    # ================= ACTION BAR =================

    def create_action_bar(self):
        bar = QFrame()
        layout = QHBoxLayout(bar)

        self.copy_user_btn = QPushButton("Copy Username")
        self.copy_pass_btn = QPushButton("Copy Password")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        self.copy_user_btn.clicked.connect(self.copy_username)
        self.copy_pass_btn.clicked.connect(self.copy_password)
        self.edit_btn.clicked.connect(self.edit_selected)
        self.delete_btn.clicked.connect(self.delete_selected)

        layout.addWidget(self.copy_user_btn)
        layout.addWidget(self.copy_pass_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()

        return bar

    # ================= DATA =================

    def load_categories(self):
        self.category_list.clear()
        categories = get_categories(self.user_id)

        if "All" not in categories:
            categories.insert(0, "All")

        self.category_list.addItems(categories)
        self.category_list.setCurrentRow(0)

    def load_data(self, category=None):
        if category == "All":
            category = None

        self.credentials = get_credentials(self.user_id, category)
        self.table.setRowCount(len(self.credentials))

        for row, cred in enumerate(self.credentials):
            cred_id, website, email, password, category = cred
            self.table.setItem(row, 0, QTableWidgetItem(website))
            self.table.setItem(row, 1, QTableWidgetItem(email))
            self.table.setItem(row, 2, QTableWidgetItem("•••••••"))

    def filter_by_category(self, item):
        self.load_data(item.text())

    # ================= ACTION VISIBILITY =================

    def toggle_action_bar(self):
        self.action_bar.setVisible(self.table.currentRow() >= 0)

    # ================= COPY =================

    def copy_username(self):
        row = self.table.currentRow()
        if row >= 0:
            QApplication.clipboard().setText(self.credentials[row][2])

    def copy_password(self):
        row = self.table.currentRow()
        if row >= 0:
            QApplication.clipboard().setText(self.credentials[row][3])

    # ================= EDIT =================

    def edit_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        cred = self.credentials[row]

        dialog = AddCredentialWindow(
            self.user_id,
            self.key,
            self,
            cred=cred,
            theme=self.current_theme
        )

        if dialog.exec():
            self.load_categories()
            self.load_data()

    # ================= DELETE =================

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        cred_id = self.credentials[row][0]
        website = self.credentials[row][1]

        confirm = QMessageBox(self)
        confirm.setWindowTitle("Confirm Delete")
        confirm.setText(f"Delete credentials for {website}?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        if confirm.exec() == QMessageBox.Yes:
            delete_credential(cred_id)
            self.load_categories()
            self.load_data()
            self.action_bar.hide()

    # ================= ADD =================

    def open_add_dialog(self):
        dialog = AddCredentialWindow(
            self.user_id,
            self.key,
            self,
            theme=self.current_theme
        )

        if dialog.exec():
            self.load_categories()
            self.load_data()

    # ================= SETTINGS =================

    def open_settings(self):
        dialog = SettingsWindow(
            self.user_id,
            current_theme=self.current_theme,
            parent=self
        )

        if dialog.exec():
            self.current_theme = (
                "dark" if dialog.theme_toggle.isChecked() else "light"
            )
            self.apply_theme()

    # ================= THEME =================

    def toggle_theme(self):
        self.current_theme = (
            "dark" if self.current_theme == "light" else "light"
        )
        self.apply_theme()

    def apply_theme(self):
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)

        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(200)
        self.anim.setStartValue(0.7)
        self.anim.setEndValue(1.0)

        if self.current_theme == "light":
            self.setStyleSheet(LIGHT_THEME)
            self.theme_toggle.setChecked(False)
        else:
            self.setStyleSheet(DARK_THEME)
            self.theme_toggle.setChecked(True)

        self.anim.start()