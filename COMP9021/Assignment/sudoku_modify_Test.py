from Assignment.sudoku_modify import *

# sudoku1 = Sudoku('sudoku_wrong_1.txt')
# sudoku2 = Sudoku('sudoku_wrong_2.txt')
# sudoku3 = Sudoku('sudoku_wrong_3.txt')
# sudoku = Sudoku('sudoku_1.txt')
# sudoku = Sudoku('sudoku_2.txt')
sudoku = Sudoku('sudoku_3.txt')
# sudoku = Sudoku('sudoku_4.txt')
# sudoku = Sudoku('sudoku_5.txt')
# sudoku.preassess()

# print(list(chain(*sudoku.originalStatus)))
# sudoku.preassess()
# print(sudoku.originalStatus)
# print(sorted(dict(Counter(chain(*sudoku.originalStatus))).items(),key = lambda x:x[1],reverse=True))
sudoku.forced_tex_output()
# sudoku.marked_tex_output()