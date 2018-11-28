def backtrack_solve(sudoku):
    solved = False
    solution = []
    for i in range(9):
        solution.append([])
        for j in range(9):
            square = sudoku.get_square(i, j)
            if square.get_is_clue():
                solution[i].append(square.get_domain()[0])
            else:
                solution[i].append(0)

    row, column, domain_position = find_start_point(sudoku)
    if row > 8:
        return sudoku

    while not solved:
        square = sudoku.get_square(row, column)
        if not square.get_is_clue():
            solution[row][column] = square.get_domain()[domain_position]
        if square.get_is_clue() or is_valid_assignment(solution, row, column):
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
            square.set_clue(True)
            square.set_domain([solution[i][j]])


def is_valid_assignment(solution, row, column):
    for i in range(9):
        if i != column and solution[row][i] != 0 and solution[row][i] == solution[row][column]:
            return False

    for j in range(9):
        if j != row and solution[j][column] != 0 and solution[j][column] == solution[row][column]:
            return False

    box_row = row // 3
    box_column = column // 3
    for i in range(3):
        for j in range(3):
            compare_row = 3 * box_row + i
            compare_column = 3 * box_column + j
            if (compare_row != row
               and compare_column != column
               and solution[compare_row][compare_column] != 0
               and solution[compare_row][compare_column] == solution[row][column]):
                return False
    return True


def find_start_point(sudoku):
    for i in range(9):
        for j in range(9):
            square = sudoku.get_square(i, j)
            if not square.get_is_clue():
                return i, j, 0
    return 9, 9, 9


def backtrack(sudoku, solution, row, column, domain_position):
    i = row
    j = column
    k = domain_position
    solution[row][column] = 0
    if k < len(sudoku.get_square(row, column).get_domain()) - 1:
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
            if not square.get_is_clue():
                domain = square.get_domain()
                domain_index = domain.index(solution[i][j])
                if domain_index < len(domain) - 1:
                    k = domain_index + 1
                    found_next = True
                else:
                    solution[i][j] = 0
    return i, j, k