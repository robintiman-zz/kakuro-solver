from kakuro import find_combos
import pickle

"""
Pre-calculate unique partitions
n - number of slots
S - the sum to equal to 
"""
parts = list(range(2, 10))
S = list(range(3, 46))
count = 0
unique = {}
partition = []
available = list(range(1,10))
for n in parts:
    for s in S:
        for combo in find_combos(s, n, available):
            count+=1
            partition = combo
        if count == 1:
           unique[(n, s)] = partition
        count = 0

pickle.dump(unique, open("unique_partitions.data", "wb"))