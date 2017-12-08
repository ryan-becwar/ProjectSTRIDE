#!/usr/local/anaconda/bin/python
import sys
from ast import literal_eval as make_tuple


curr_word = None
curr_count = 0

best = None
best_key = -1
best_score = -sys.maxsize
# Process each key-value pair from the mapper
for line in sys.stdin:

    key, data = line.split('\t')

    tup = make_tuple(data)
    route, score = tup

    if score > best_score:
        best_key = key
        best = data
        best_score = score

print('{0}\t{1}'.format(best_key, best))
