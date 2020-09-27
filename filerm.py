from typing import Iterable
import os
import sys
import re


def print_help():
    with open("help.txt") as file:
        print(file.read())


def exit_on_syntax_error():
    print("Invalid command line parameters detected!", file=sys.stderr)
    print_help()
    exit(1)


parameters = {
    "help": False,
    "recursively": False,
    "hidden": False,
    "pattern": None,
    "directory": os.path.curdir
}


files_to_delete = []


for i in range(1, len(sys.argv)):
    if sys.argv[i][0] == '-':
        if len(sys.argv[i]) == 1:
            if i >= len(sys.argv) - 1:
                parameters["directory"] = sys.argv[i]
            elif i > 1 and (
                sys.argv[i - 1] == "--pattern" or (
                    sys.argv[i - 1][0] == '-' and
                    sys.argv[i - 1][1] != '-' and
                    'p' in sys.argv[i - 1]
                )
            ):
                pass
            else:
                exit_on_syntax_error()
        elif sys.argv[i][1] == '-':
            if sys.argv[i] == "--help":
                parameters["help"] = True
            elif sys.argv[i] == "--recursively":
                parameters["recursively"] = True
            elif sys.argv[i] == "--hidden":
                parameters["hidden"] = True
            elif sys.argv[i] == "--pattern":
                if i >= len(sys.argv) - 1:
                    parameters["directory"] = sys.argv[i]
                elif i + 1 <= len(sys.argv):
                    parameters["pattern"] = sys.argv[i + 1]
                else:
                    exit_on_syntax_error()
        else:
            for param in range(1, len(sys.argv[i])):
                if param == "h":
                    parameters["help"] = True
                elif param == "r":
                    parameters["recursively"] = True
                elif param == "i":
                    parameters["hidden"] = True
                elif param == "p":
                    if i + 1 <= len(sys.argv):
                        parameters["pattern"] = sys.argv[i + 1]
                    else:
                        exit_on_syntax_error()

if parameters["help"]:
    print_help()
    exit(0)


def append_files(directory: str, files: Iterable[str]):
    for file in files:
        if parameters["pattern"] and re.fullmatch(parameters["pattern"], file):
            if file[0] == '.':
                if parameters["hidden"]:
                    files_to_delete.append(os.path.join(directory, file))
            else:
                files_to_delete.append(os.path.join(directory, file))


if parameters["recursively"]:
    for directory_path, directory_names, file_names in os.walk(parameters["directory"]):
        append_files(directory_path, file_names)
else:
    append_files(
        parameters["directory"],
        (
            file for file in os.listdir(parameters["directory"]) if
            os.path.isfile(os.path.join(parameters["directory"], file))
        )
    )


if files_to_delete:
    print("The following files will be removed:")
    for file_name in files_to_delete:
        print(file_name)
    answer = input("Proceed? [y/N] ")
    if answer in ('y', 'Y', 'д', 'Д'):
        for file_name in files_to_delete:
            try:
                os.remove(file_name)
            except PermissionError:
                print(f"Failed to remove {file_name} (permission denied)", file=sys.stderr)
            except FileNotFoundError:
                print(f"Failed to remove {file_name} (file does not exist)", file=sys.stderr)
    else:
        print("Cancelled")

