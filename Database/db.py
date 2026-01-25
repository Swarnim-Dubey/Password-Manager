import sqlite3
from pathlib import Path

DB_NAME = "password-manager.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------- DATABASE SETUP ----------

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Table for Master Password
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash BLOB NOT NULL
        )
    """)

    # Table for the credentials
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------- MASTER PASSWORD ----------

def store_master_hash(password_hash: bytes):
    conn = get_connection()
    cursor = conn.cursor()

    # Ensure only ONE master password exists
    cursor.execute("DELETE FROM master_auth")

    cursor.execute(
        "INSERT INTO master_auth (password_hash) VALUES (?)",
        (password_hash,)
    )
    conn.commit()
    conn.close()


def get_master_hash():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM master_auth LIMIT 1")
    row = cursor.fetchone()

    conn.close()
    return row[0] if row else None


# ---------- CREDENTIALS ----------

def add_credential(service: str, username: str, password_b64: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO credentials (service, username, password)
        VALUES (?, ?, ?)
    """, (service, username, password_b64))

    conn.commit()
    conn.close()


def get_credentials():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, service, username, password FROM credentials")
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_credential(service: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM credentials WHERE service = ?",
        (service,)
    )

    conn.commit()
    conn.close()

def delete_cred_by_id(cred_id : int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM credentials WHERE id = ?", (cred_id))

    conn.commit()
    conn.close()


# ---------- TESTING ----------

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database is ready !")
