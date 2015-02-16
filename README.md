segmenter.py
============

The Segmenter class takes two arguments specifying the file location of 1grams and 2grams. The use of 2grams is optional but it will perform better if you have them.

Here's an example
```python
from segmenter import Segmenter
seg = Segmenter("1grams.txt", fpath_2grams="2grams.txt")
segmentation = seg.segment("allblacks")
print(segmentation)
> "all-blacks"
```

test-shell.py
=============

An interactive REPL for testing Segmenter. Run like so:
```bash
python3 shell.py
```

If you want to test Segmenter using 1grams only, run it like this:
```bash
python3 shell.py -simple
```

How it works
============

The segment(string) method works in two stages: slice and combine.

<h5>slice(string)</h5>
Look at substrings in <code>string</code> and segment according to the most likely. Repeat the process on each segment, looking at smaller and smaller substrings, until you recurse below a predefined minimum substring length (currently this is 3).

<h5>combine(segmentation)</h5>
Look at the segment in <code>segmentation</code>. If a segment is below the minimum substring length, look at its neighbouring segments. If they can be combined to form a string in the ngrams we loaded, then we combine it. Repeat until we can no longer combine anything.
