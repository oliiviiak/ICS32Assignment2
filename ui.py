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
    start_choice = input("Enter 'C' to create a new file, 'O' to open, or 'admin' for command mode: ").strip()

    if start_choice.lower() == "admin":
        run_admin_mode()
    elif start_choice.upper() == "C":
        create_profile()
    elif start_choice.upper() == "O":
        open_profile()
    else:
        print("Invalid command.")


def run_admin_mode():


def create_profile():
    path_str = input("Enter directory path: ").strip()
    name = input("Enter filename: ").strip()

    if not name.endswith(".dsu"):
        name += ".dsu"
    
    current_path = Path(path_str) / name

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    bio = input("Enter bio: ").strip()

    # if there's a space in the username or password
    if " " in username or " " in password:
        print("ERROR: Username and password cannot contain spaces.")
        return
    
    current_profile = Profile(username, password)
    current_profile.bio = bio
    current_profile.save_profile(str(current_path))
    print(f"Profile created and saved to {current_path}")


def open_profile():


def edit_profile():
