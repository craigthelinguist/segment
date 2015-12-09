# --------------------------------------------------------------------------------
# Imports.
# --------------------------------------------------------------------------------

import os
import sys
import codecs


# --------------------------------------------------------------------------------
# Globals.
# --------------------------------------------------------------------------------

# These words should not be considered as ngrams. The loader will ignore them if
# show up in the ngram files.
IGNORE = ["the", "and"]

# The segmentation algorithm will attempt to recursively segment strings until they
# get below this specified minimum length.
MINSIZE = 3

# Needed to read certain kinds of characters common in corpora.
ENCODING = "latin-1"


# --------------------------------------------------------------------------------
# Segmenter class.
# --------------------------------------------------------------------------------

class Segmenter(object):
    """
    A Segmenter object attempts to separate a string by its constituent words.
    It does this using files of unigrams and bigrams. A unigram is a single word;
    a bigram is a pair of words. The probability of a unigram is based on its
    frequency among all the other words. The probability of a bigram is based on
    the frequency of those two words appearing in that order among all other
    pairs of words.
    """

    def __init__(self, fpath_1grams, fpath_2grams=None):

        # Initialise instance variables.
        self._1grams = None
        self._2grams = None

        # Load in the ngrams.
        loader = Loader()
        self.__1grams = loader.load_ngrams(fpath_1grams, 1, min_ngram_size=MINSIZE, ignore=IGNORE)
        if fpath_2grams:
            self.__2grams = loader.load_ngrams(fpath_2grams, 2, min_ngram_size=MINSIZE, ignore=IGNORE)

        # Check ngrams
        for c in self.__1grams:
            print (self.__1grams[c])
        for c in self.__2grams:
            for d in self.__2grams[c]:
                print(self.__2grams[c][d])

    def prob(self, *words):
        """
        Get the probability of the given unigram or bigram.

        Example usage:
        prob("hello") -> returns the probability of "hello" occuring.
        prob("hello", "world") -> returns the probability of "world" occuring after a "hello" occurs.

        Get the probability of the specified n-grams
        Raises ValueError if you pass in an illegal number of n-grams.
        :rtype : float
        """

        # Check unigram.
        if len(words) == 1:
            word = words[0]
            if word in self.__1grams:
                return self.__1grams[word]
            else: return 0.0

        # Check bigram.
        elif len(words) == 2:
            word1 = words[0]
            word2 = words[1]
            if word1 in self.__2grams and word2 in self.__2grams[word1]:
                return self.__2grams[word1][word2]
            else: return 0.0

        # Erroneous use of this method.
        else:
            raise ValueError("Invalid number of arguments passed.")

    def segment(self, string):
        """
        Attempt to segment the string into smaller components.
        Return the string with its components delimited by '-'
        :rtype : str
        """
        segmentation = self.__slice(string, len(string)-1)
        if self.__2grams:
            return self.__combine(segmentation)
        else:
            return segmentation

    def __slice(self, string, degree):
        """
        Segment a string by looking for the most probable substring. If there are no
        substrings then we attempt to slice on a smaller degree (stopping when degree
        gets below a predefined minimum). Otherwise we segment on the most probable
        substring and recursively slice the segments.
        :param string: the string to be segmented.
        :param degree: look for substrings of this length.
        :return: the string's segmentation, where the segments are delimited by "-".
        """

        # Base case: string is below a predefined minimum size.
        if degree < MINSIZE: return string

        # We look for the most probable substring in this word. The first character of the
        # most probable substring will be at string[pivot].
        pr_string = self.prob(string)
        pr_pivot = 2.0
        pivot = -1

        # Look for substrings of length degree and check their likelihood against the most
        # probable string so far.
        for i in range(0, len(string)-degree+1):
            substr = string[i:i+degree]
            if substr in self.__1grams:
                pr_substr = self.prob(substr)
                if (pivot == -1 and pr_substr > pr_string) or (pivot > -1 and pr_substr > pr_pivot):
                    pr_pivot = pr_substr
                    pivot = i

        # If we did not find ANY substrings, repeat the process with a smaller degree.
        if pivot == -1: return self.__slice(string, degree-1)

        # Otherwise there's a most probable substring. The string is split into three segments (the
        # middle chunk is the most probable substring) and then recurse on each segmen
        else:
            left = string[:pivot]
            mid = string[pivot:pivot+degree]
            right = string[pivot+degree:]
            lseg = self.__slice(left, len(left)-1)
            mseg = self.__slice(mid, len(mid)-1)
            rseg = self.__slice(right, len(right)-1)

            # Concatenate the outputs of each recursive call and return.
            return "-".join([lseg,mseg,rseg]).lstrip("-").rstrip("-")

    def __combine(self, segmentation):
        """
        Attempt to merge the parts of a segmented string. The algorithm for doing this is
        greedy: if two segments combined form a segment, they will be combined. If there's
        more than one way to combine two segments the most probable combination is chosen.
        :param string: the string to be segmented.
        :param degree: look for substrings of this length.
        :return: the string's segmentation, where the segments are delimited by "-".
        """

        # Split string by its segments.
        segments = segmentation.split("-")
        length = len(segments)
        if length < 2: return segmentation

        # Keep looking for segments to merge.
        while True:

            # Used to keep track of the best merge.
            indxToMerge = -1
            bestMergeProb = 0.0

            # Look at successive pairs of segments.
            for i in range(length-1):
                seg1 = segments[i]
                seg2 = segments[i+1]

                # If the segments individually are above a certain size, don't bother.
                if len(seg1) > MINSIZE and len(seg2) > MINSIZE:
                    continue

                # If the combined segments do not form a valid 1gram, don't bother.
                merger = seg1 + seg2
                if merger not in self.__1grams: continue

                # Update the best merge.
                prob = self.prob(merger)
                if prob > bestMergeProb:
                    indxToMerge = i
                    bestMergeProb = prob

            # Could not find anything to merge. We're done.
            if indxToMerge == -1:
                return segmentation

            # Otherwise we found something to merge. Merge it and repeat the loop.
            else:
                merger = segments[indxToMerge] + segments[indxToMerge+1]
                segments = segments[:indxToMerge] + [merger] + segments[indxToMerge+2:]
                return "-".join(segments)



