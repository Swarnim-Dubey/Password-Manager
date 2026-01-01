import base64
import sys

# importing functions from folders

from Security.auth import hash_password, check_password
from Security.encryption import make_key, encrypt_text, decrypt_text
from Database.db import (init_db, store_master_hash, get_master_hash, add_credential, get_credentials, delete_credential)

# ---------- Base 64 ----------

def encode_b64(data):
    return base64.b64encode(data).decode("utf-8")

def decode_b64(data):
    return base64.b64encode(data.encode("utf-8"))

# ---------- Master Password ----------

def setup_master_password():
    print("-" * 15,"\nFirst time setup", "-" * 15)
    pwd = input("Create master password : ")
    hashed = hash_password(pwd)
    store_master_hash(hashed)
    print("Master password have been saved successfully !!")

def login():
    stored_hash = get_master_hash()
    pwd = input("Enter MASTER password : ")

    if check_password(pwd, stored_hash):
        print("Login Successful ✅")
        return make_key(pwd)
    else:
        print("Wrong Password ❌")
        return None

# ----------- MENU ----------

def dashboard(key):
    while True:
        print("---------- DASHBOARD ----------")
        print("1. Add Credential")
        print("2. View Credentials")
        print("3. Delete Credential(s)")
        print("4. Exit")

        choice = int(input("Enter your choice : "))

        if choice == 1:
            service = input("Service Name : ")
            username = input("Username : ")
            password = input("Password : ")

            encrypted = encrypt_text(password, key)
            encrypted_b64 = encode_b64(encrypted)

            add_credential(service, username, encrypted_b64)
            print("Credential Stored Successfully! ✅")

        elif choice == 2:
            creds = get_credentials()

            if not creds:
                print("No credentials found 😓")
                continue

            print("\nStored Credentials are :")
            for service, username, password_b64 in creds:
                decrypted = decrypt_text(
                    decode_b64(password_b64),
                    key
                )
                print(f"{service} | {username} | {decrypted}")

        elif choice == 3:
            service = input("Service name to delete: ")
            delete_credential(service)
            print("Credential Deleted Successfully! 👍")

        elif choice == 4:
            print("Bye 👋")
            break

        else:
            print("Invalid choice!")


# ---------- PROGRAM START ----------

def main():
    print("\n","-" * 30, "PASSWORD MANAGER", "-" * 30)

    init_db()

    # First run
    if not get_master_hash():
        setup_master_password()

    key = login()
    if key is None:
        sys.exit()

    dashboard(key)


if __name__ == "__main__":
    main()
