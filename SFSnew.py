import os
import getpass
from src2.PathManager import PM

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
            cmd = input(f"{current_user}>>> ").split(" ")
            argv = [] if len(cmd) < 2 else cmd[1:]
            cmd = cmd[0]
            if cmd == "":
                continue
            print("\n")

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

            # internal user access
            elif cmd == "logout":
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
                    pass

        except Exception as e:
            print(e)
            continue
                    