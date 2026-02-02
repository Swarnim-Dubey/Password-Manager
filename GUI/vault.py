from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QLabel,
    QMessageBox, QApplication, QHeaderView
)
from PySide6.QtCore import Qt

from Database.db import get_credentials, delete_credential
from GUI.add_cred import AddCredentialWindow
from GUI.edit_cred import EditCredentialWindow
from Security.auth import decrypt_data


class VaultWindow(QWidget):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.selected_credential = None
        self.credentials = []

        self.setWindowTitle("Password Vault")
        self.setFixedSize(900, 550)

        self.build_ui()
        self.refresh_category_filter()
        self.load_credentials()

    # ------------------ UI ------------------

    def build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ---------- Top Controls ----------
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        self.add_button = QPushButton("➕ Add")
        self.edit_button = QPushButton("✏️ Edit")
        self.delete_button = QPushButton("🗑 Delete")
        self.copy_user_button = QPushButton("📋 Copy Username")
        self.copy_pass_button = QPushButton("🔑 Copy Password")

        for btn in [
            self.add_button, self.edit_button, self.delete_button,
            self.copy_user_button, self.copy_pass_button
        ]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(36)

        self.add_button.clicked.connect(self.open_add)
        self.edit_button.clicked.connect(self.open_edit)
        self.delete_button.clicked.connect(self.delete_selected)
        self.copy_user_button.clicked.connect(self.copy_username)
        self.copy_pass_button.clicked.connect(self.copy_password)

        controls_layout.addWidget(self.add_button)
        controls_layout.addWidget(self.edit_button)
        controls_layout.addWidget(self.delete_button)
        controls_layout.addWidget(self.copy_user_button)
        controls_layout.addWidget(self.copy_pass_button)
        controls_layout.addStretch()

        controls_layout.addWidget(QLabel("Category:"))

        self.category_filter_combo = QComboBox()
        self.category_filter_combo.setFixedWidth(140)
        self.category_filter_combo.currentTextChanged.connect(self.filter_by_category)
        controls_layout.addWidget(self.category_filter_combo)

        main_layout.addLayout(controls_layout)

        # ---------- Table ----------
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Service", "Username", "Password", "Category"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self.select_credential)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0F0F0F;
                color: #EDEDED;
                font-size: 13px;
                border: 1px solid #1E1E1E;
            }
            QHeaderView::section {
                background-color: #151515;
                color: #FFFFFF;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding-left: 6px;
            }
            QTableWidget::item:selected {
                background-color: #2B2B2B;
                color: #FFFFFF;
            }
        """)

        main_layout.addWidget(self.table)

        # ---------- Global Dark Theme ----------
        self.setStyleSheet("""
            QWidget { background-color: #0B0B0B; color: #EDEDED; }
            QPushButton {
                background-color: #1C1C1C;
                color: #FFFFFF;
                border-radius: 8px;
                font-weight: 600;
                padding: 6px 16px;
                font-size: 13px;
                border: 1px solid #2A2A2A;
            }
            QPushButton:hover { background-color: #2A2A2A; }
            QPushButton:pressed { background-color: #111111; }
            QComboBox {
                background-color: #151515;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 5px;
                font-size: 12px;
                border: 1px solid #2A2A2A;
            }
            QLabel { font-size: 12px; color: #EDEDED; }
        """)

    # ------------------ Data ------------------

    def refresh_category_filter(self):
        credentials = get_credentials()
        categories = sorted({c["category"] for c in credentials if c["category"]})

        self.category_filter_combo.blockSignals(True)
        self.category_filter_combo.clear()
        self.category_filter_combo.addItem("All")
        self.category_filter_combo.addItems(categories)
        self.category_filter_combo.blockSignals(False)

    def load_credentials(self, category_filter="All"):
        self.table.setRowCount(0)
        self.selected_credential = None
        self.credentials = get_credentials()

        filtered = [
            c for c in self.credentials
            if category_filter == "All" or c["category"] == category_filter
        ]

        self.table.setRowCount(len(filtered))
        for row, cred in enumerate(filtered):
            self.table.setItem(row, 0, self._center_item(cred["service"]))
            self.table.setItem(row, 1, self._center_item(cred["username"]))
            self.table.setItem(row, 2, self._center_item("••••••••"))
            self.table.setItem(row, 3, self._center_item(cred["category"]))

    def _center_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    # ------------------ Actions ------------------

    def select_credential(self, row, _):
        if 0 <= row < len(self.credentials):
            self.selected_credential = self.credentials[row]

    def open_add(self):
        AddCredentialWindow(self.key, self).exec()
        self.refresh_category_filter()
        self.load_credentials(self.category_filter_combo.currentText())

    def open_edit(self):
        if not self.selected_credential:
            return
        EditCredentialWindow(self.key, self.selected_credential, self).exec()
        self.refresh_category_filter()
        self.load_credentials(self.category_filter_combo.currentText())

    def delete_selected(self):
        if not self.selected_credential:
            return

        service = self.selected_credential["service"]

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Do you want to delete the credential for '{service}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        delete_credential(self.selected_credential["id"])
        self.selected_credential = None
        self.refresh_category_filter()
        self.load_credentials(self.category_filter_combo.currentText())

    def filter_by_category(self, category):
        self.load_credentials(category)

    # ------------------ Clipboard ------------------

    def copy_username(self):
        if not self.selected_credential:
            return
        QApplication.clipboard().setText(self.selected_credential["username"])
        self.show_message("Copied", "Username copied to clipboard.")

    def copy_password(self):
        if not self.selected_credential:
            return
        password = decrypt_data(self.selected_credential["password"], self.key)
        QApplication.clipboard().setText(password)
        self.show_message("Copied", "Password copied to clipboard.")

    # ------------------ Utility ------------------

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
