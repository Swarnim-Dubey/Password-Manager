from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt

from Security.encryption import decrypt_text
from Database.db import get_credentials, delete_cred_by_id
from GUI.add_cred import AddCredentialWindow
import base64


def decode_b64(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


class ViewCredentialWindow(QWidget):
    def __init__(self, key: bytes):
        super().__init__()
        self.key = key
        self.setWindowTitle("View Credentials")
        self.resize(850, 500)

        self.setup_ui()
        self.populate_services()
        self.load_credentials()

    # ---------- UI ----------

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Top bar
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Filter By Service:"))

        self.service_filter = QComboBox()
        self.service_filter.currentIndexChanged.connect(self.load_credentials)
        top_bar.addWidget(self.service_filter)

        add_btn = QPushButton("➕ Add Credential")
        add_btn.clicked.connect(self.open_add_window)
        top_bar.addWidget(add_btn)

        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Service", "Username", "Password", "👁", "🗑"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    # ---------- DROPDOWN ----------

    def populate_services(self):
        self.service_filter.blockSignals(True)
        self.service_filter.clear()
        self.service_filter.addItem("All Services")

        creds = get_credentials()
        services = sorted(set(c[1] for c in creds))
        self.service_filter.addItems(services)

        self.service_filter.blockSignals(False)

    # ---------- TABLE ----------

    def load_credentials(self):
        self.table.setRowCount(0)
        selected_service = self.service_filter.currentText()

        creds = get_credentials()
        for cid, service, username, pwd_b64 in creds:
            if selected_service != "All Services" and service != selected_service:
                continue
            self.add_row(cid, service, username, pwd_b64)

    def add_row(self, cid, service, username, pwd_b64):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(service))
        self.table.setItem(row, 1, QTableWidgetItem(username))

        pwd_item = QTableWidgetItem("••••••••")
        pwd_item.setData(Qt.UserRole, pwd_b64)
        self.table.setItem(row, 2, pwd_item)

        # 👁 Eye button
        eye_btn = QPushButton("👁")
        eye_btn.clicked.connect(lambda _, r=row: self.toggle_password(r))
        self.table.setCellWidget(row, 3, eye_btn)

        # 🗑 Delete button
        del_btn = QPushButton("🗑")
        del_btn.clicked.connect(lambda _, i=cid: self.delete_credential(i))
        self.table.setCellWidget(row, 4, del_btn)

    # ---------- ACTIONS ----------

    def toggle_password(self, row):
        item = self.table.item(row, 2)

        if item.text().startswith("•"):
            try:
                enc = decode_b64(item.data(Qt.UserRole))
                dec = decrypt_text(enc, self.key)
                item.setText(dec)
            except Exception:
                item.setText("Decryption Failed")
        else:
            item.setText("••••••••")

    def delete_credential(self, cid):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this credential?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_cred_by_id(cid)
            self.populate_services()
            self.load_credentials()

    def open_add_window(self):
        dialog = AddCredentialWindow(self.key, self)
        dialog.exec()
        self.populate_services()
        self.load_credentials()
