
import queue


def AC3(sudoku):
    """

    :param sudoku:
    :return:
    """
    q = queue.Queue()
    for i in range(9):
        for j in range(9):
            square = sudoku.get_square(i, j)
            for constraint in square.constraints:
                q.put(constraint)

    while not q.empty():
        arc = q.get()
        source_square = sudoku.get_square(arc.source.row, arc.source.column)
        target_square = sudoku.get_square(arc.target.row, arc.target.column)
        if revise(source_square, target_square):
            # Does not check if arc is already in queue
            for a in source_square.constraints:
                q.put(a)


def revise(source_square, target_square):
    """

    :param source_square:
    :param target_square:
    :return:
    """
    revised = False
    if len(target_square.get_domain()) == 1:
        try:
            source_square.get_domain().remove(target_square.get_domain()[0])
            revised = True
            if len(source_square.get_domain()) == 1:
                source_square.is_clue = True
        except ValueError:
            pass
    return revised
