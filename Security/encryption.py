# Trying AES-256 encryption/decryption

import hashlib
import base64
from cryptography.fernet import Fernet


def make_key(master_pwd: str) -> bytes:
    # take password -> sha256 -> 32 bytes
    hashed = hashlib.sha256(master_pwd.encode()).digest()
    # fernet wants base64 key so just do that
    key = base64.urlsafe_b64encode(hashed)
    return key


def encrypt_text(txt: str, key: bytes) -> bytes:
    # encrypt the text
    f = Fernet(key)
    result = f.encrypt(txt.encode())
    return result


def decrypt_text(enc: bytes, key: bytes) -> str:
    # decrypt back to string
    f = Fernet(key)
    try:
        dec = f.decrypt(enc)
        return dec.decode()
    except Exception as e:
        print("decryption failed:", e)
        return ""


# main test thing
if __name__ == "__main__":
    # print("-" * 20)
    print("-" * 20, "AES ENCRYPTION AND DECRYPTION (TESTING_PHASE)", "-" * 20)
    print()

    pwd = input("Enter MASTER password: ")
    key = make_key(pwd)
    print("Key made successfully!\n")

    while True:
        print("Options:")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Quit")

        choice = input("Your choice: ")

        if choice == "1":
            txt = input("Text to encrypt: ")
            enc = encrypt_text(txt, key)
            print("Encrypted:", enc)

        elif choice == "2":
            print("Paste encrypted bytes:")
            enc_in = input()
            try:
                # lol using eval here, kinda unsafe but works
                enc_bytes = eval(enc_in)
                dec = decrypt_text(enc_bytes, key)
                print("Decrypted:", dec)
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            print("Bye!")
            break

        else:
            print("Invalid option, try again.")