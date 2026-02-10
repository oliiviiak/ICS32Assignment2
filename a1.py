# Olivia Kong
# oykong@uci.edu
# 92692989

from pathlib import Path
import shlex


# helper method for printing paths
def print_values(list_name):
    for item in list_name:
        print(item)


# L command
def list_files(path):
    p = Path(path)
    all_files = []
    all_dirs = []

    for item in p.iterdir():
        if item.is_file():
            all_files.append(item)
        else:
            all_dirs.append(item)

    print_values(all_files)
    print_values(all_dirs)


# L -r command
def list_recursively(path):
    p = Path(path)
    all_files_dirs = []

    def recurse_dir(directory):
        for item in directory.iterdir():
            all_files_dirs.append(item)
            if item.is_dir():
                recurse_dir(item)

    recurse_dir(p)
    print_values(all_files_dirs)


# L -f command
def list_only_files(path):
    p = Path(path)
    all_files = []

    for item in p.iterdir():
        if item.is_file():
            all_files.append(item)

    print_values(all_files)


# L -r -f command
def list_only_files_recursively(path):
    p = Path(path)
    all_files = []

    def recurse_dir(directory):
        for item in directory.iterdir():
            if item.is_file():
                all_files.append(item)
            elif item.is_dir():
                recurse_dir(item)

    recurse_dir(p)
    print_values(all_files)


# L -s command
def list_exact_filename(path, file_name):
    p = Path(path)
    all_files = []

    for item in p.iterdir():
        if item.is_file() and item.name == file_name:
            all_files.append(item)

    print_values(all_files)


# L -r -s command
def list_exact_filename_recursively(path, file_name):
    p = Path(path)
    all_files = []

    def recurse_dir(directory):
        for item in directory.iterdir():
            if item.is_file() and item.name == file_name:
                all_files.append(item)
            elif item.is_dir():
                recurse_dir(item)

    recurse_dir(p)
    print_values(all_files)


# L -e command
def list_files_extensions(path, extension_name):
    p = Path(path)
    all_files = []

    for item in p.iterdir():
        if item.is_file() and item.suffix[1:] == extension_name:
            all_files.append(item)

    print_values(all_files)


# L -r -e command
def list_files_extensions_recursively(path, extension_name):
    p = Path(path)
    all_files = []

    def recurse_dir(directory):
        for item in directory.iterdir():
            if item.is_file() and item.suffix[1:] == extension_name:
                all_files.append(item)
            elif item.is_dir():
                recurse_dir(item)

    recurse_dir(p)
    print_values(all_files)


# # C -n command
def create_new_file_in_dir(path, file_name):
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"Error: the path {path} was not found.")
    if not p.is_dir():
        raise NotADirectoryError(f"Error: the path {path} is not a directory.")

    dsu_filename = f"{file_name}.dsu"
    file_path = p / dsu_filename

    file_path.touch()
    print(file_path)


# # D command
def delete_dsu_file(file_path):
    p = Path(file_path)

    if not p.exists():
        raise FileNotFoundError(f"ERROR")
    if not p.is_file():
        raise ValueError(f"Error: the path {file_path} is not a file.")
    if p.suffix != ".dsu":
        raise ValueError("ERROR")

    p.unlink()
    print(f"{file_path} DELETED")


# # R command
def read_dsu_file(file_path):
    p = Path(file_path)

    if not p.exists():
        raise FileNotFoundError(f"Error: the file {file_path} was not found.")
    if not p.is_file():
        raise ValueError(f"Error: the path {file_path} is not a file.")
    if p.suffix != ".dsu":
        raise ValueError("ERROR")

    content = p.read_text()

    if not content:
        print("EMPTY")
    else:
        print(content, end='')


# helper method for receiving input correctly for L
def parse_L_command(full_input):
    if len(full_input) < 2:
        return None, None

    option_start_index = len(full_input)
    for i in range(2, len(full_input)):
        if full_input[i].startswith('-'):
            option_start_index = i
            break

    path = " ".join(full_input[1: option_start_index])
    if option_start_index < len(full_input):
        options = full_input[option_start_index:]
    else:
        options = []

    return path, options


# helper method for receiving input correctly for C
def parse_C_command(full_input):
    if len(full_input) < 4:
        return None, None

    option_start_index = -1
    for i in range(2, len(full_input)):
        if full_input[i] == '-n':
            option_start_index = i
            break

    if option_start_index == -1 or option_start_index == len(full_input) - 1:
        return None, None

    path = " ".join(full_input[1: option_start_index])
    filename = full_input[option_start_index + 1]

    return path, filename


def main():

    while True:

        user_input = input().strip()

        if not user_input:
            continue

        try:
            full_input = shlex.split(user_input)
            command = full_input[0]

            if command == "Q":
                break

            elif command == "L":
                path, option = parse_L_command(full_input)

                if path is None:
                    print("ERROR")
                    continue

                # recursive functions
                if len(option) == 0:
                    list_files(path)
                elif option[0] == "-r":
                    if len(option) == 1:
                        list_recursively(path)
                    elif option[1] == "-f":
                        list_only_files_recursively(path)
                    elif option[1] == "-s" and len(option) > 2:
                        list_exact_filename_recursively(path, option[2])
                    elif option[1] == "-e" and len(option) > 2:
                        list_files_extensions_recursively(path, option[2])
                    else:
                        print("ERROR")

                # non-recursive functions
                elif option[0] == "-f":
                    list_only_files(path)
                elif option[0] == "-s" and len(option) > 1:
                    list_exact_filename(path, option[1])
                elif option[0] == "-e" and len(option) > 1:
                    list_files_extensions(path, option[1])
                else:
                    print("ERROR")

            elif command == "C":
                path, name = parse_C_command(full_input)
                if path is None or name is None:
                    print("ERROR")
                    continue
                create_new_file_in_dir(path, name)

            elif command == "D":
                if len(full_input) < 2:
                    print("ERROR")
                    continue

                file_path = " ".join(full_input[1:])
                delete_dsu_file(file_path)

            elif command == "R":
                if len(full_input) < 2:
                    print("ERROR")
                    continue

                file_path = " ".join(full_input[1:])
                read_dsu_file(file_path)

            else:
                print("ERROR")

        except FileNotFoundError as e:
            print(str(e))
        except NotADirectoryError as e:
            print(str(e))
        except PermissionError as e:
            print(f"Error: Permission denied.")
        except ValueError as e:
            print(str(e))
        except Exception:
            print("ERROR")


if __name__ == "__main__":
    main()
