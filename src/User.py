import os
import getpass
import json
from .Encryptor import encryptor, read_file, write_file
from .config import *

class InternalUser:

    def __init__(self) -> None:
        pass




class AdminUser(InternalUser):

    def __init__(self) -> None:
        self.admin_file = encryptor.key_file_path

    def createUser(self):
        admin_data = read_file(self.admin_file)
        user_name = input("User name: ")

        # check if user already exists
        if user_name in admin_data["users"]:
            print(f"{user_name} already exists.")
            return

        user_password = getpass.getpass("User password: ")
        admin_data["users"][user_name] = user_password
        write_file(self.admin_file, admin_data)

        # make an encrypted folder for this user
        user_folder = f"{HOME}/{encryptor.encrypt_data(user_name)}"
        os.makedirs(user_folder)
        write_file(f"{user_folder}/{encryptor.encrypt_data(user_name)}", {})
    
    def createGroup(self):
        group_name = input("Group name: ")
        group_users = input("Group members (comma separated): ").split(",")
        admin_data = read_file(self.admin_file)

        # check if all users are valid
        existed_users = admin_data["users"].keys()
        valid_group_users = []
        for user in group_users:
            if user not in existed_users:
                print(f"{user} is not a valid user. Skipped")
                continue
            valid_group_users.append(user)

        if group_name not in admin_data["groups"]:
            admin_data["groups"][group_name] = []
        admin_data["groups"][group_name].extend(valid_group_users)
        write_file(self.admin_file, admin_data)

admin_user = AdminUser()
# AdminUser().createUser()
# AdminUser().createUser()
# AdminUser().createGroup()
# print(read_file(AdminUser().admin_file))