# --------------------------------------------------------------------------------
# Loader.
# --------------------------------------------------------------------------------

class Loader(object):
    """
    This is for loading ngrams. You may wish to change this to support more file-types.
    Currently this only loads .tsv files where each line looks like this:

        WORD \t COUNT  (for 1-grams)
        WORD WORD \t COUNT  (for 2-grams)
    """

    def load_ngrams(self, fname, degree, min_ngram_size=None, ignore=[]):
        """
        Load ngrams from a file.
        :param fname: name of the file.
        :param degree: degree of ngrams (e.g. 1grams, 2grams)
        :param min_ngram_size: if specified, an ngram will be ignored if it
            contains a word with length less than min_ngram_size.
        :param ignore: if specified, an ngram will be ignored if it contains
            any of the words in the ignore list.
        :return: a normed dict of probabilities from ngrams to doubles. They
            look like this:

            unigrams[word] = prob of word appearing
            bigrams[first][second] = prob of second following first

        """

        words = dict()
        count = 0
        with codecs.open(fname, "r", ENCODING) as f:

            for line in f:

                # ngram
                line = line.split("\t")
                ngram = line[0]
                freq = int(line[1])

                # split ngram into its tokens
                # check validity
                ngrams = ngram.split(" ")
                if len(ngrams) != degree: continue
                if min_ngram_size:
                    for n in ngrams:
                        if len(n) < min_ngram_size: continue
                        if n in ignore: continue

                # add to words
                curr_dict = words
                for ngram in ngrams[:-1]:
                    if ngram not in curr_dict:
                        curr_dict[ngram] = dict()
                    curr_dict = curr_dict[ngram]

                # add to the curr_dict
                ngram = ngrams[-1]
                if ngram in curr_dict: curr_dict[ngram] = curr_dict[ngram] + freq
                else: curr_dict[ngram] = freq
                count += freq

            # normalise everything
            self.recursive_norm(words, count)

        return words

    def recursive_norm(self, words, count):
        for key in words:
            if isinstance(words[key], int):
                words[key] = 1.0 * words[key] / count
            else:
                self.recursive_norm(words[key], count)


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
        print(word + "     ---->     " + seg.segment(word))

if __name__ == "__main__": main()
