import numpy as np
import sys

"""
n = number of spots
S = sum to add up to
"""

def find_combos(S, n, available, picked):
    curr_sum = sum(picked)
    if curr_sum == S and len(picked) == n:
        yield picked
    if curr_sum > S or len(picked) > n:
        return

    for i, num in enumerate(available):
        available = available[i + 1:]
        picked = picked + [num]
        yield from find_combos(S, n, available, picked)

n = int(sys.argv[1])
S = int(sys.argv[2])
available = [i for i in range(1, 10)]
for comb in find_combos(S, n, available, []):
    print(comb)