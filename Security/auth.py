import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
# from Database.db import create_user
from Database.db import (
    get_user_by_email, save_otp, clear_otp, update_password, get_user_by_identifier, hash_password
)
from Security.otp_manager import generate_otp, get_expiry_time, is_otp_valid
from Security.email_service import send_email
from Database.db import get_user_by_identifier, hash_password


# ================= AUTH =================

def authenticate_user(identifier, password):
    user = get_user_by_identifier(identifier)

    if not user:
        return None

    stored_hash = user["password"]
    salt = user["salt"]

    if hash_password(password, salt) == stored_hash:
        key = user["encryption_key"].encode()
        return (user["id"], key)

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

# ---------- SEND OTP ----------

def send_otp_to_email(email):
    user = get_user_by_email(email)

    if not user:
        return False, "User does not exist"

    otp = generate_otp()
    expiry = get_expiry_time()

    save_otp(email, otp, expiry)

    subject = "Your OTP Code"
    body = f"""
Your OTP is: {otp}

This OTP will expire in 5 minutes.
"""

    if send_email(email, subject, body):
        return True, "OTP sent successfully"
    else:
        return False, "Failed to send email"


# ---------- VERIFY OTP ----------

def verify_otp(email, entered_otp):
    user = get_user_by_email(email)

    if not user:
        return False, "User not found"

    stored_otp = user["otp"]
    stored_expiry = user["otp_expiry"]

    valid, message = is_otp_valid(stored_otp, stored_expiry, entered_otp)

    if valid:
        clear_otp(email)

    return valid, message


# ---------- RESET PASSWORD ----------

def reset_password(email, new_password):
    update_password(email, new_password)
    return True, "Password updated successfully"