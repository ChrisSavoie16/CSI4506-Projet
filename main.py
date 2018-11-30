import os
import time
import sys
from backtrack.Backtrack import backtrack_solve
from AC3.AC3 import AC3
from utils.SudokuInitialisation import init_sudoku


def main():

    with open(os.path.join("data", "sudokus_start.txt")) as f:
        sudokus = f.readlines()

    total_time = 0
    max_time = 0
    min_time = 0

    for i in range(len(sudokus)):
        problem = init_sudoku(sudokus[i])
        start_time = time.time()
        backtrack_solve(problem)
        exec_time = time.time() - start_time
        total_time += exec_time

        if i == 0:
            max_time = exec_time
            min_time = exec_time

        if exec_time > max_time:
            max_time = exec_time

        if exec_time < min_time:
            min_time = exec_time
        print(exec_time, str(i + 1) + "/" + str(len(sudokus)))

    print("Total: ", total_time)
    print("Maximum: ", max_time)
    print("Minimum: ", min_time)
    print("Average: ", total_time / len(sudokus))


def test_ac3():
    with open(os.path.join("data", "sudokus_start.txt")) as f:
        sudokus = f.readlines()

    for problem in sudokus:
        sudoku = init_sudoku(problem)
        start = time.time()
        backtrack_solve(sudoku)
        end = time.time()

        sudoku = init_sudoku(problem)
        a_start = time.time()
        AC3(sudoku)
        a_end = time.time()

        ab_start = time.time()
        backtrack_solve(sudoku)
        ab_end = time.time()
        print(end - start, a_end - a_start, ab_end - ab_start)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_ac3()