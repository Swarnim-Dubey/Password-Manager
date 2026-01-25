from Security.auth import hash_password, check_password
from Security.encryption import make_key, encrypt_text, decrypt_text
from Database.db import init_db, store_master_hash, get_master_hash, add_credential, get_credentials, delete_cred_by_id
import base64
import sys

# ---------- BASE64 ----------

def encode_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")

def decode_b64(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))

# ---------- MASTER PASSWORD ----------

def setup_master_password():
    print("-"*15,"\nFirst-time setup","-"*15)
    pwd = input("Create MASTER password : ")
    store_master_hash(hash_password(pwd))
    print("Master password stored securely!")

def login():
    stored_hash = get_master_hash()
    pwd = input("Enter MASTER password : ")
    if check_password(pwd, stored_hash):
        print("Login Successful!")
        return make_key(pwd)

    print("Wrong Password!")
    return None

# ---------- MAIN DASHBOARD ----------

def get_creds(prompt : str)-> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("THE CREDENTIALS CANNOT BE EMPTY")

def dashboard(key: bytes):
    while True:
        print("\n----- DASHBOARD -----")
        print("1. Add credential")
        print("2. View credentials")
        print("3. Delete credential")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            service = get_creds("Service Name : ")
            username = get_creds("Username : ")
            password = get_creds("Password : ")
            encrypted = encrypt_text(password, key)
            encrypted_b64 = encode_b64(encrypted)
            add_credential(service, username, encrypted_b64)
            print("Credential Stored! ")

        elif choice == "2":
            creds = get_credentials()
            if not creds:
                print("No Credentials Stored")
                continue
            print("\nStored Credentials are :")
            for service, username, password_b64 in creds:
                decrypted = decrypt_text(decode_b64(password_b64),key)
                print(f"{service} | {username} | {decrypted}")

        elif choice == "3":
            creds = get_credentials()
            if not creds:
                print("Found no credentials to delete !!")
                continue
                
            print("\nSelect credentials to delete : ")
            for index, (cid, service, username, _) in enumerate(creds, start = 1):
                print(f"{index}. {service} | {username}")
            try:
                choice = int(input("Enter your choice : "))
                selected =creds[choice - 1]
                cred_id = selected[0]

                confirm = input("Are you sure, you want to delete? (y/n) : ").lower()
                if confirm == "y":
                    delete_cred_by_id(cred_id)
                    print("The credential was Deleted !!")
                else:
                    print("Deletion was cancelled :( ")
            except:
                print("Invalid Selection !!")

            '''service = get_creds("Service name to delete : ")
            delete_credential(service)
            print("Credential deleted!")'''

        elif choice == "4":
            print("Bye ")
            break

        else:
            print("Invalid choice!")


# ---------- PROGRAM START ----------

def main():
    print("-" * 25," PASSWORD MANAGER ", "-" * 25)

    init_db()

    if not get_master_hash():
        setup_master_password()

    key = login()
    if key is None:
        sys.exit()

    dashboard(key)


if __name__ == "__main__":
    main()
