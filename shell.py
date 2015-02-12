
# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import os
import sys
from segmenter import Segmenter


# --------------------------------------------------------------------------------
# Globals.
# --------------------------------------------------------------------------------

_seg = None
_INTRO = '''Nau mai, haere mai ki te Segmenter testing shell.
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
        global _INTRO
        print(_INTRO)
    elif user_input.startswith("prob(") and user_input.endswith(")"):
        user_input = user_input.lstrip("prob(").rstrip(")")
        args = user_input
        args = args.split(",")
        for i in range(len(args)):
            args[i] = args[i].lstrip().rstrip()
            args[i] = args[i].lstrip('"').rstrip('"').lstrip("'").rstrip("'")
        global _seg
        prob = _seg.prob(args)
        print(prob)
    elif user_input.endswith(")"):
        print("Unrecognised command.")
    else:
        global _seg
        print(_seg.segment(user_input))


# --------------------------------------------------------------------------------
# Main.
# --------------------------------------------------------------------------------

def abort(errmsg):
    print(errmsg)
    print("Closing....")
    sys.exit(1)

def main():

    # defaults
    fpath_frequencies = "frequencies.txt"
    fpath_ngrams = None
    # fpath_ngrams = "3grams.txt"

    # parse arguments
    args = sys.argv[1:]
    for arg in args:

        if arg == "-simple":
            fpath_ngrams = None

    # validate filepaths
    for fpath in [fpath_frequencies, fpath_ngrams]:
        if fpath and not os.path.isfile(fpath):
            print("Error: could not find " + fpath)
            sys.exit(1)

    # initialise segmenter
    print("Loading Segmenter.")
    global _seg
    _seg = Segmenter(fpath_frequencies, fpath_ngrams)

    # show intro msg
    clear()
    global _INTRO
    print(_INTRO)

    # read, eval
    while (True):
        user_input = str(input("> "))
        eval(user_input)

if __name__ == '__main__':
    main()