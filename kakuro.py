import numpy as np
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import pickle

"""
Kakuro game solver.
Demo example from p.119 in book. 

n = number of spots
S = sum to add up to
"""

dummy = [[-1,-1,-1,-1,-1],
         [-1,-1, 0, 0,-1],
         [-1, 0, 0, 0,-1],
         [-1, 0,-1,-1,-1],
         [-1,-1,-1,-1,-1]]

# Key = the position in the grid
# Value = the clues connected to the cell. (row clue, column clue)
clues = {(1,2): (4,3), (1,3): (4,4), (2,1): (7,5), (2,2): (7,3), (2,3): (7,4), (3,1): (None,5)}
# clues = {(1,1)}


def get_nonzero(values):
    symbols = []
    new_row = False
    count = -1
    for value in values:
        if value != 0 and not new_row:
            symbols[count].append(value)
        if value != 0 and new_row:
            symbols.append([value])
            new_row = False
            count += 1
        if value == 0:
            new_row = True
    return symbols

class Kakuro:

    def __init__(self, grid, clues):
        """
        :param grid: Template matrix - Maps the variables x into the clues c.  
        :param H: 
        :param V: 
        """
        self.grid = grid
        self.clues = clues


    def solve_algebraic(self):
        """
        Algorithm:
        1. Put a symbol into an empty cell
        2. Solve the puzzle with the available clues and symbols as far as possible
        3. Repeat until all cells are filled. 
        :return: True if successful, False otherwise.
        """
        spreadsheet = zeros(len(self.grid), len(self.grid[0]))

        # Fill the symbol matrix
        # TODO import all available symbols instead
        sym_count = 97 # This is the char code for 'a'
        row_sums = zeros(len(self.grid), 1)
        col_sums = zeros(len(self.grid), 1)
        sym_multiplier = 1
        for cell in self.get_cell():
            row = cell[0]
            col = cell[1]
            row_clue, col_clue = self.clues[row, col]
            row_sums[row] = row_clue
            col_sums[col] = col_clue
            spreadsheet[row, col] = Symbol(chr(sym_count) * sym_multiplier)
            sym_count += 1
            if sym_count > 122:
                sym_multiplier += 1
                sym_count = 97

        pprint(spreadsheet)
        # Build the equations
        for i in range(len(self.grid)):
            symbols, equations, dependencies = self.build_equations(col_sums, dependencies, equations, i, row_sums, spreadsheet, symbols)

        # Solve the equations
        pprint(spreadsheet)
        system_sol = linsolve(equations, *symbols)[0]
        solution = {e[1] : e[0] for e in zip(list(system_sol), symbols)}

        # Enforce the rules. There are two rules in Kakuro which are translated to inequalities.
        # 1. Only use digits 1 to 9: 0 < a < 10
        # 2. No digits can be repeated for a single clue: a != b
        # 3. It has to be an integer
        inequalities = []
        for dep in dependencies:
            prev = dep.pop()
            inequalities += [solution[prev] >= 1, solution[prev] <= 9]
            for next in dep:
                inequalities.append(Ne(solution[prev], solution[next]))
                inequalities += [solution[next] >= 1, solution[next] <= 9]
                prev = next

        raise NotImplemented
        # TODO Enter the data for the game at p.119.
        ineq_sol = solve(inequalities, symbols[4]) # TODO this doesn't work in the general case
        true_value = None
        for test_value in range(1,10):
            if ineq_sol.subs(symbols[4], test_value):
                true_value = test_value

        if not true_value:
            print("Solution not found!")
            return False

        # Solve the rest using the true value(s) for the dependent variable(s)
        for sym in solution:
                solution[sym] = solution[sym].subs(symbols[4], true_value)

        self.insert_solution(solution, spreadsheet)
        pprint(spreadsheet)
        return True

    def build_equations(self, i, sums, spreadsheet, direction):
        dependencies = []
        equations = []
        symbols = []
        if direction == "row":
            values = get_nonzero(spreadsheet.row(i))
        else:
            values = get_nonzero(spreadsheet.col(i))

        eqn_row = '+'.join(map(lambda sym: str(sym), values))
        if sums[i] != None and eqn_row != '':
            eqn_row += '-{}'.format(sums[i])
            dependencies.append(values)
            equations.append(parse_expr(eqn_row))

        if direction == "row":
            symbols += values
        return dependencies, equations, symbols

    def insert_solution(self, solution, spreadsheet):
        for i in range(spreadsheet.shape[0]):
            for j in range(spreadsheet.shape[1]):
                value = spreadsheet[i, j]
                if value != 0:
                    spreadsheet[i, j] = solution[value]

    def get_cell(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 0:
                    yield (i,j)


p119_clues = pickle.load(open("p119.kak", "rb"))
p119_board = pickle.load(open("p119.game", "rb"))
kakuro = Kakuro(p119_board, p119_clues)
squares = kakuro.solve_algebraic()