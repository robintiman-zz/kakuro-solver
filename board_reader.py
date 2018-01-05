import sys
import pickle
import argparse

"""
A helper program to build Kakuro games for the solver. 
"""
parser = argparse.ArgumentParser()
parser.add_argument("-b", help="Board matrix", action="store_true")
parser.add_argument("-c", help="Clue dict", action="store_true")
parser.add_argument("-x", help="Append this option to make changes", action="store_true")
args = parser.parse_args()

if args.b and not args.x:
    clues = {}
    file = input("Game name:\n")
    print("Insert cell values according to:\n"
          "<x> <y> <x clue> <y clue>")
    for cell in sys.stdin:
        try:
            x, y, x_clue, y_clue = tuple(int(v) for v in cell.split())
            clues[(x,y)] = (x_clue, y_clue)
        except ValueError:
            print("Wrong format!")

    pickle.dump(clues, open("{}.kak".format(file), "wb"))

if args.c and not args.c:
    file = input("Game name:\n")
    print("Insert matrix\n"
          "0 for empty cell, -1 for clue cell")
    board = []
    for cell in sys.stdin:
        try:
            row = [int(x) for x in cell.split()]
            board.append(row)
        except ValueError:
            print("Wrong format!")
    pickle.dump(board, open("{}.game".format(file), "wb"))
    print("Game saved!")

if args.x:
    if args.b:
        file = open(input("Enter the game name:\n"), "wb)")
        data = pickle.load(file)
        change = input("Enter coordinates and the new value:\n")
        x, y, value = tuple(int(v) for v in change.split())
        