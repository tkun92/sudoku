import numpy as np
from copy import deepcopy
from termcolor import colored

verbose = False
debug = True


def read_input(file_name):
    sudokus = list()
    with open(file_name, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line == "\n":
                continue
            sudokus.append(line.strip("\n"))

    actualsudoku = list()
    listsudoku = list()
    for item in sudokus:
        for i in range(0, len(item), 9):
            lines = item[i:i + 9]
            add = list()
            for index in lines:
                if index == ".":
                    add.append(None)
                else:
                    add.append(int(index))

            actualsudoku.append(add)

        listsudoku.append(actualsudoku)

        actualsudoku = []
    return listsudoku


def make_output(listsudoku):
    num_of_done = 0
    with open("output", "w") as output:
        for counter, item in enumerate(listsudoku):
            sudoku = Sudoku()
            sudoku.fill_example(item)
            sudoku.check_table()
            output.writelines("Counter:" + str(counter) + "\n")
            isitdone = sudoku.isitdone()
            output.writelines(str(isitdone) + "\n")

            if isitdone:
                num_of_done += 1

            for i in range(9):
                for j in range(9):
                    output.writelines(str(sudoku._table[i][j].final_number))
                output.writelines("\n")
            output.writelines("##################\n")
            for i in range(9):
                for j in range(9):
                    output.writelines(str(sudoku.table[i][j].possibilities))
                output.writelines("\n")
            output.writelines("\n")

    print("{} % of the sudokus are solved".format(num_of_done / len(listsudoku) * 100))


class Cell(object):
    def __init__(self):
        self.final_number = None
        self.possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.cube_id = None
        self.row_index = None
        self.col_index = None
        self.table = None

    def set_final(self, number):
        global verbose, debug
        self.final_number = number
        self.possibilities = [number]

        self.table.table_possibilities_elimination()
        if verbose:
            print("{} --> ({}, {})".format(number, self.row_index, self.col_index))
            print()
            self.table.print_final()
            if debug:
                inp = input()
                if len(inp):
                    debug = False

    def remove_possibility(self, number):
        assert len(self.possibilities) > 1
        self.table.changed = True
        self.possibilities.remove(number)

    def check_final(self):
        if len(self.possibilities) == 1 and self.final_number is None:
            self.set_final(self.possibilities[0])
            if verbose:
                print(colored("[Found number] ", "green") + "Find a final number {} in cell ({}, {})".format(
                    self.possibilities[0], self.row_index, self.col_index))
                print('------------------------------------------------------')


class Sudoku(object):
    def __init__(self):
        self._table = list()
        self.changed = False

        self.init_table()

    def init_table(self):
        cell = Cell()
        row = list()
        [row.append(deepcopy(cell)) for _ in range(9)]
        [self._table.append(deepcopy(row)) for _ in range(9)]

        for i, row in enumerate(self._table):
            for j, cell in enumerate(row):
                cube_id = (i // 3) * 3 + (j // 3)
                cell.cube_id = cube_id
                cell.row_index = i
                cell.col_index = j
                cell.table = self

    def fill_example(self, examplee_table):
        # print(example_table)
        for i, row in enumerate(self._table):
            for j, number in enumerate(row):
                # print("i:" + str(i) + " j:" + str(j))
                if examplee_table[i][j] == ".":
                    continue
                if examplee_table[i][j] is not None:
                    self._table[i][j].set_final(examplee_table[i][j])
        if verbose:
            print("End of filling example.")
            print(examplee_table)
            self.print_possibilities()
            print("#################################################################")

    def print_possibilities(self):
        for row in self._table:
            for cell in row:
                print(cell.possibilities, end=" ")
            print()

    def print_final(self):
        for row in self._table:
            for cell in row:
                print(cell.final_number if cell.final_number is not None else '.', end=" ")
            print()
        print()

    def print_cube_id(self):
        for row in self._table:
            for cell in row:
                print(cell.cube_id, end=" ")
            print()

    @property
    def table(self):
        return self._table

    def eliminate_possibilities(self, i, j, num):
        self.eliminate_possibilities_row(i, j, num)
        self.eliminate_possibilities_col(i, j, num)
        self.eliminate_possibilities_cube(i, j, num)

    def eliminate_possibilities_row(self, i, j, num):
        for index, cell in enumerate(self._table[i]):
            if index != j and num in cell.possibilities:
                cell.remove_possibility(num)

    def eliminate_possibilities_col(self, i, j, num):
        for index in range(len(self._table)):
            if index != i and num in self._table[index][j].possibilities:
                self._table[index][j].remove_possibility(num)

    def eliminate_possibilities_cube(self, i, j, num):
        cube_id = self._table[i][j].cube_id
        for row_index, row in enumerate(self._table):
            for col_index, cell in enumerate(row):
                if cell.cube_id == cube_id and not (row_index == i and col_index == j) and num in cell.possibilities:
                    cell.remove_possibility(num)

    def table_possibilities_elimination(self):
        for row_index, row in enumerate(self._table):
            for col_index, cell in enumerate(row):
                if len(cell.possibilities) == 1:
                    self.eliminate_possibilities(row_index, col_index, cell.possibilities[0])
                else:
                    self.intermediate_eliminate_possibilities(row_index, col_index)

    def intermediate_eliminate_possibilities(self, i, j):
        self.intermediate_elimination_row(i, j)
        self.intermediate_elimination_col(i, j)
        self.intermediate_elimination_cube(i, j)

    def intermediate_elimination_row(self, i, j):
        length = len(self._table[i][j].possibilities)

        same_indices = [j]
        for index, cell in enumerate(self._table[i]):
            if index != j and len(cell.possibilities) > 1 and cell.possibilities == self._table[i][j].possibilities:
                same_indices.append(index)

        if len(same_indices) == length:
            for number in self._table[i][j].possibilities:
                for index, cell in enumerate(self._table[i]):
                    if index not in same_indices and number in cell.possibilities and len(cell.possibilities) > 1:
                        cell.remove_possibility(number)

    def intermediate_elimination_col(self, i, j):
        length = len(self._table[i][j].possibilities)

        same_indices = [i]
        for index in range(len(self._table)):
            if index != i and len(self._table[index][j].possibilities) > 1 and self._table[index][j].possibilities == \
                    self._table[i][j].possibilities:
                same_indices.append(index)

        if len(same_indices) == length:
            for number in self._table[i][j].possibilities:
                for index in range(len(self._table)):
                    if index not in same_indices and number in self._table[index][j].possibilities and len(
                            self._table[index][j].possibilities) > 1:
                        self._table[index][j].remove_possibility(number)

    def intermediate_elimination_cube(self, i, j):
        cube_id = self._table[i][j].cube_id
        length = len(self._table[i][j].possibilities)

        same_indices = [(i, j)]
        for row_index, row in enumerate(self._table):
            for col_index, cell in enumerate(row):
                if cell.cube_id == cube_id and not (row_index == i and col_index == j) and len(
                        cell.possibilities) > 1 and cell.possibilities == self._table[i][j].possibilities:
                    same_indices.append((row_index, col_index))

        if len(same_indices) == length:
            for number in self._table[i][j].possibilities:
                for row_index, row in enumerate(self._table):
                    for col_index, cell in enumerate(row):
                        if cell.cube_id == cube_id and (
                                row_index, col_index) not in same_indices and number in cell.possibilities and \
                                len(cell.possibilities) > 1:
                            cell.remove_possibility(number)

    def check_table(self):
        while True:
            self.changed = False
            for row in self._table:
                for cell in row:
                    cell.check_final()
            if not self.changed:
                break
        if verbose:
            self.print_possibilities()

    def isitdone(self):
        done = True
        for row in self._table:
            for cell in row:
                if cell.final_number is None:
                    done = False
        return done


if __name__ == "__main__":
    # sudoku = Sudoku()
    # """
    # example_table = [[None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None],
    #                  [None, None, None, None, None, None, None, None, None]]
    # """
    # example_table = [[None, 2, None, None, None, 5, None, None, None],
    #                  [None, 1, 5, None, None, None, None, None, None],
    #                  [None, None, None, None, None, 8, 7, None, 3],
    #                  [None, 5, 1, None, None, None, None, None, None],
    #                  [None, None, 9, 7, None, None, None, 1, None],
    #                  [None, None, None, 3, None, None, None, 4, 6],
    #                  [None, None, None, None, 8, None, None, None, 1],
    #                  [7, None, None, 9, 3, None, None, 6, None],
    #                  [None, None, None, None, None, None, 4, None, 8]]

    listsudoku = read_input("input")
    make_output(listsudoku)

    print("Done!!!")

