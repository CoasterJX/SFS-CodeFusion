import getpass
import os
from src.Encryptor import encryptor, read_file, write_file
from src.Encryptor import to_fake_decoded_dir, to_real_encoded_dir
from src.config import *
from src.User import admin_user

admin_file = encryptor.key_file_path


if __name__ == '__main__':

    print("Secure File System (SFS)")
    current_user = "*"
    current_dir = ""

    while True:
        cmd = input(f"{current_user}>>> ").split(" ")
        argv = [] if len(cmd) < 2 else cmd[1:]
        cmd = cmd[0]
        if cmd == "":
            continue
        print("\n")

        # guest user access
        if current_user == "*":

            if cmd == "login":
                username = input("Enter user name: ")
                password = getpass.getpass(f"{username}'s password: ")
                admin_data = read_file(admin_file)
                if admin_data["users"].get(username, None) != password:
                    print("Invalid credential.")
                else:
                    current_user = username
                    current_dir = f"/home/{username}"
            
            elif cmd == "quit":
                break
            
            else:
                print("You haven't login. Please login first.")
        
        # internal user access
        elif cmd == "logout":
            current_user = "*"
            root_dir = ROOT
        elif cmd == "pwd":
            print(current_dir)
        elif cmd == "ls":
            if current_dir == "/home":
                admin_data = read_file(admin_file)
                # print(admin_data)
                # users = admin_data["users"].keys()
                same_group_users = set()
                for _, group_members in admin_data["groups"].items():
                    # print(current_user, group_members, current_user in group_members)
                    if current_user in group_members:
                        same_group_users = same_group_users.union(set(group_members))
                for user_encoded in os.listdir(to_real_encoded_dir(current_dir)):
                    user = encryptor.decrypt_data(user_encoded)
                    if user in same_group_users:
                        print(user)
                    else:
                        print(user_encoded)
            else:
                admin_data = read_file(admin_file)
                
        elif cmd == "cd":
            if len(argv) == 0:
                print("Please specify destination.")
            else:
                paths = argv[0].split("/")
                for p in paths:
                    if p == "":
                        continue
                    elif p == "..":
                        current_dir = os.path.dirname(current_dir)
                    else:
                        current_dir = os.path.join(current_dir, p)
        
        # admin user access
        elif cmd == "create-user" and current_user == "admin":
            admin_user.createUser()
        elif cmd == "create-group" and current_user == "admin":
            admin_user.createGroup()
            
        else:
            print("Invalid command.")
        
        print("\n")
