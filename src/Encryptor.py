import os
import glob
import json
import base64
from cryptography.fernet import Fernet
from .config import *

class Encryptor:

    def __init__(self) -> None:
        self.key_file_path = None
        os.makedirs(ROOT, exist_ok=True)
        os.makedirs(HOME, exist_ok=True)

        key_files = [f for f in glob.glob(ROOT + "/*") if os.path.isfile(f)]
        if key_files:
            self.key_file_path = key_files[0]
            key = os.path.basename(self.key_file_path).encode()
            self.cipher_suite = Fernet(key)
        else:
            key = Fernet.generate_key()
            self.cipher_suite = Fernet(key)
            key_file_name = key.decode()
            self.key_file_path = os.path.join(ROOT, key_file_name)
            with open(self.key_file_path, 'w') as f:
                f.write(self.encrypt_data(json.dumps({
                    "users": {
                        "admin": "ECE422"
                    },
                    "groups": {}
                })))
            admin_folder = f"{HOME}/{self.encrypt_data('admin')}"
            os.makedirs(admin_folder, exist_ok=True)
            with open(f"{admin_folder}/{self.encrypt_data('admin')}", 'w') as f:
                f.write(self.encrypt_data(json.dumps({})))

    def encrypt_data(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        # Encode encrypted bytes to a base64 string for easier handling
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt_data(self, encrypted_data):
        # Decode base64 string to bytes before decryption
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode()
        
encryptor = Encryptor()

def read_file(path):
    with open(path, 'r') as f:
        decrypted_data = encryptor.decrypt_data(f.read())
        return json.loads(decrypted_data)
    
def write_file(path, data):
    encrypted_data = encryptor.encrypt_data(json.dumps(data))
    with open(path, 'w') as f:
        f.write(encrypted_data)

def to_real_encoded_dir(fake_dir):
    dir_component = fake_dir.split("/")
    encoded_dir = HOME
    home_reached = False
    for dc in dir_component:
        if dc == "":
            continue
        elif dc == "home" and not home_reached:
            home_reached = True
            continue
        else:
            encoded_entries = os.listdir(encoded_dir)
            encode_map = {}
            for ee in encoded_entries:
                encode_map[encryptor.decrypt_data(ee)] = ee
            encoded_dir = os.path.join(encoded_dir, encode_map[dc])

    return encoded_dir

def to_fake_decoded_dir(real_dir):
    dir_component = real_dir.split("/")
    decoded_dir = ""
    root_reached, home_reached = False, False
    for dc in dir_component:
        # print(dc)
        if dc == "":
            continue
        elif dc == "root" and not root_reached:
            root_reached = True
            decoded_dir = os.path.join(decoded_dir, "/")
        elif dc == "home" and not home_reached:
            home_reached = True
            decoded_dir = os.path.join(decoded_dir, "home")
        else:
            decoded_dir = os.path.join(decoded_dir, encryptor.decrypt_data(dc))
            # decoded_dir = f"{decoded_dir}/{encryptor.decrypt_data(dc)}"
    return decoded_dir
