
# --------------------------------------------------------------------------------
# Imports.
# --------------------------------------------------------------------------------

import sys
import os
import codecs


# --------------------------------------------------------------------------------
# Constants.
# --------------------------------------------------------------------------------

__GRAMMAR = ["the", "and"]
__VALID_CHARS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n",
                "o","p","q","r","s","t","u","v","w","x","y","z","-"]
__ENCODING = "latin-1"
MIN_DEGREE = 4


# --------------------------------------------------------------------------------
# Functions.
# --------------------------------------------------------------------------------

def _valid(*words):
    for word in words:
        if len(word) < 3 or word in __GRAMMAR:
            return False
        for char in word:
            if char not in __VALID_CHARS:
                return False
    return True


def load_frequencies(fname):
    """
    Load string frequency counts from a file into a Trie and return.
    :rtype : Trie
    """

    # output
    print("Loading " + fname)

    # get frequency counts
    words = {}
    count = 0
    with codecs.open(fname, "r", __ENCODING) as f:
        for line in f:

            # parse line
            line = line.lstrip().rstrip().split()
            word = line[0].lower()
            freq = int(line[1])

            # validate word
            if not _valid(word):
                continue

            # add to map
            words[word] = freq
            count += freq

    # normalise, return
    for word in words:
        words[word] = words[word] / count
    print("Finished loading " + fname + ".")
    return words

def load_3grams(fname):
    """
    Load all 3 grams from a file into a
    Load all words from the specified file into a Trie and return.
    :rtype : Trie
    """

    # output
    print("Loading " + fname)

    # get frequency counts
    grams = dict(dict(dict()))
    count = 0
    def add3gram(s1, s2, s3):
        if s1 not in grams:
            toadd = { s2 : { s3 : 1 } }
            if not isinstance(toadd, dict):
                raise TypeError()
            grams[s1] = { s2 : { s3 : 1 } }
        else:
            grams[s1][s2][s3] += 1

    count = 0
    with codecs.open(fname, "r", __ENCODING) as f:
        for line in f:

            # parse line
            line = line.lstrip().rstrip().split("\t")
            freq = int(line[0])
            w1 = line[0].lower()
            w2 = line[1].lower()
            w3 = line[2].lower()

            # validate ngrams
            if not _valid(w1,w2,w3) :
                continue

            # add to map
            add3gram(w1, w2, w3)
            count += freq

    print(len(grams))

    # normalise, return
    for w1 in grams:
        for w2 in grams[w1]:
            for w3 in grams[w1][w2]:
                grams[w1][w2][w3] = grams[w1][w2][w3] / count

    # show progress
    print("Finished loading " + fname + ".")
    print(type(grams))

    return grams
