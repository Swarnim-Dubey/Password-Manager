import os
import sqlite3
import hashlib
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "passwords.db")


# -------------------------
# CONNECTION
# -------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------
# DATABASE INIT
# -------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table (Multi-user system)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    # Credentials table (linked to user)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# -------------------------
# PASSWORD HASHING
# -------------------------
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


# -------------------------
# USER FUNCTIONS
# -------------------------
def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    try:
        cursor.execute(
            "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
            (username, salt, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, salt, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    user_id, salt, stored_hash = user
    if hash_password(password, salt) == stored_hash:
        return user_id

    return None


# -------------------------
# CREDENTIAL FUNCTIONS
# -------------------------
def add_credential(user_id, website, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO credentials (user_id, website, email, password) VALUES (?, ?, ?, ?)",
        (user_id, website, email, password)
    )

    conn.commit()
    conn.close()


def get_credentials(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, website, email, password FROM credentials WHERE user_id = ?",
        (user_id,)
    )

    data = cursor.fetchall()
    conn.close()
    return data


def delete_credential(credential_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM credentials WHERE id = ?", (credential_id,))
    conn.commit()
    conn.close()