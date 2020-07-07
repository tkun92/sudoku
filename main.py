import sudoku
import kivytest

app = kivytest.TestApp()
sudokuObj = sudoku.Sudoku()


item = sudoku.read_input("input")[0]

sudokuObj.fill_example(item)
print("#")
app.run()

