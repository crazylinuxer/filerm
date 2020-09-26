import os
import sys


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
    "directory": "./"
}


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
