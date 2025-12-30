import base64
import sys

# importing functions from folders

from Security.auth import hash_password, check_password
from Security.encryption import make_key, encrypt_text, decrypt_text
from Database.db import (init_db, store_master_hash, get_master_hash, add_credential, get_credentials, delete_credential)

# ---------- Base 64 ----------

def encode_b64(data):
    ...

def decode_b64(data):
    ...