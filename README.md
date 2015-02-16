segmenter.py
============

Use Segmenter like this:
```python
from segmenter import Segmenter
seg = Segmenter("1grams.txt", fpath_2grams="2grams.txt", fpath_3grams="3grams.txt")
segmentation = seg.segment("allblacks")
print(segmentation)
> "all-blacks"
```

Segmenter takes three arguments specifying the file location of 1grams, 2grams, and 3grams. 2grams and 3grams are optional: it will perform better if you have them though, by doing the combine stage (described below). If you don't want that, then use it like this:
```python
from segmenter import Segmenter
seg = Segmenter("1grams.txt")
segmentation = seg.segment("allblacks")
print(segmentation)
> "all-black-s"
```

Note that it can take quite a while to load the ngrams into memory.

test-shell.py
=============

An interactive REPL for testing the segmenter. Run like so:
```bash
python3 shell.py
```

How it works
============

The segment(string) method works in two stages: slice and combine. Slice looks for 

<h5>slice(string)</h5>
Look at substrings in <code>string</code> and segment according to the most likely. Repeat the process on each segment, looking at smaller and smaller substrings, until you below a predefined minimum substring length (currently this is 3).

<h5>combine(segmentation)</h5>
Look at the segment in <code>segmentation</code>. If a segment is below the minimum substring length, look at its neighbouring segments. If they can be combined to form a string in the ngrams we loaded, then we combine it. Repeat until we can no longer combine anything.
