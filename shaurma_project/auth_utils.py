# auth_utils.py
import json
import hashlib
import os

def load_users():
    if not os.path.exists('data.json'):
        return {}
    with open('data.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open('data.json', 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {'password': hash_password(password)}
    save_users(users)
    return True

def authenticate_user(username, password):
    users = load_users()
    if username not in users:
        return False
    return users[username]['password'] == hash_password(password)