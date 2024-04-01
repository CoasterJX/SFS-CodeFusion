import os
import getpass
from src2.PathManager import PM
from src2.Encryptor import encryptor

if __name__ == '__main__':

    print("Secure File System (SFS)")
    current_user = None
    current_user_name = ""
    current_path = ""

    def init():
        global current_user, current_user_name, current_path
        current_user = None
        current_user_name = ""
        current_path = ""

    while True:
        try:
            print()
            cmd = input(f"{current_user_name}>>> ").split(" ")
            argv = [] if len(cmd) < 2 else cmd[1:]
            cmd = cmd[0]
            if cmd == "":
                continue
            print()

            # guest user access
            if current_user == None:

                if cmd == "login":

                    # check user existence
                    user_name = input("Enter user name: ")
                    current_user = PM.get_user(user_name)
                    current_user_name = user_name
                    current_path = f"/home/{current_user_name}"

                    # check password correctness
                    password = getpass.getpass(f"{current_user_name}'s password: ")
                    if current_user["password"] != password:
                        print("Invalid credential.")
                        init()
                        continue

                    # check hash correctness
                    if not PM.check_hash(current_user_name):
                        print("!!! Your file or folder has been modified !!!")

                elif cmd == "quit":
                    print("Bye.")
                    break

                else:
                    print("You haven't login. Please login first.")
            
            # admin user access
            elif cmd == "create-user" and current_user_name == "admin":
                PM.create_user(input("Enter user name: "))

            # internal user access
            elif cmd == "logout":
                PM.save_hash(current_user_name)
                init()
            
            elif cmd == "pwd":
                print(current_path)

            elif cmd == "ls":

                # get target ls path
                if len(argv) == 0:
                    ls_path = current_path
                else:
                    ls_path = os.path.join(current_path, argv[0])
                    ls_path = os.path.normpath(ls_path)
                real_ls_path = PM.to_real_encoded_path(ls_path)

                # check if path is executable
                if not PM.check_permission(real_ls_path, current_user_name, 'x'):
                    print(f"{ls_path}: Permission denied")
                    continue

                # execute and display decoded ones with read access
                for res in os.listdir(real_ls_path):
                    if res == "home":
                        print(res)
                        continue
                    res_path = os.path.join(real_ls_path, res)
                    if PM.check_permission(res_path, current_user_name, 'r'):
                        print(encryptor.decrypt_data(res))
                    else:
                        print(res)
                
            elif cmd == "cd":

                # get target cd path
                if len(argv) == 0:
                    print("Please specify destination.")
                    continue
                destination = os.path.join(current_path, argv[0])
                destination = os.path.normpath(destination)
                real_cd_path = PM.to_real_encoded_path(destination)

                # check if it is a directory
                if not os.path.isdir(real_cd_path):
                    print(f"{destination}: Not a directory")
                    continue

                # check target path is executable
                if not PM.check_permission(real_cd_path, current_user_name, 'x'):
                    print(f"{destination}: Permission denied")
                    continue
                
                # cd to destination
                current_path = destination
            
            elif cmd == "mkdir":

                # get target folder
                if len(argv) == 0:
                    print("PLease specify folder name.")
                    continue
                file_name = argv[0]
                real_file_path = os.path.join(
                    PM.to_real_encoded_path(current_path),
                    encryptor.encrypt_data(file_name)
                )

                # ensure folder does not exists
                try:
                    PM.to_real_encoded_path(os.path.join(current_path, file_name))
                    print(f"{file_name}: Folder already exists")
                    continue
                except:
                    pass

                # check write permission of current directory
                if not PM.check_permission(
                    PM.to_real_encoded_path(current_path),
                    current_user_name, 'w'
                ):
                    print(f"{file_name}: Permission denied")
                    continue

                # make the folder
                PM.create_folder(real_file_path, current_user_name)

            elif cmd == "touch":

                # get target file
                if len(argv) == 0:
                    print("PLease specify folder name.")
                    continue
                file_name = argv[0]
                real_file_path = os.path.join(
                    PM.to_real_encoded_path(current_path),
                    encryptor.encrypt_data(file_name)
                )

                # ensure file does not exists
                try:
                    PM.to_real_encoded_path(os.path.join(current_path, file_name))
                    print(f"{file_name}: File already exists")
                    continue
                except:
                    pass

                # check write permission of current directory
                if not PM.check_permission(
                    PM.to_real_encoded_path(current_path),
                    current_user_name, 'w'
                ):
                    print(f"{file_name}: Permission denied")
                    continue

                # make the file and write an empty
                PM.create_file(real_file_path, current_user_name)
                PM.write_file(real_file_path, "")
            
            elif cmd == "cat":

                # get target file
                if len(argv) == 0:
                    print("PLease specify file name.")
                    continue
                file_path = os.path.join(current_path, argv[0])
                real_file_path = PM.to_real_encoded_path(file_path)

                # check if it is file
                if not os.path.isfile(real_file_path):
                    print(f"{argv[0]}: Not a file")
                    continue

                # check read permission
                if not PM.check_permission(real_file_path, current_user_name, 'r'):
                    print(f"{argv[0]}: Permission denied")
                    continue

                # read file
                print(PM.read_file(real_file_path))
            
            elif cmd == "echo":

                # get target file
                if len(argv) < 2:
                    print("PLease specify file name and message.")
                    continue
                file_path = os.path.join(current_path, argv[0])
                real_file_path = PM.to_real_encoded_path(file_path)

                # check write permission
                if not PM.check_permission(real_file_path, current_user_name, 'w'):
                    print(f"{argv[0]}: Permission denied")
                    continue

                # write to file
                write_content = " ".join(argv[1:])
                PM.write_file(real_file_path, write_content)

            elif cmd == "mv":

                # get target path
                if len(argv) < 2:
                    print("Please specify original and new file/folder name.")
                    continue
                target_path = os.path.join(current_path, argv[0])
                real_path = PM.to_real_encoded_path(target_path)

                # check write permission
                if not PM.check_permission(real_path, current_user_name, 'w'):
                    print(f"{argv[0]}: Permission denied")
                    continue

                # check if renamed file/folder exists
                renamed_path = os.path.join(current_path, argv[1])
                try:
                    PM.to_real_encoded_path(renamed_path)
                    print(f"{argv[1]}: Already exists")
                    continue
                except:
                    pass

                # rename file/folder
                real_renamed_path = os.path.join(
                    PM.to_real_encoded_path(current_path),
                    encryptor.encrypt_data(argv[1])
                )
                os.rename(real_path, real_renamed_path)

            elif cmd == "chmod":

                # get new permission and permission path
                if len(argv) < 2:
                    print("Please specify new permission and file/folder name.")
                    continue
                new_permission = int(argv[0])
                target_path = os.path.join(current_path, argv[1])
                real_path = PM.to_real_encoded_path(target_path)

                # check execute permission
                if not PM.check_permission(real_path, current_user_name, 'x'):
                    print(f"{argv[1]}: Permission denied")
                    continue

                # change permission
                old_permission = PM.get_path_permission(real_path)
                old_permission["permission"] = new_permission
                PM.set_path_permission(real_path, old_permission)


        except Exception as e:
            print("error occurred")
            print(e)
            continue
                    