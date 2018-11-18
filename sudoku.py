class Sudoku:

    board = []

    def __init__(self):
        for i in range(9):
            self.board[i] = []
            for j in range(9):
                self.board[i][j] = Square()

    def get_square(self, i, j):
        return self.board[i][j]


class Square:

    domain = []
    isClue = False

    def __init__(self):
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def set_domain(self, domain):
        self.domain = domain

    def get_domain(self):
        return self.domain

    def set_clue(self, isClue):
        self.isClue = isClue

    def is_clue(self):
        return self.isClue
