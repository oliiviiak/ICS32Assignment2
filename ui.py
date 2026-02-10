# Olivia Kong
# oykong@uci.edu
# 92692989

import shlex
from pathlib import Path
from Profile import Profile, Post


current_profile = None
current_path = None


def start():
    print("Welcome to the Journaling System!")
    start_choice = input("Enter 'C' to create a new file,"
                         + " 'O' to open, or 'admin' for command"
                         + " mode: ").strip()

    if start_choice.lower() == "admin":
        run_admin_mode()
    elif start_choice.upper() == "C":
        create_profile()
    elif start_choice.upper() == "O":
        open_profile()
    else:
        print("Invalid command.")


# def run_admin_mode():


def create_profile():
    global current_profile, current_path
    path_str = input("Enter directory path: ").strip()
    p = Path(path_str)
    filename = input("Enter filename: ").strip()

    if not p.exists() or not p.is_dir():
        print(f"ERROR: The directory {path_str} is invalid.")
        return

    # check if the file path ends in ".dsu"
    if not filename.endswith(".dsu"):
        filename += ".dsu"

    current_path = p / filename

    # get profile parameters information
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    bio = input("Enter bio: ").strip()

    # if there's a space in the username or password
    if " " in username or " " in password:
        print("ERROR: Username and password cannot contain spaces.")
        return

    # create Profile object using user inputs
    current_profile = Profile(username, password)
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
