from copy import deepcopy
from termcolor import colored
from tqdm import tqdm

verbose = False
debug = True
intermediate = False
write_output = True


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


def solve_sudokus(listsudoku):
    num_of_done = 0

    if write_output:
        with open("output", "w") as output:
            for counter, item in enumerate(tqdm(listsudoku)):
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
    else:
        for counter, item in enumerate(tqdm(listsudoku)):
            sudoku = Sudoku()
            sudoku.fill_example(item)
            sudoku.check_table()
            if sudoku.isitdone():
                num_of_done += 1

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

    def fill_example(self, example_table):
        for i, row in enumerate(self._table):
            for j, number in enumerate(row):
                if example_table[i][j] == ".":
                    continue
                if example_table[i][j] is not None:
                    self._table[i][j].set_final(example_table[i][j])
        if verbose:
            print("End of filling example.")
            print(example_table)
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

    """Basic elimination"""

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

    """Intermediate elimination"""

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

    """Check for single number"""

    def check_single(self, num):
        for row_index in range(9):
            self.check_row(row_index, num)

        for col_index in range(9):
            self.check_col(col_index, num)

        for cube_id in range(9):
            self.check_cube(cube_id, num)

    def check_row(self, row_index, num):
        num_counter = 0
        col_index = None
        for index, cell in enumerate(self._table[row_index]):
            if num in cell.possibilities:
                num_counter += 1
                col_index = index

        assert num_counter > 0

        # In this case we find a new number only in one cell in this row.
        if num_counter == 1 and len(self._table[row_index][col_index].possibilities) > 1:
            self._table[row_index][col_index].possibilities = [num]
            self.changed = True

    def check_col(self, col_index, num):
        num_counter = 0
        row_index = None

        for index in range(len(self._table)):
            if num in self._table[index][col_index].possibilities:
                num_counter += 1
                row_index = index

        assert num_counter > 0

        # In this case we find a new number only in one cell in this column.
        if num_counter == 1 and len(self._table[row_index][col_index].possibilities) > 1:
            self._table[row_index][col_index].possibilities = [num]
            self.changed = True

    def check_cube(self, cube_id, num):
        num_counter = 0
        row_index = None
        col_index = None

        for i, row in enumerate(self._table):
            for j, cell in enumerate(row):
                if cell.cube_id == cube_id and num in cell.possibilities:
                    num_counter += 1
                    row_index = i
                    col_index = j

        assert num_counter > 0

        # In this case we find a new number only in one cell in this cube.
        if num_counter == 1 and len(self._table[row_index][col_index].possibilities) > 1:
            self._table[row_index][col_index].possibilities = [num]
            self.changed = True

    """Final result check"""

    def final_check(self):
        for row_index in range(9):
            done = self.final_check_row(row_index)
            if not done:
                return False

        for col_index in range(9):
            done = self.final_check_col(col_index)
            if not done:
                return False

        for cube_id in range(9):
            done = self.final_check_cube(cube_id)
            if not done:
                return False

        return True

    def final_check_row(self, row_index):
        check_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for cell in self._table[row_index]:
            assert len(cell.possibilities) == 1
            assert cell.final_number is not None

            try:
                check_list.remove(cell.final_number)
            except ValueError:
                # Try to remove one number two times!
                return False

        assert len(check_list) == 0
        return True

    def final_check_col(self, col_index):
        check_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for index in range(len(self._table)):
            assert len(self._table[index][col_index].possibilities) == 1
            assert self._table[index][col_index].final_number is not None

            try:
                check_list.remove(self._table[index][col_index].final_number)
            except ValueError:
                # Try to remove one number two times!
                return False

        assert len(check_list) == 0
        return True

    def final_check_cube(self, cube_id):
        check_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for row in self._table:
            for cell in row:
                if cell.cube_id == cube_id:
                    assert len(cell.possibilities) == 1
                    assert cell.final_number is not None

                    try:
                        check_list.remove(cell.final_number)
                    except ValueError:
                        # Try to remove one number two times!
                        return False

        assert len(check_list) == 0
        return True

    def table_possibilities_elimination(self):
        for row_index, row in enumerate(self._table):
            for col_index, cell in enumerate(row):
                if len(cell.possibilities) == 1:
                    self.eliminate_possibilities(row_index, col_index, cell.possibilities[0])
                elif intermediate:
                    self.intermediate_eliminate_possibilities(row_index, col_index)

        for num in range(1, 10):
            self.check_single(num)

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
        for row in self._table:
            for cell in row:
                if cell.final_number is None:
                    return False

        done = self.final_check()
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
    solve_sudokus(listsudoku)

    print("Done!!!")
