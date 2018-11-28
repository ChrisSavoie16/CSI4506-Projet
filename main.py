import os
import time
from backtrack.Backtrack import backtrack_solve
from utils.SudokuInitialisation import init_sudoku

with open(os.path.join("data", "sudokus_start.txt")) as f:
    sudokus = f.readlines()

with open(os.path.join("data", "sudokus_finish.txt")) as f:
    solutions = f.readlines()

total_time = 0
max_time = 0
min_time = 0
failure_count = 0
for i in range(len(sudokus)):
    problem = init_sudoku(sudokus[i])
    solution = init_sudoku(solutions[i])
    start_time = time.time()
    backtrack_solve(problem)
    exec_time = time.time() - start_time
    if problem == solution:
        total_time += exec_time

        if i == 0:
            max_time = exec_time
            min_time = exec_time

        if exec_time > max_time:
            max_time = exec_time

        if exec_time < min_time:
            min_time = exec_time
    else:
        failure_count += 1
    print(exec_time, str(i + 1) + "/" + str(len(sudokus)))

print("Total: ", total_time)
print("Maximum: ", max_time)
print("Minimum: ", min_time)
print("Average: ", total_time / len(sudokus))
print("Failure Count: ", failure_count)

