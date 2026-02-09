# Olivia Kong
# oykong@uci.edu
# 92692989

import shlex
from pathlib import Path
from Profile import Profile, Post

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


def open_profile():


def edit_profile():
