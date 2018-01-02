import numpy as np
import sys
from operator import itemgetter

"""
Kakuro game solver.
Demo example from p.119 in book. 

n = number of spots
S = sum to add up to
"""

NA = -1
VALUE = 0
H_SUM = 1
V_SUM = 2
D_SUM = 3

dummy = np.matrix([[-1,-1,-1,-1,-1],
                   [-1,-1, 0, 0,-1],
                   [-1, 0, 0, 0,-1],
                   [-1, 0,-1,-1,-1],
                   [-1,-1,-1,-1,-1]])

horizontal_dummy = np.matrix([[0,0,0,0,0],
                              [0,4,0,0,0],
                              [7,0,0,0,0],
                              [0,0,0,0,0],
                              [0,0,0,0,0]])

vertical_dummy = np.matrix([[0,0,3,4,0],
                            [0,5,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])

class Kakuro:

    def __init__(self, A, H, V):
        """
        :param A: Template matrix - Maps the variables x into the clues c.  
        :param H: 
        :param V: 
        """
        self.A = A
        self.V = V
        self.H = H

    def validate(self):
        pass

    def solve(self):
        """
        Backtracking algorithm
        :return: True if solved, False otherwise 
        """
        blank_row, blank_col = np.where(self.A == 0)
        current_cell = (blank_row[0], blank_col[0])
        blank_row = blank_row[1:]
        blank_col = blank_col[1:]
        current_value = 1
        iteration_count = 0
        while len(blank_col) > 0 and len(blank_row) > 0:
            self.A[current_cell[0], current_cell[1]] = current_value
            iteration_count += 1


    def find_linking_squares(self):
        # TODO fix
        linking_squares = []
        for i in range(len(self.A)):
            for j in range(len(self.A)):
                if 0 < i < len(self.A) - 1:
                    adjacent_row = [i - 1, i + 1]
                elif i == len(self.A) - 1:
                    adjacent_row = [i - 1]
                else:
                    adjacent_row = [i + 1]

                if 0 < j < len(self.A) - 1:
                    adjacent_col = [j - 1, j + 1]
                elif j == len(self.A) - 1:
                    adjacent_col = [j - 1]
                else:
                    adjacent_col = [j + 1]

                adjacent = [self.A[i, k] for k in adjacent_col]
                adjacent += [self.A[k, j] for k in adjacent_row]
                if np.count_nonzero(adjacent) == len(adjacent) - 2:
                    linking_squares.append((i, j))

        print(linking_squares)
        return linking_squares

    def add_variable(self, template):
        pass


    def print_board(self):
        board = ""
        for row in self.board:
            for slot in row:
                board += "|{}".format(slot.to_string())
            board += "|\n"
        print(board)

class Slot:

    def __init__(self, type=NA):
        self.type = type
        if type == D_SUM:
            self.value = (0,0)
        else:
            self.value = 0

    def to_string(self):
        if self.type == NA:
            return " \ "
        elif self.type == VALUE:
            return " {} ".format(self.value)
        elif self.type == H_SUM:
            return " \{}".format(self.value)
        elif self.type == V_SUM:
            return "{}\ ".format(self.value)
        else:
            return "{}\{}".format(self.value[0], self.value[1])

    def get_type(self):
        return self.type

    def get_value(self):
        if self.type == VALUE:
            return self.type
        else:
            return False

    def set_value(self, value):
        if self.type == VALUE:
            self.value = value
            return True
        else:
            return False

def find_combos(S, n, available, picked=[], partial_sum=0):
    if partial_sum == S and len(picked) == n:
        yield picked

    if partial_sum > S or len(picked) > n:
        return

    for i, num in enumerate(available):
        remaining = available[i + 1:]
        yield from find_combos(S, n, remaining, picked + [num], partial_sum + num)

kakuro = Kakuro(dummy, horizontal_dummy, vertical_dummy)
squares = kakuro.solve()