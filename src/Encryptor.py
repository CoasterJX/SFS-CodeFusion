import os
import glob
import json
from cryptography.fernet import Fernet
from config import *

class Encryptor:

    def __init__(self) -> None:
        self.key_file_path = None

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
            with open(self.key_file_path, 'wb') as f:
                f.write(self.encrypt_data(json.dumps({
                    "users": {
                        "admin": "ECE422"
                    },
                    "groups": {}
                })))

    def encrypt_data(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()
        
encryptor = Encryptor()

def read_file(path):
    with open(path, 'rb') as f:
        decrypted_data = encryptor.decrypt_data(f.read())
        return json.loads(decrypted_data)
    
def write_file(path, data):
    encrypted_data = encryptor.encrypt_data(json.dumps(data))
    with open(path, 'wb') as f:
        f.write(encrypted_data)
