# midi-experiments
 
Krumhansl-Schmuckler key-finding algorithm.
Useful links [Key-finding algorithm by Rober Hart](http://rnhart.net/articles/key-finding/), [What'sKey for Key by David Temperley, pdf](http://davidtemperley.com/wp-content/uploads/2015/11/temperley-mp99.pdf)
```python

import key_finding as kf
import numpy as np

notes = [[12, 0.2], [43, 0.21]] # list of list of pitch and duration

keys = kf.find_key(notes)
# it will return tuples of probabilities — major and minor key
# [0.2, 0.6 ...][0.3, 0.3]
# then you can compare it

# for human representstion use `find_key_str()`
kf.find_key_str(notes)

# return somth like "A major" or "D minor"

```