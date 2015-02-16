
# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import os
import sys
from segmenter import Segmenter


# --------------------------------------------------------------------------------
# Globals.
# --------------------------------------------------------------------------------

__seg = None
__INTRO = '''Nau mai, haere mai ki te Segmenter testing shell.
Type a word and its English segmentation will be displayed.
Type help() to show all commands.'''

# --------------------------------------------------------------------------------
# Functions for I/O.
# --------------------------------------------------------------------------------

def clear():
    """
    Clear the terminal.
    :rtype : None
    """
    in_terminal = os.getenv("TERM")
    if not in_terminal:
        for i in range(80):
            print(chr(27) + "[2J") # escape sequence
    else:
        os.system("cls" if os.name == "nt" else "clear")

def eval(user_input):
    """
    Evaluate the user input. if they typed in a key-word, such as help(), then it will be executed.
    Otherwise the word they entered will be segmented and displayed to the console.
    :rtype : None
    """
    if user_input == "exit()":
        print("Closing....")
        sys.exit(0)
    elif user_input == "clear()":
        clear()
    elif user_input == "help()":
        print()
        print("============")
        print("  Commands  ")
        print("============")
        print("clear()\n\tClear console.")
        print("exit()\n\tQuit program.")
        print("help()\n\tDisplay commands.")
        print("intro()\n\tDisplay instructions again.")
        print("prob(s)\n\tGet probability of s.")
        print("prob(a,b,c)\n\tGet probability of a,b,c appearing in that order.")
        print()
    elif user_input == "intro()":
        global __INTRO
        print(__INTRO)
    elif user_input.startswith("prob(") and user_input.endswith(")"):
        user_input = user_input.lstrip("prob(").rstrip(")")
        args = user_input
        args = args.split(",")
        for i in range(len(args)):
            args[i] = args[i].lstrip().rstrip()
            args[i] = args[i].lstrip('"').rstrip('"').lstrip("'").rstrip("'")
        global __seg
        prob = __seg.prob(*args)
        print(prob)
    elif user_input.endswith(")"):
        print("Unrecognised command.")
    else:
        global __seg
        print(__seg.segment(user_input))


# --------------------------------------------------------------------------------
# Main.
# --------------------------------------------------------------------------------

def abort(errmsg):
    print(errmsg)
    print("Closing....")
    sys.exit(1)

def main():

    # default fpaths
    ngrams1 = "1grams.txt"
    ngrams2 = "2grams.txt"

    # parse arguments
    args = sys.argv[1:]
    for arg in args:
        if arg == "-simple":
            ngrams2 = None

    # check existence of 1grams
    if not os.path.isfile("1grams.txt"):
        print("Error: could not find 1grams.txt.")
        print("Exiting....")
        sys.exit(1)

    # check existence of 2grams and 3grams
    if ngrams2 and not os.path.isfile(ngrams2):
        print("Could not find some files.")
        print("Segmenter will run without use of 2grams and 3grams.")
        ngrams2 = None

    # make segmenter
    global __seg
    __seg = Segmenter(ngrams1, fpath_2grams=ngrams2)

    # show intro msg
    clear()
    global __INTRO
    print(__INTRO)
    print("hello, world!")

    # read, eval
    while (True):
        user_input = str(input("> "))
        eval(user_input)

if __name__ == '__main__':
    main()