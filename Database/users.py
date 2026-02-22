import os
from Database.vault_manager import get_vault_path

def user_exists(username):
    return os.path.exists(get_vault_path(username))


def create_user(username, password):
    if user_exists(username):
        return False
    return True


def validate_login(username):
    return user_exists(username)