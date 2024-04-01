import os
import base64
from cryptography.fernet import Fernet

class Encryptor:

    def __init__(self) -> None:
        encrypt_key_file = "SFS-key.pem"

        if not os.path.isfile(encrypt_key_file):
            print("SFS-key not found. Create a new one for first use...")
            create_new_key_selection = input("Do you want to create a new one? (y/n): ")

            if create_new_key_selection != "y":
                exit()
            encrypt_key = Fernet.generate_key()
            with open(encrypt_key_file, 'wb') as f:
                f.write(encrypt_key)

            print("The SFS key is critical to activate the whole encryption of SFS.")
            print("Please keep this key file in a secret place:")
            print(f"\n\t{encrypt_key_file}\n")
        
        with open(encrypt_key_file, 'rb') as f:
            encrypt_key = f.read()
            self.encryptor = Fernet(encrypt_key)
    

    def encrypt_data(self, decrypted_data):
        encrypted_data = self.encryptor.encrypt(decrypted_data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    

    def decrypt_data(self, encrypted_data):
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        return self.encryptor.decrypt(encrypted_bytes).decode()

encryptor = Encryptor()
