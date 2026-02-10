ICS32 Assignment 2: Journal

Program Description:
    This Python program is a journaling system that allows users
    to create, manage, and store journal entries in .dsu files.
    The program supports creating profiles with usernames,
    passwords, bios, and adding and deleting journal posts.

    a2.py: Main module for the program.
    ui.py: User interface module, handles both admin and
    user friendly modes.
    Profile.py: File to manage saving and loading of user data. Do not edit.
    a1.py: Contains all the logic for L, D, R commands.

How to Run:
    python3 a2.py

All Commands:
    L - List the contents of the user specified directory.
    Q - Quit the program.
    C - Create a new .dsu file in the specified directory.
    O - Open existing .dsu file
    D - Delete .dsu file.
    R - Read the contents of a .dsu file.
    E - Edit an open user profile.
    P - Print contents of open user profile.

Options of the 'L' command:
    -r Output directory content recursively.
    -f Output only files, excluding directories in the results.
    -s Output only files that match a given file name.
    -e Output only files that match a given file extension.

Options for 'C' command:
    -n allows the user to specify the name of the file.

Options for 'E' command:
    -usr Edit the username.
    -pwd Edit the password.
    -bio Edit the bio.
    -addpost Add a new post to profile.
    -delpost Delete post by index.

Options for 'P' command:
    -usr Print the username.
    -pwd Print the password.
    -bio Print the bio.
    -posts Print all posts.
    -post < index > Print post by index.
    -all Print all contents of profile.
