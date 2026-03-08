import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from Database.db import get_user


# ================= AUTH =================

def authenticate_user(username, password):
    user = get_user(username)

    if not user:
        return None

    user_id, stored_hash, salt = user

    hashed_input = hashlib.sha256((password + salt).encode()).hexdigest()

    if hashed_input == stored_hash:
        key = derive_key(password, salt)
        return (user_id, key)

    return None


# ================= KEY DERIVATION =================

def derive_key(password: str, salt: str) -> bytes:
    """
    Derive encryption key using user's actual salt
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),  # use stored salt
        iterations=200_000,
        backend=default_backend()
    )

    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


# ================= ENCRYPT / DECRYPT =================

def encrypt_data(plain_text: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(plain_text.encode()).decode()


def decrypt_data(cipher_text: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(cipher_text.encode()).decode()