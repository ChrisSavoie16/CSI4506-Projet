from utils.Sudoku import Sudoku


def init_sudoku(problem):
    new = Sudoku()
    for i in range(81):
        if problem[i] != "0":
            square = new.get_square(i // 9, i % 9)
            square.is_clue = True
            square.domain = [int(problem[i])]
    return new
