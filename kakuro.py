import numpy as np
from sympy import Matrix, Symbol, zeros, pprint, ones
from sympy.solvers.solveset import linsolve
from sympy.parsing.sympy_parser import parse_expr

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

dummy = [[-1,-1,-1,-1,-1],
         [-1,-1, 0, 0,-1],
         [-1, 0, 0, 0,-1],
         [-1, 0,-1,-1,-1],
         [-1,-1,-1,-1,-1]]

# Key = the position in the grid
# Value = the clues connected to the cell. (row clue, column clue)
clues = {(1,2): (4,3), (1,3): (4,4), (2,1): (7,5), (2,2): (7,3), (2,3): (7,4), (3,1): (None,5)}

horizontal_dummy = [[0,0,0,0,0],
                    [0,4,0,0,0],
                    [7,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]

vertical_dummy = [[0,0,3,4,0],
                  [0,5,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0]]

def get_nonzero(values):
    symbols = []
    for value in values:
        if value != 0:
            symbols.append(value)
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

    def validate(self):
        pass

    def solve(self):
        """
        Backtracking algorithm
        :return: True if solved, False otherwise 
        """
        blank_row, blank_col = np.where(self.grid == 0)
        current_cell = (blank_row[0], blank_col[0])
        blank_row = blank_row[1:]
        blank_col = blank_col[1:]
        current_value = 1
        iteration_count = 0
        while len(blank_col) > 0 and len(blank_row) > 0:
            self.grid[current_cell[0], current_cell[1]] = current_value
            iteration_count += 1


    def solve_algebraic(self):
        """
        Algorithm:
        1. Put a symbol into an empty cell
        2. Solve the puzzle with the available clues and symbols as far as possible
        3. Repeat until all cells are filled. 
        :return: True if successful, False otherwise.
        """
        num_cells = len(self.grid) * len(self.grid[0])
        symbols = [Symbol(chr(code)) for code in range(97 + num_cells, 96, -1)]
        spreadsheet = zeros(len(self.grid), len(self.grid[0]))
        # Fill the symbol matrix
        num_symbols = 0
        sym_count = 97 # This is the char code for 'a'
        for cell in self.get_cell():
            spreadsheet[cell[0], cell[1]] = Symbol(chr(sym_count))
            num_symbols += 1
            sym_count += 1

        # Fill the row and column sums to match the symbol matrix
        row_sums = zeros(len(self.grid), 1)
        col_sums = zeros(len(self.grid), 1)
        for cell in self.get_cell():
            row = cell[0]
            col = cell[1]
            row_clue, col_clue = self.clues[row, col]
            row_sums[row] = row_clue
            col_sums[col] = col_clue

        # Build the equations
        equations = []
        symbols = []
        for i in range(len(self.grid)):
            row_syms = get_nonzero(spreadsheet.row(i))
            col_syms = get_nonzero(spreadsheet.col(i))
            eqn_row = '+'.join(map(lambda sym: str(sym), row_syms))
            eqn_col = '+'.join(map(lambda sym: str(sym), col_syms))
            if row_sums[i] != None and eqn_row != '':
                eqn_row += '-{}'.format(row_sums[i])
                equations.append(parse_expr(eqn_row))
            if col_sums[i] != None and eqn_col != '':
                eqn_col += '-{}'.format(col_sums[i])
                equations.append(parse_expr(eqn_col))
            symbols += row_syms

        # Solve the equations
        result = linsolve(equations, *symbols)
        pprint(spreadsheet)
        print(result)
        return True

    def get_cell(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 0:
                    yield (i,j)

    def find_linking_squares(self):
        # TODO fix
        linking_squares = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if 0 < i < len(self.grid) - 1:
                    adjacent_row = [i - 1, i + 1]
                elif i == len(self.grid) - 1:
                    adjacent_row = [i - 1]
                else:
                    adjacent_row = [i + 1]

                if 0 < j < len(self.grid) - 1:
                    adjacent_col = [j - 1, j + 1]
                elif j == len(self.grid) - 1:
                    adjacent_col = [j - 1]
                else:
                    adjacent_col = [j + 1]

                adjacent = [self.grid[i, k] for k in adjacent_col]
                adjacent += [self.grid[k, j] for k in adjacent_row]
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

kakuro = Kakuro(dummy, clues)
squares = kakuro.solve_algebraic()