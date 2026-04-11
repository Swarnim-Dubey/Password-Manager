import os
import json

USERS_FILE = "Database/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- For the user thing ----------

def user_exists(username):
    users = load_users()
    return username in users


def email_exists(email):
    users = load_users()
    return any(user["email"] == email for user in users.values())


def create_user(username, password, email):
    users = load_users()

    if username in users:
        return False, "Username already exists"

    if email_exists(email):
        return False, "Email already registered"

    users[username] = {
        "password": password,
        "email": email,
        "otp": None,
        "otp_expiry": None
    }

    save_users(users)
    return True, "User created successfully"


def validate_login(identifier, password):
    users = load_users()

    for username, data in users.items():
        if username == identifier or data["email"] == identifier:
            if data["password"] == password:
                return True, username

    return False, None


# ---------- OTP  System ----------

def get_user_by_email(email):
    users = load_users()

    for username, data in users.items():
        if data["email"] == email:
            return username, data

    return None, None

def save_otp(email, otp, expiry):
    users = load_users()

    for username in users:
        if users[username]["email"] == email:
            users[username]["otp"] = otp
            users[username]["otp_expiry"] = expiry

    save_users(users)

def clear_otp(email):
    users = load_users()

    for username in users:
        if users[username]["email"] == email:
            users[username]["otp"] = None
            users[username]["otp_expiry"] = None

    save_users(users)

def update_password(email, new_password):
    users = load_users()

    for username in users:
        if users[username]["email"] == email:
            users[username]["password"] = new_password

    save_users(users)
