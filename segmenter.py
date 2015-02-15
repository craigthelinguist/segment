

# --------------------------------------------------------------------------------
# Imports.
# --------------------------------------------------------------------------------

import os
import sys
import loader as _loader


# --------------------------------------------------------------------------------
# Globals.
# --------------------------------------------------------------------------------



# --------------------------------------------------------------------------------
# Clases.
# --------------------------------------------------------------------------------

class Segmenter(object):

    __frequencies = None
    __3grams = None
    __MIN_DEGREE = _loader.MIN_DEGREE

    def __init__(self, fpath_frequencies, fpath_3grams=None):
        self.__frequencies = _loader.load_frequencies(fpath_frequencies)
        if fpath_3grams:
            self.__3grams = _loader.load_3grams(fpath_3grams)
        else:
            self.__3grams = dict(dict(dict()))

    def prob(self, words):
        """
        Get the probability of the specified n-grams.
        Raises ValueError if you pass in an illegal number of n-grams.
        :rtype : float
        """
        if isinstance(words, str):
            words = [words]
        if len(words) == 1:
            word = words[0]
            p = self._pr(word)
            return p
        elif len(words) == 3:
            word1 = words[0]
            word2 = words[1]
            word3 = words[2]
            _3grams = self.__3grams
            if word1 in _3grams:
                if word2 in _3grams[word1]:
                    if word3 in _3grams[word1][word2]:
                        return _3grams[word1][word2][word3]
            return 0.0
        else:
            raise ValueError("Can only get probability of 1-grams or 3-grams.")

    def _pr(self, s):
        if s not in self.__frequencies:
            return 0.0
        else:
            return self.__frequencies[s]

    def _pr3gram(self, s1, s2, s3):
        """
        Get the probability that three strings appear one after another.
        :rtype : float
        """
        if not s1 in self.__3grams:
            return 0.0
        elif not s2 in self.__3grams[s1]:
            return 0.0
        elif not s3 in self.__3grams[s1][s2]:
            return 0.0
        else:
            return self.__3grams[s1][s2][s3]

    def segment(self, string):
        """
        Attempt to segment the given string into its English word components.
        Return the string with its components delimited by '-'
        :rtype : str
        """
        return self._slice(string, self.__frequencies, len(string)-1)

    def _slice(self, string, words, degree):

        # base case.
        if degree < self.__MIN_DEGREE:
         return string

        # keep track of the most probable substring in this word. the first character
        # of this string will be at string[pivot].
        pr_string = self.prob(string)
        pr_pivot = 2.0
        pivot = -1

        # find all strings of length degree in this string and check their likelihood
        # record the most probable string in the word, which will start at pivot.
        for i in range(0, len(string)-degree+1):
            substr = string[i:i+degree]
            if substr in words:
                pr_substr = self.prob(substr)
                if (pivot == -1 and pr_substr > pr_string) or (pivot > -1 and pr_substr > pr_pivot):
                    pr_pivot = pr_substr
                    pivot = i

        # if no pivot, then repeat with a lesser degree.
        if pivot == -1:
            return self._slice(string, words, degree-1)

        # if there's a pivot, split string into three and repeat on each string
        # join the strings with "-" to show segmentation.
        else:
            left = string[:pivot]
            mid = string[pivot:pivot+degree]
            right = string[pivot+degree:]
            lseg = self._slice(left, words, len(left)-1)
            mseg = self._slice(mid, words, len(mid)-1)
            rseg = self._slice(right, words, len(right)-1)

            return "-".join([lseg,mseg,rseg]).lstrip("-").rstrip("-")

# --------------------------------------------------------------------------------
# Main.
# --------------------------------------------------------------------------------
def main():

    if len(sys.argv) == 1:
        print("Error: no arguments supplied.")
        print("Usage: segmenter.py arg1 arg2 ... ")
        print("Where arg1, arg2, ... are the strings you want to segment.")
        sys.exit(0)

    if not os.path.isfile("1grams.txt"):
        print("Error: could not find 1grams.txt.")
        print("Exiting....")
        sys.exit(1)
    ngrams1 = "1grams.txt"

    ngrams3 = "3grams.txt"
    if not os.path.isfile(ngrams3):
        print("Could not find 3grams.txt.")
        print("Segmenter will run without use of 3grams.")
        ngrams3 = None

    seg = Segmenter(ngrams1, ngrams3)

    for word in sys.argv[1:]:
        print(word + "     ---->     ", end="")
        segmentation = seg.segment(word)
        print(segmentation)

if __name__ == "__main__": main()
