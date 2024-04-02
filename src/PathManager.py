import os
import json
import xattr
import getpass
from checksumdir import dirhash
from .Encryptor import encryptor

def permission_to_bool(permission_num):
    permission_oct = int(str(permission_num), 8)
    return [b == '1' for b in bin(permission_oct)[2:].zfill(9)]

class PathManager:

    def __init__(self) -> None:
        self.root = "file-system"
        self.home = os.path.join(self.root, "home")
        os.makedirs(self.home, exist_ok=True)
        self.set_path_permission(self.root, {
            "owner": "admin",
            "group": "admin",
            "permission": 755
        })
        self.set_path_permission(self.home, {
            "owner": "admin",
            "group": "admin",
            "permission": 755
        })
        try:
            self.get_all_users()
        except IOError:
            print("Initializing SFS for first use...")
            self.set_all_users({
                "admin": {
                    "password": "",
                    "groups": "admin",
                    "lastHash": ""
                }
            })
            admin_home_path = os.path.join(self.home, encryptor.encrypt_data("admin"))
            self.create_folder(admin_home_path, "admin")
            self.save_hash("admin")

    
    def get_all_users(self):
        encrypted_users = xattr.getxattr(self.root, "user.SFS.users").decode()
        return json.loads(encryptor.decrypt_data(encrypted_users))
    

    def set_all_users(self, all_users):
        encrypted_users = encryptor.encrypt_data(json.dumps(all_users))
        xattr.setxattr(self.root, "user.SFS.users", encrypted_users.encode())
    

    def get_user(self, user_name):
        users = self.get_all_users()
        if user_name not in users:
            raise Exception(f"{user_name}: User does not exist.")
        return users[user_name]
    

    def create_user(self, user_name):
        users = self.get_all_users()
        if user_name in users:
            raise Exception(f"{user_name}: User already exists.")
        users[user_name] = {
            "password": getpass.getpass("User password: "),
            "groups": input(f"Groups {user_name} belongs to (comma separated, 1st one the default): ").split(","),
            "lastHash": ""
        }
        self.set_all_users(users)
        user_home_path = os.path.join(self.home, encryptor.encrypt_data(user_name))
        self.create_folder(user_home_path, user_name)
        self.save_hash(user_name)


    def save_hash(self, user_name):
        users = self.get_all_users()
        user_home_path = self.to_real_encoded_path(os.path.join("/home", user_name))
        users[user_name]["lastHash"] = dirhash(user_home_path, 'sha256')
        self.set_all_users(users)

    
    def check_hash(self, user_name):
        users = self.get_all_users()
        user_home_path = self.to_real_encoded_path(os.path.join("/home", user_name))
        return users[user_name]["lastHash"] == dirhash(user_home_path, 'sha256')

    
    def get_path_permission(self, path):
        encrypted_permission = xattr.getxattr(path, "user.SFS.permission").decode()
        return json.loads(encryptor.decrypt_data(encrypted_permission))
    

    def set_path_permission(self, path, permission):
        encrypted_permission = encryptor.encrypt_data(json.dumps(permission))
        xattr.setxattr(path, "user.SFS.permission", encrypted_permission.encode())
    

    def check_permission(self, path, user_name, permission):
        p_index = {
            'r': 0,
            'w': 1,
            'x': 2
        }[permission]

        user_data = self.get_user(user_name)
        p_data = self.get_path_permission(path)
        p_bool_list = permission_to_bool(p_data["permission"])

        has_owner_p = p_data["owner"] == user_name and p_bool_list[0:3][p_index]
        has_group_p = p_data["group"] in user_data["groups"] and p_bool_list[3:6][p_index]
        has_other_p = p_bool_list[6:9][p_index]
        return has_owner_p or has_group_p or has_other_p
    

    def create_file(self, file_path, owner):
        open(file_path, 'w').close()
        users = self.get_all_users()
        group = users[owner]["groups"][0]
        self.set_path_permission(file_path, {
            "owner": owner,
            "group": group,
            "permission": 710
        })
    

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            decrypted_data = encryptor.decrypt_data(f.read())
            return json.loads(decrypted_data)
        
    
    def write_file(self, file_path, data):
        encrypted_data = encryptor.encrypt_data(json.dumps(data))
        with open(file_path, 'w') as f:
            f.write(encrypted_data)
        # a = self.read_file(file_path)
        # print(a)

    
    def create_folder(self, folder_path, owner):
        os.makedirs(folder_path)
        users = self.get_all_users()
        group = users[owner]["groups"][0]
        self.set_path_permission(folder_path, {
            "owner": owner,
            "group": group,
            "permission": 710
        })
    

    def to_real_encoded_path(self, fake_path):
        if fake_path == "/":
            return self.root
        encoded_path = ""
        fake_path_components = os.path.normpath(fake_path).split(os.sep)
        for i, fpc in enumerate(fake_path_components):
            if i == 0:
                encoded_path = self.root
                continue
            if i == 1:
                encoded_path = self.home
                continue
            encoded_fpcs = os.listdir(encoded_path)
            found = False
            for efpc in encoded_fpcs:
                if encryptor.decrypt_data(efpc) == fpc:
                    found = True
                    encoded_path = os.path.join(encoded_path, efpc)
                    break
            if not found:
                raise Exception(f"{fake_path}: Path does not exists")
        return encoded_path

    
    def to_fake_decoded_path(self, real_path):
        decoded_path = ""
        real_path_components = os.path.normpath(real_path).split(os.sep)
        for i, rpc in enumerate(real_path_components):
            if i == 0:
                decoded_path = "/"
                continue
            if i == 1:
                decoded_path = f"/{rpc}"
                continue
            decoded_path = os.path.join(decoded_path, encryptor.decrypt_data(rpc))
        return decoded_path

PM = PathManager()

if __name__ == '__main__':
    os.makedirs("aaa")
    def set_extended_attribute_with_json(path, attribute_name, data):
        attr_name = f"user.{attribute_name}"
        json_data = json.dumps(data)  # Convert the data to a JSON string
        xattr.setxattr(path, attr_name, json_data.encode())

    # Get and deserialize an extended attribute
    def get_extended_attribute_as_json(path, attribute_name):
        attr_name = f"user.{attribute_name}"
        try:
            json_data = xattr.getxattr(path, attr_name)
            return json.loads(json_data.decode())  # Convert the JSON string back to data
        except IOError:  # The attribute might not exist
            return None

    # Example usage
    path = "aaa"  # Replace with your path
    attribute_name = "metadata"
    data = {
        "author": "John Doe",
        "tags": ["example", "demo"],
        "published": True
    }

    # Set the attribute with serialized JSON data
    set_extended_attribute_with_json(path, attribute_name, data)

    # Retrieve the attribute and deserialize the JSON data
    retrieved_data = get_extended_attribute_as_json(path, attribute_name)
    print(f"Retrieved Data: {retrieved_data}")
