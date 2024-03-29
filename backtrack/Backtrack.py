def backtrack_solve(sudoku):
    """
    The main implementation that solves the sudoku using a backtrack algorithm
    :param sudoku: sudoku to solve
    :return: return the sudoku if already solved. modifies original sudoku if already solved
    """
    solved = False
    # Build solution space
    solution = []
    for i in range(9):
        solution.append([])
        for j in range(9):
            square = sudoku.get_square(i, j)
            if square.is_clue:
                solution[i].append(square.domain[0])
            else:
                solution[i].append(0)

    row, column, domain_position = find_start_point(sudoku)
    # If row is out of range, sudoku is already solved
    if row > 8:
        return sudoku

    while not solved:
        square = sudoku.get_square(row, column)
        if not square.is_clue:
            solution[row][column] = square.domain[domain_position]
        if square.is_clue or is_valid_assignment(sudoku, solution, row, column):
            domain_position = 0

            if column == 8 and row == 8:
                solved = True
            elif column == 8:
                row += 1
                column = 0
            else:
                column += 1
        else:
            row, column, domain_position = backtrack(sudoku, solution, row, column, domain_position)

    for i in range(9):
        for j in range(9):
            square = sudoku.get_square(i, j)
            square.is_clue = True
            square.domain = [solution[i][j]]


def is_valid_assignment(sudoku, solution, row, column):
    """
    Checks if the assigned number in the solution space is valid
    :param solution: the solution space
    :param row: row assigned
    :param column: column assigned
    :return: boolean
    """
    for arc in sudoku.get_square(row, column).constraints:
        constraint = arc.target
        if solution[constraint.row][constraint.column] != 0 \
                and solution[constraint.row][constraint.column] == solution[row][column]:
            return False
    return True


def find_start_point(sudoku):
    """
    Program finds the start point. Essential the first square that is not a clue.
    If none is found, returns 9,9,9, meaning the sudoku is already solved.
    :param sudoku: the Sudoku instance that we are trying to solve
    :return: row, column, domain_index to start at
    """
    for i in range(9):
        for j in range(9):
            square = sudoku.get_square(i, j)
            if not square.is_clue:
                return i, j, 0
    return 9, 9, 9


def backtrack(sudoku, solution, row, column, domain_position):
    """
    finds the next starting point of the backtrack algorithm
    :param sudoku: the sudoku trying to be solved
    :param solution: the solution space
    :param row: current row
    :param column: current column
    :param domain_position: current domain position
    :return: row, column, domain_position starting point
    """
    i = row
    j = column
    k = domain_position
    solution[row][column] = 0
    if k < len(sudoku.get_square(row, column).domain) - 1:
        k += 1
    else:
        found_next = False
        while not found_next:
            if j == 0:
                j = 8
                i -= 1
            else:
                j -= 1
            square = sudoku.get_square(i, j)
            if not square.is_clue:
                domain = square.domain
                domain_index = domain.index(solution[i][j])
                if domain_index < len(domain) - 1:
                    k = domain_index + 1
                    found_next = True
                else:
                    solution[i][j] = 0
    return i, j, k
