

# --------------------------------------------------------------------------------
# Imports.
# --------------------------------------------------------------------------------

import os
import sys
import loader

# --------------------------------------------------------------------------------
# Globals.
# --------------------------------------------------------------------------------

IGNORE = ["the", "and"]
MINSIZE = 3

# --------------------------------------------------------------------------------
# Clases.
# --------------------------------------------------------------------------------

class Segmenter(object):

    # instance variables
    __1grams = None
    __2grams = None

    def __init__(self, fpath_1grams, fpath_2grams=None):
        self.__1grams = loader.load_ngrams(fpath_1grams, 1, min_ngram_size=MINSIZE, ignore=IGNORE)
        if fpath_2grams:
            self.__2grams = loader.load_ngrams(fpath_2grams, 2, min_ngram_size=MINSIZE, ignore=IGNORE)

    def prob(self, *words):
        """
        Get the probability of the specified n-grams.
        Raises ValueError if you pass in an illegal number of n-grams.
        :rtype : float
        """
        if len(words) == 1:
            word = words[0]
            if word in self.__1grams:
                return self.__1grams[word]
            else: return 0.0

        elif len(words) == 2:
            word1 = words[0]
            word2 = words[1]
            if word1 in self.__2grams and word2 in self.__2grams[word1]:
                return self.__2grams[word1][word2]
            else: return 0.0

        else:
            raise ValueError("Invalid number of arguments passed.")

    def segment(self, string):
        """
        Attempt to segment the given string into its English word components.
        Return the string with its components delimited by '-'
        :rtype : str
        """
        segmentation = self.__slice(string, len(string)-1)
        if self.__2grams:
            return self.__combine(segmentation)
        else:
            return segmentation

    def __slice(self, string, degree):

        # base case
        if degree < MINSIZE: return string

        # keep track of the most probable substring in this word. the first character
        # of this string will be at string[pivot].
        pr_string = self.prob(string)
        pr_pivot = 2.0
        pivot = -1

        # find all strings of length degree in this string and check their likelihood
        # record the most probable string in the word, which will start at the value of pivot.
        for i in range(0, len(string)-degree+1):
            substr = string[i:i+degree]
            if substr in self.__1grams:
                pr_substr = self.prob(substr)
                if (pivot == -1 and pr_substr > pr_string) or (pivot > -1 and pr_substr > pr_pivot):
                    pr_pivot = pr_substr
                    pivot = i

        # if no pivot was found, repeat with a lesser degree
        if pivot == -1: return self.__slice(string, degree-1)

        # if there's a pivot, split string into three and repeat on each string
        # concatenate each recursive answer with "-" to delimit segments
        else:
            left = string[:pivot]
            mid = string[pivot:pivot+degree]
            right = string[pivot+degree:]
            lseg = self.__slice(left, len(left)-1)
            mseg = self.__slice(mid, len(mid)-1)
            rseg = self.__slice(right, len(right)-1)
            return "-".join([lseg,mseg,rseg]).lstrip("-").rstrip("-")

    def __combine(self, segmentation):

        segments = segmentation.split("-")
        length = len(segments)
        if length < 2: return segmentation

        # keep merging segments of length 1
        while True:

            # keep track of best merge
            indxToMerge = -1
            bestMergeProb = 0.0

            for i in range(length-1):

                seg1 = segments[i]
                seg2 = segments[i+1]
                if len(seg1) > MINSIZE and len(seg2) > MINSIZE: continue
                merger = seg1 + seg2
                if merger not in self.__1grams: continue
                prob = self.prob(merger)
                if prob > bestMergeProb:
                    indxToMerge = i
                    bestMergeProb = prob

            if indxToMerge == -1:
                return segmentation
            else:
                merger = segments[indxToMerge] + segments[indxToMerge+1]
                segments = segments[:indxToMerge] + [merger] + segments[indxToMerge+2:]
                return "-".join(segments)

# --------------------------------------------------------------------------------
# Main.
# --------------------------------------------------------------------------------

def main():

    # check arguments have been supplied
    if len(sys.argv) == 1:
        print("Error: no arguments supplied.")
        print("Usage: segmenter.py arg1 arg2 ... ")
        print("Where arg1, arg2, ... are the strings you want to segment.")
        sys.exit(0)

    # check existence of 1grams
    if not os.path.isfile("1grams.txt"):
        print("Error: could not find 1grams.txt.")
        print("Exiting....")
        sys.exit(1)
    ngrams1 = "1grams.txt"

    # check existence of 2grams
    ngrams2 = "2grams.txt"
    if not os.path.isfile(ngrams2):
        print("Could not find 2grams file")
        print("Segmenter will run without use of 2grams")
        ngrams2 = None

    # make segmenter, display output
    seg = Segmenter(ngrams1, fpath_2grams=ngrams2)
    for word in sys.argv[1:]:
        print(word + "     ---->     ", end="")
        segmentation = seg.segment(word)
        print(segmentation)

if __name__ == "__main__": main()
