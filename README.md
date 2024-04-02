# Project 2: SFS-CodeFusion

## Deployment Instructions

To deploy the Secure File System (SFS) successfully, please follow these steps:

1. Establish a connection to the instance with the IP address `10.2.9.68` hosted on Cybera.
2. Obtain the SFS codebase from its GitHub repository: [SFS-CodeFusion](https://github.com/CoasterJX/SFS-CodeFusion).
3. After downloading the repository, navigate to the SFS-CodeFusion directory using the command `cd /path/to/SFS-CodeFusion`.
4. Initiate the SFS by executing the command `python SFS.py`.
5. For first-time deployments, the system will prompt for initial setup. Please respond with `y` to proceed. You will receive a file named `SFS-key.pem`. It is crucial to store this file securely as it is used to decrypt the data within the `file-system` directory.

## User Guide

### Admin User Instructions

As an admin user, follow these guidelines to manage the SFS:

- Ensure that the `SFS-key.pem` file is located in the `SFS-CodeFusion/` directory for admin access. Without this key, admin login is not possible.
- To log in as an admin, enter `login` in the SFS command line, then input `admin` as the username when prompted. The presence of `SFS-key.pem` will grant admin access.
- Admin-specific commands include:
  - `create-user`: This command allows you to create a new user. You'll need to provide a username, password, and a comma-separated list of groups the user belongs to. The first group mentioned will be set as the user's default group for file permissions.

Note: Groups are created automatically upon creating a user to avoid unassigned groups. This ensures cleaner management.

### Internal User Instructions

For internal users, the following steps are necessary to use SFS:

- Request an admin to set up your user account with a username, password, and assigned groups.
- To log in, type `login` in the SFS command line and follow the prompts to enter your username and password.
- Supported commands for internal users include:
  - `pwd`: Displays the current directory.
  - `ls`: Lists files and directories in the current location.
  - `cd`: Changes the current directory.
  - `mkdir <folder_name>`: Creates a new folder.
  - `touch <file_name>`: Creates a new file.
  - `cat <file_name>`: Displays the content of a file.
  - `echo <file_name> [contents]`: Writes content to a file.
  - `mv <old_name> <new_name>`: Renames a file or folder.
  - `chmod <permission> <file/folder_name>`: Changes permissions of a file or folder (ownership required).
  - `rm <file/folder_name>`: Removes a file or folder.

### General Guidelines for All Users

- Always log out after your session by typing `logout`.
- Upon login, the system will alert you of any modifications made to files or folders since your last session. Regular backups are recommended as a precaution.

This README serves as a comprehensive guide for deploying and utilizing the SFS-CodeFusion system. For further assistance or inquiries, please refer to the project documentation or contact the system administrator.