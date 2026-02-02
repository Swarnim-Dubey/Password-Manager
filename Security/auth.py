import os
import base64
import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


# ---------------- PASSWORD HASHING ----------------

def hash_password(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def verify_password(password: str, stored_hash: bytes) -> bool:
    return hash_password(password) == stored_hash


# ---------------- KEY DERIVATION ----------------

def derive_key(password: str) -> bytes:
    salt = b"password-manager-salt"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
        backend=default_backend()
    )

    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


# ---------------- ENCRYPT / DECRYPT ----------------

def encrypt_data(plain_text: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(plain_text.encode())


def decrypt_data(cipher_text: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(cipher_text).decode()
