import hashlib
import base64
from cryptography.fernet import Fernet


def make_key(master_password: str) -> bytes:
    """
    derives a Fernet-compatible AES-256 key
    from the master password
    """
    hashed = hashlib.sha256(master_password.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(hashed)


def encrypt_text(plain_text: str, key: bytes) -> bytes:
    """
    encrypt plain text using AES (Fernet)
    it returns encrypted bytes
    """
    f = Fernet(key)
    return f.encrypt(plain_text.encode("utf-8"))


def decrypt_text(encrypted_bytes: bytes, key: bytes) -> str:
    """
    Decrypt AES encrypted bytes.
    Returns original string.
    Raises exception if key is wrong.
    """
    f = Fernet(key)
    return f.decrypt(encrypted_bytes).decode("utf-8")
