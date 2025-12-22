# Integration of Base64 and AES-256

import hashlib
import base64
from cryptography.fernet import Fernet

# ---------- Functions ----------

def make_key(master_pwd: str) -> bytes:
    # Derive a Fernet key from a master password using SHA256
    hashed = hashlib.sha256(master_pwd.encode()).digest()
    key = base64.urlsafe_b64encode(hashed)
    return key

def encrypt_text(txt: str, key: bytes) -> bytes:
    # Encrypt text using Fernet AES
    f = Fernet(key)
    return f.encrypt(txt.encode("utf-8"))

def decrypt_text(enc: bytes, key: bytes) -> str:
    # Decrypt bytes back to string using Fernet AES
    f = Fernet(key)
    try:
        dec = f.decrypt(enc)
        return dec.decode("utf-8")
    except Exception as e:
        print("Decryption failed : ", e)
        return " "

def encode_b64(data: bytes) -> str:
    # Convert bytes to Base64 string
    return base64.b64encode(data).decode("utf-8")

def decode_b64(txt: str) -> bytes:
    # Convert Base64 string back to bytes
    try:
        return base64.b64decode(txt.encode("utf-8"))
    except Exception as e:
        print("Decode error : ", e)
        return b" "

#   ---------- Main Code ----------

if __name__ == "__main__":
    print("-" * 20, "AES + BASE64 SECURITY SYSTEM", "-" * 20)
    print()

    pwd = input("Enter MASTER password : ")
    key = make_key(pwd)
    print("Key generated successfully!\n")

    stored_b64 = None

    while True:
        print("\nWhat you want to do?")
        print("1. Encrypt & Store")
        print("2. Show Stored (Base64)")
        print("3. Decode & Decrypt")
        print("4. Quit")

        choice = input("Enter choice : ")

        if choice == "1":
            txt = input("Enter text to encrypt and store : ")
            enc_bytes = encrypt_text(txt, key)
            stored_b64 = encode_b64(enc_bytes)
            print("String stored successfully!")

        elif choice == "2":
            if stored_b64:
                print("Stored Base64 string :\n", stored_b64)
            else:
                print("No string stored yet :(")

        elif choice == "3":
            if stored_b64:
                enc_bytes = decode_b64(stored_b64)
                dec_txt = decrypt_text(enc_bytes, key)
                print("Decoded & Decrypted text : ", dec_txt)
            else:
                print("No string stored yet :(")

        elif choice == "4":
            print("Bye!")
            break

        else:
            print("Invalid option, try again.")