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
                           + "'E' to edit file\n"
                           + "'P' to print file\n"
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
        elif user_input.upper() == "E":
            friendly_edit()
        elif user_input.upper() == "P":
            friendly_print()
        elif user_input.upper() in ["L", "D", "R"]:
            a1_commands(user_input)
        else:
            print("ERROR: Invalid command.")


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
        try:
            admin_input = input().strip()

            if not admin_input:
                continue

            if admin_input.upper() == "Q":
                break

            parts = shlex.split(admin_input)
            command = parts[0].upper()

            if command == "C":
                handle_create(parts)
            elif command == "O":
                if len(parts) > 1:
                    open_profile(parts)
            elif command == "E":
                handle_edit(parts)
            elif command == "P":
                handle_print(parts)
            elif command == 'L':
                handle_list(parts)
            elif command == 'D':
                handle_delete(parts)
            elif command == 'R':
                handle_read(parts)
            else:
                print("ERROR")

        except Exception:
            print("ERROR")


def handle_create(parts):
    global current_path, current_profile

    try:
        if "-n" not in parts:
            print("ERROR")
            return

        name_index = parts.index("-n")
        if name_index + 1 >= len(parts):
            print("ERROR")
            return

        path_str = " ".join(parts[1:name_index]).strip('"').strip("'")
        p = Path(path_str)

        if not p.exists() or not p.is_dir():
            print("ERROR")
            return

        filename = parts[name_index + 1].strip('"').strip("'")

        if not filename.endswith(".dsu"):
            filename += ".dsu"

        current_path = p / filename
        current_path.touch(exist_ok=True)

        current_profile = Profile()
        current_profile.username = ""
        current_profile.password = ""
        current_profile.bio = ""

        current_profile.save_profile(str(current_path))
        print(current_path)

    except Exception:
        print("ERROR")


def handle_edit(parts):
    # param parts are the parts of the given command
    global current_path, current_profile
    if not current_profile or not current_path:
        print("ERROR")
        return

    try:
        # start from index 1 of parts because 0 is E
        i = 1
        while i < len(parts):
            arg = parts[i]

            if arg == "-usr" and i + 1 < len(parts):
                current_profile.username = parts[i+1]
                i += 2
            elif arg == "-pwd" and i + 1 < len(parts):
                current_profile.password = parts[i+1]
                i += 2
            elif arg == "-bio" and i + 1 < len(parts):
                current_profile.bio = parts[i+1]
                i += 2
            elif arg == "-addpost" and i + 1 < len(parts):
                new_post = Post(parts[i+1])
                current_profile.add_post(new_post)
                i += 2
            elif arg == "-delpost" and i + 1 < len(parts):
                try:
                    index = int(parts[i+1])
                    current_profile.del_post(index)
                except (ValueError, IndexError):
                    print("ERROR: Invalid post ID")
                    return
                i += 2
            else:
                print("ERROR")
                return

        current_profile.save_profile(current_path)

    except Exception:
        print("ERROR")


def handle_print(parts):
    if not current_profile:
        print("ERROR")
        return

    if "-all" in parts:
        print(f"Username: {current_profile.username}")
        print(f"Password: {current_profile.password}")
        print(f"Bio: {current_profile.bio}")
        for i, post in enumerate(current_profile.get_posts()):
            print(f"Post {i}: {post.entry}")
        return

    if "-usr" in parts:
        print(current_profile.username)
    if "-pwd" in parts:
        print(current_profile.password)
    if "-bio" in parts:
        print(current_profile.bio)
    if "-posts" in parts:
        for i, post in enumerate(current_profile.get_posts()):
            print(f"Post {i}: {post.entry}")
    if "-post" in parts:
        try:
            idx = int(parts[parts.index("-post") + 1])
            posts = current_profile.get_posts()
            print(posts[idx].entry)
        except Exception:
            print("ERROR")


def handle_list(parts):
    path, options = a1.parse_L_command(parts)
    if path is None:
        print("ERROR")
        return

    try:
        if len(options) == 0:
            a1.list_files(path)
        elif options[0] == "-r":
            if len(options) == 1:
                a1.list_recursively(path)
            elif options[1] == "-f":
                a1.list_only_files_recursively(path)
            elif options[1] == "-s" and len(options) > 2:
                a1.list_exact_filename_recursively(path, options[2])
            elif options[1] == "-e" and len(options) > 2:
                a1.list_files_extensions_recursively(path, options[2])
            else:
                print("ERROR")
        elif options[0] == "-f":
            a1.list_only_files(path)
        elif options[0] == "-s" and len(options) > 1:
            a1.list_exact_filename(path, options[1])
        elif options[0] == "-e" and len(options) > 1:
            a1.list_files_extensions(path, options[1])
        else:
            print("ERROR")
    except Exception:
        print("ERROR")


def handle_delete(parts):
    if len(parts) > 1:
        file_path = " ".join(parts[1:])

        try:
            a1.delete_dsu_file(file_path)
        except Exception:
            print("ERROR")
    else:
        print("ERROR")


def handle_read(parts):
    if len(parts) > 1:
        file_path = " ".join(parts[1:])
        try:
            a1.read_dsu_file(file_path)
        except Exception:
            print("ERROR")
    else:
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
    current_profile.save_profile(str(current_path))

    try:
        current_path.touch()
        print(f"Profile created and saved to {current_path}")
    except Exception as e:
        print(f"ERROR: {e}")


def open_profile(parts):
    global current_profile, current_path

    try:
        path_str = " ".join(parts[1:]).strip('"').strip("'")

        if not path_str:
            print("ERROR")
            return

        file_path = Path(path_str)

        if file_path.suffix == ".dsu" and file_path.exists():
            current_profile = Profile()
            current_profile.load_profile(str(file_path))
            current_path = file_path
            print(f"Opened: {current_path}")
        else:
            print("ERROR")
    except Exception:
        print("ERROR")


def edit_profile(parts):
    global current_profile, current_path
    # param parts are the parts of the given command

    if current_profile is None:
        print("ERROR: No profile loaded.")
        return

    try:
        # start from index 1 of parts because 0 is E
        i = 1
        while i < len(parts):
            option = parts[i]
            if i + 1 >= len(parts):
                break

            val = parts[i+1]

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
                if val.strip():
                    current_profile.add_post(Post(val))
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
    global current_profile, current_path
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
                post_index = int(parts[option_index + 1])

                posts = current_profile.get_posts()
                # check if post index is valid
                if 0 <= post_index < len(posts):
                    print(posts[post_index].entry)
                else:
                    print("ERROR: post index invalid.")

            except (ValueError, IndexError):
                print("ERROR")


def friendly_edit():
    global current_profile

    if not current_profile:
        print("\nERROR: No journal open.")
        return

    print("---Edit Journal---")
    print("Options: -usr, -pwd, -bio, -addpost, -delpost")

    user_input = input("Enter edit command: ").strip()

    if not user_input:
        return

    parts = ["E"] + shlex.split(user_input)
    edit_profile(parts)


def friendly_print():
    global current_profile

    if not current_profile:
        print("\nERROR: No journal open.")
        return

    print("---Print Journal---")
    print("Options: -all, -usr, -pwd,"
          + " -bio, -posts, -post <id>")

    user_input = input("Enter print command: ").strip()

    if not user_input:
        return

    parts = ["P"] + shlex.split(user_input)
    print_profile(parts)
