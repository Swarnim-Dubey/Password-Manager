import os
import sys
import sqlite3

# ---------- BASE DIRECTORY ----------
if getattr(sys, "frozen", False):
    # Running as PyInstaller exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as normal Python script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "passwords.db")


# ---------- CONNECTION ----------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ---------- DATABASE SETUP ----------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Master password table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS master_auth (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            password_hash BLOB NOT NULL
        )
    """)

    # Credentials table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------- MASTER PASSWORD ----------
def store_master_hash(password_hash: bytes):
    """
    Stores or replaces the single master password hash.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR REPLACE INTO master_auth (id, password_hash) VALUES (1, ?)",
        (password_hash,)
    )

    conn.commit()
    conn.close()


def get_master_hash():
    """
    Returns stored master password hash or None if not set.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT password_hash FROM master_auth WHERE id = 1")
    row = cur.fetchone()

    conn.close()
    return row[0] if row else None


# ---------- CREDENTIALS ----------
def add_credential(service, username, password, category):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO credentials (service, username, password, category) VALUES (?, ?, ?, ?)",
        (service, username, password, category)
    )

    conn.commit()
    conn.close()


def get_credentials():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT id, service, username, password, category FROM credentials"
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def update_credential(cred_id, service, username, password, category):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE credentials
        SET service = ?, username = ?, password = ?, category = ?
        WHERE id = ?
    """, (service, username, password, category, cred_id))

    conn.commit()
    conn.close()


def delete_credential(cred_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM credentials WHERE id = ?", (cred_id,))

    conn.commit()
    conn.close()


# ---------- COMPATIBILITY ALIASES ----------
def get_master_password_hash():
    return get_master_hash()


def set_master_password_hash(password_hash: bytes):
    store_master_hash(password_hash)
