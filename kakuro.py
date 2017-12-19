import numpy as np
import sys

"""
Kakuro game solver.
Demo example from p.119 in book. 

n = number of spots
S = sum to add up to
"""

def find_combos(S, n, available, picked=[], partial_sum=0):
    if partial_sum == S and len(picked) == n:
        yield picked
    if partial_sum > S or len(picked) > n:
        return

    for i, num in enumerate(available):
        remaining = available[i + 1:]
        yield from find_combos(S, n, remaining, picked + [num], partial_sum + num)

n = int(sys.argv[1])
S = int(sys.argv[2])
available = [i for i in range(1, 10)]
for comb in find_combos(S, n, available):
    print(list(comb), sum(comb))