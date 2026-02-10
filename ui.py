# Olivia Kong
# oykong@uci.edu
# 92692989

import shlex
import a1
from pathlib import Path
from Profile import Profile, Post


current_profile = None
current_path = None


def start():
    print("Welcome to the Journaling System!")

    while True:
        user_input = input("\n----Commands-----\n"
                            + "'C' to create a new file\n"
                            + "'O' to open file\n"
                            + "'L' to list the contents\n"
                            + "'D' to delete file\n"
                            + "'R' read contents of file\n"
                            + "'Q' to quit\n"
                            + "'admin' for command mode\n"
                            + "> ").strip()
        
        if not user_input:
            continue

        if user_input.upper() == "Q":
            print("Bye!")
            break

        if user_input.lower() == "admin":
            run_admin_mode()
            break
        elif user_input.upper() == "C":
            create_profile()
        elif user_input.upper() == "O":
            open_profile()
        elif user_input.upper() in ["L", "D", "R"]:
            a1_commands(user_input)
        else:
            print("Invalid command.")


def a1_commands(command):
    print(f"---{command} Command Menu---")
    print(f"Command Format:")
    print(f"[COMMAND] [INPUT] [[-]OPTION] [INPUT]")

    full_command_input = input("Enter full command: ")

    if not full_command_input:
        return
    
    parts = shlex.split(full_command_input)

    if len(parts) < 1:
        print("ERROR: Invalid command.")
        return
    
    cmd_type = parts[0].upper()

    handle_a1_logic(cmd_type, parts)


def handle_a1_logic(command, parts):

    if len(parts) < 2:
        print("ERROR: Invalid command.")
        return
    
    path = parts[1]

    if command == "L":
        if "-r" in parts and "-f" in parts:
            a1.list_only_files_recursively(path)
        elif "-r" in parts:
            a1.list_recursively(path)
        elif "-f" in parts:
            a1.list_only_files(path)
        else:
            a1.list_files(path)
    elif command == "D":
        a1.delete_dsu_file(path)
    elif command == "R":
        a1.read_dsu_file(path)


def run_admin_mode():

    while True:
        admin_input = input().strip()

        if not admin_input:
            continue

        parts = shlex.split(admin_input)
        command = parts[0].upper()

        if parts[0].upper() == "Q":
            break

        handle_admin_logic(command, parts)


def handle_admin_logic(command, parts):
    try:
        # a1 commands
        if command in ["L", "D", "R"]:
            if len(parts) < 2:
                print("ERROR")
                return
            path = parts[1]
            
            if command == "L":
                if "-r" in parts and "-f" in parts:
                    a1.list_only_files_recursively(path)
                elif "-r" in parts:
                    a1.list_recursively(path)
                elif "-f" in parts:
                    a1.list_only_files(path)
                else:
                    a1.list_files(path)
            elif command == "D":
                a1.delete_dsu_file(path)
            elif command == "R":
                a1.read_dsu_file(path)
        # a2 commands
        elif command == "C":
            create_profile(parts)
        elif command == "O":
            open_profile(parts)
        elif command == "E":
            edit_profile(parts)
        elif command == "P":
            print_profile(parts)
        else:
            print("ERROR")
    except Exception:
        print("ERROR")


def create_profile():
    global current_profile, current_path
    path_str = input("Enter directory path: ").strip()
    p = Path(path_str)

    if not p.exists() or not p.is_dir():
        print(f"ERROR: The directory {path_str} is invalid.")
        return
    
    filename = input("Enter filename: ").strip()

    # check if the file path ends in ".dsu"
    if not filename.endswith(".dsu"):
        filename += ".dsu"

    current_path = p / filename

    # if file already exists just open
    if current_path.exists():
        print(f"File already exists. Opening {current_path}")
        open_profile(str(current_path))
        return

    # get profile parameters information
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    bio = input("Enter bio: ").strip()

    # if there's a space in the username or password
    if " " in username or " " in password:
        print("ERROR: Username and password cannot contain spaces.")
        return

    # create Profile object using user inputs
    current_profile = Profile(username=username, password=password)
    current_profile.bio = bio

    try:
        current_path.touch()
        # save profile
        current_profile.save_profile(str(current_path))
        print(f"Profile created and saved to {current_path}")
    except Exception as e:
        print(f"ERROR: {e}")


def open_profile(path_provided=None):
    # if there's a path given
    if path_provided:
        path_str = path_provided
    else:
        # if there's no path given, get path
        path_str = input("Enter the full path to the"
                         + ".dsu file to open: ").strip()

    # load profile with the given path (current_profile)
    file_path = Path(path_str)
    if file_path.suffix == ".dsu" and file_path.exists():
        current_profile = Profile()
        current_profile.load_profile(str(file_path))
        current_path = file_path
        print(f"Opened: {current_path}")
    else:
        print("ERROR: path is invalid.")


def edit_profile(parts):
    # param parts are the parts of the given command

    if current_profile is None:
        print("ERROR: No profile loaded.")
        return

    try:
        # start from index 1 of parts because 0 is E
        i = 1
        while i < len(parts):
            option = parts[i]

            if option == "-usr":
                current_profile.username = parts[i+1]
                i += 2

            elif option == "-pwd":
                current_profile.password = parts[i+1]
                i += 2

            elif option == "-bio":
                current_profile.bio = parts[i+1]
                i += 2

            elif option == "-addpost":
                new_entry = parts[i+1]
                current_profile.add_post(Post(new_entry))
                i += 2

            elif option == "-delpost":
                post_index = int(parts[i+1])
                current_profile.del_post(post_index)
                i += 2

            else:
                i += 1

        current_profile.save_profile(str(current_path))
        print("Profile updated successfully!")

    except (IndexError, ValueError):
        print("ERROR: Invalid format for edit command.")
    except Exception as e:
        print(f"ERROR: {e}")


def print_profile(parts):
    # check if loaded a profile
    if not current_profile:
        print("ERROR")
        return

    # print all option command
    if "-all" in parts:
        print(f"Username: {current_profile.username}")
        print(f"Password: {current_profile.password}")
        print(f"Bio: {current_profile.bio}")
        for i, post in enumerate(current_profile.get_posts()):
            print(f"Post #{i}: {post.entry}")

    else:
        if "-usr" in parts:
            print(f"{current_profile.username}")

        if "-pwd" in parts:
            print(f"{current_profile.password}")

        if "-bio" in parts:
            print(f"{current_profile.bio}")

        if "-posts" in parts:
            for i, post in enumerate(current_profile.get_posts()):
                print(f"Post #{i}: {post.entry}")

        if "-post" in parts:
            try:
                # find index of the option,
                # then look at the index next to it (for post index)
                option_index = parts.index("-post")
                post_index = int(parts[[option_index + 1]])

                posts = current_profile.get_posts()
                # check if post index is valid
                if 0 <= post_index < len(posts):
                    print(posts[post_index].entry)
                else:
                    print("ERROR: post index invalid.")

            except (ValueError, IndexError):
                print("ERROR")
