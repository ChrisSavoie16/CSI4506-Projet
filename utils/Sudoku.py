class Sudoku:

    def __init__(self):
        self.board = []
        for i in range(9):
            self.board.append([])
            for j in range(9):
                self.board[i].append(Square())

    def __str__(self):
        string = ""
        for i in range(9):
            for j in range(9):
                square = self.get_square(i, j)
                if square.get_is_clue():
                    string += str(square.get_domain()[0])
                else:
                    string += "0"
            string += "\n"
        return string

    def __eq__(self, other):
        if isinstance(other, Sudoku):
            for i in range(9):
                for j in range(9):
                    self_square = self.get_square(i, j)
                    other_square = other.get_square(i, j)
                    if not self_square == other_square:
                        return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_square(self, row, column):
        return self.board[row][column]


class Square:

    def __init__(self):
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.is_clue = False

    def __str__(self):
        return "Clue: " + str(self.is_clue()) + "\n" + "Domain" + str(self.get_domain()) + "\n"

    def __eq__(self, square):
        if isinstance(square, Square):
            return self.is_clue== square.is_clue and self.get_domain() == square.get_domain()
        return False

    def set_domain(self, domain):
        self.domain = domain

    def get_domain(self):
        return self.domain

    def set_clue(self, is_clue):
        self.is_clue = is_clue

    def get_is_clue(self):
        return self.is_clue
