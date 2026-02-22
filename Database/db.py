import os
import sqlite3
import hashlib
import secrets

# =========================
# DATABASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "passwords.db")


# =========================
# CONNECTION
# =========================
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# =========================
# DATABASE INIT
# =========================
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        # Credentials table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                website TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'Other',
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()


# =========================
# PASSWORD HASHING
# =========================
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


# =========================
# USER FUNCTIONS
# =========================
def create_user(username, password):
    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                (username, salt, password_hash)
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_user(username):
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, password_hash, salt FROM users WHERE username = ?",
            (username,)
        )
        return cursor.fetchone()


def get_username(user_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        return row[0] if row else "Unknown User"


# =========================
# CREDENTIAL FUNCTIONS
# =========================
def add_credential(user_id, website, email, password, category="Other"):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO credentials (user_id, website, email, password, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, website, email, password, category)
        )


def get_credentials(user_id, category=None):
    with get_connection() as conn:
        if category and category != "All":
            cursor = conn.execute(
                """
                SELECT id, website, email, password, category
                FROM credentials
                WHERE user_id = ? AND category = ?
                """,
                (user_id, category)
            )
        else:
            cursor = conn.execute(
                """
                SELECT id, website, email, password, category
                FROM credentials
                WHERE user_id = ?
                """,
                (user_id,)
            )

        return cursor.fetchall()


def delete_credential(credential_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM credentials WHERE id = ?",
            (credential_id,)
        )


def update_credential(cred_id, website, email, password, category):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE credentials
            SET website = ?, email = ?, password = ?, category = ?
            WHERE id = ?
            """,
            (website, email, password, category, cred_id)
        )


# =========================
# CATEGORY FUNCTIONS
# =========================
def get_categories(user_id):
    default_categories = ["All", "Social", "Work", "Finance", "Shopping", "Other"]

    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT DISTINCT category FROM credentials WHERE user_id = ?",
            (user_id,)
        )
        rows = cursor.fetchall()

    user_categories = [
        row[0] for row in rows
        if row[0] not in default_categories and row[0] is not None
    ]

    return default_categories + user_categories

def delete_all_credentials(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM credentials WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()