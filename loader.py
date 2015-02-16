
# --------------------------------------------------------------------------------
# Imports.
# --------------------------------------------------------------------------------

import codecs


# --------------------------------------------------------------------------------
# Constants.
# --------------------------------------------------------------------------------

__GRAMMAR = ["the", "and"]
__VALID_CHARS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n",
                "o","p","q","r","s","t","u","v","w","x","y","z","-"]
__ENCODING = "latin-1"



# --------------------------------------------------------------------------------
# Functions.
# --------------------------------------------------------------------------------

def load_ngrams(fname, degree, min_ngram_size=None, ignore=[]):
    words = dict()
    count = 0
    with codecs.open(fname, "r", __ENCODING) as f:

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
        recursive_norm(words, count)

    return words


def recursive_norm(words, count):
    for key in words:
        if isinstance(words[key], int):
            words[key] = words[key] / count
        else:
            recursive_norm(words[key], count)