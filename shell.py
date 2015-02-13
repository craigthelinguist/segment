
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
        prob = __seg.prob(args)
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

    # defaults
    fpath_frequencies = "frequencies.txt"
    fpath_grams = None

    # parse arguments
    args = sys.argv[1:]
    for arg in args:
        if arg == "-simple":
            fpath_ngrams = None

    # validate filepaths
    if not os.path.isfile(fpath_frequencies):
        abort("Could not find frequencies.txt")
    if not fpath_grams or not os.path.isfile(fpath_grams):
        print("Could not find 3grams.txt, loading without 3grams.")

    # initialise segmenter
    print("Loading Segmenter.")
    global __seg
    __seg = Segmenter(fpath_frequencies, fpath_grams)

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