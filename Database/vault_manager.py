import os
from Database.db import get_connection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "data", "vaults")

os.makedirs(VAULT_DIR, exist_ok=True)


def get_vault_path(username):
    safe_username = username.lower()
    return os.path.join(VAULT_DIR, f"{safe_username}.db")


def create_vault(username):
    db_path = get_vault_path(username)

    if os.path.exists(db_path):
        return False  # already exists

    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    return True


def load_vault(username):
    db_path = get_vault_path(username)
    return get_connection(db_path)