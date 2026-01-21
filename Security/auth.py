import bcrypt


# Make a hashed version of the password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Check if a password matches the stored one or not
def check_password(password, stored_hash):
    return bcrypt.checkpw(password.encode(), stored_hash)

def get_creds(prompt : str)-> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("THE CREDENTIALS CANNOT BE EMPTY 😑")

# --------- VERIFYING THE MASTER PASSWORD ---------

if __name__ == "__main__":
    print("-------- MASTER PASSWORD TEST --------")

    # First time setup
    print("------ FIRST TIME SETUP ------")
    pwd = get_creds("\nCreate MASTER password : ")
    stored_hash = hash_password(pwd)
    print("Password saved securely!")

    # Login
    login_pwd = get_creds("Enter master password : ")

    if check_password(login_pwd, stored_hash):
        print("Login successful! ✅")
    else:
        print("Wrong password! 😑")