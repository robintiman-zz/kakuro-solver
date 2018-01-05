import sys
import pickle

"""
A helper program to build Kakuro games for the solver. 
"""
clues = {}
file = input("Game name:\n")
print("Insert cell values according to:\n"
      "<x> <y> <x clue> <y clue>")
for cell in sys.stdin:
    try:
        x, y, x_clue, y_clue = tuple(int(x) for x in cell.split())
        clues[(x,y)] = (x_clue, y_clue)
    except ValueError:
        print("Wrong format!")

pickle.dump(clues, open("{}.kak".format(file), "wb"))