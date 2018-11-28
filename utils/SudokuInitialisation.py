from utils.Sudoku import Sudoku


def init_sudoku(problem):
    new = Sudoku()
    for i in range(81):
        if problem[i] != "0":
            square = new.get_square(i // 9, i % 9)
            square.set_clue(True)
            square.set_domain([int(problem[i])])
    return new
