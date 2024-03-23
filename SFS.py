import json
import src.Encryptor as Encryptor
from src.config import *
data_file = ROOT

def load_data():
    try:
        with open(data_file, 'rb') as file:
            encrypted_data = file.read()
            decrypted_data = Encryptor.decrypt_data(encrypted_data)
            return json.loads(decrypted_data)
    except FileNotFoundError:
        return {"users": [], "groups": []}
    
def save_data(data):
    encrypted_data = Encryptor.encrypt_data(json.dumps(data))
    with open(data_file, 'wb') as file:
        file.write(encrypted_data)

def create_user(username, password_hash, groups):
    data = load_data()
    data['users'].append({"username": username, "password_hash": password_hash, "groups": groups})
    save_data(data)

def list_users():
    data = load_data()
    for user in data['users']:
        print(user['username'])

def create_group(group_name):
    data = load_data()
    data['groups'].append({"group_name": group_name, "members": []})
    save_data(data)

def list_groups():
    data = load_data()
    for group in data['groups']:
        print(group['group_name'])

