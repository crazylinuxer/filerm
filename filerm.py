from typing import Iterable
import os
import sys
import re


def print_help():
    with open("help.txt") as file:
        print(file.read())


def exit_on_syntax_error():
    print("Invalid command line parameters detected!", file=sys.stderr, end="\n\n")
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


skip = False

for i in range(1, len(sys.argv)):
    if skip:
        skip = False
        continue
    if sys.argv[i][0] == '-':
        if len(sys.argv[i]) == 1:
            if i >= len(sys.argv) - 1:
                parameters["directory"] = sys.argv[i]
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
                    skip = True
                else:
                    exit_on_syntax_error()
        else:
            for param in range(1, len(sys.argv[i])):
                if sys.argv[i][param] == "h":
                    parameters["help"] = True
                elif sys.argv[i][param] == "r":
                    parameters["recursively"] = True
                elif sys.argv[i][param] == "i":
                    parameters["hidden"] = True
                elif sys.argv[i][param] == "p":
                    if i + 1 <= len(sys.argv):
                        parameters["pattern"] = sys.argv[i + 1]
                        skip = True
                    else:
                        exit_on_syntax_error()
                else:
                    exit_on_syntax_error()
    elif i >= len(sys.argv) - 1:
        parameters["directory"] = sys.argv[i]
    else:
        exit_on_syntax_error()


if parameters["help"]:
    print_help()
    exit(0)


def append_if_not_hidden(directory: str, file: str):
    if file[0] == '.':
        if parameters["hidden"]:
            files_to_delete.append(os.path.join(directory, file))
    else:
        files_to_delete.append(os.path.join(directory, file))


def append_files(directory: str, files: Iterable[str]):
    for file in files:
        if parameters["pattern"]:
            if re.fullmatch(parameters["pattern"], file):
                append_if_not_hidden(directory, file)
        else:
            append_if_not_hidden(directory, file)


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
        print("Done!")
    else:
        print("Cancelled")

