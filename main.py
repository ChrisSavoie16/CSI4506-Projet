import os
import time
import datetime
from backtrack.Backtrack import backtrack_solve
from AC3.AC3 import AC3
from utils.SudokuInitialisation import init_sudoku


def basic_comparison():
    """
    Writes results in result/results.txt
    :return:
    """
    with open(os.path.join("data", "sudokus_start.txt")) as f:
        sudokus = f.readlines()

    total_bt_time = 0
    total_ac3_time = 0
    total_ac3_bt_time = 0
    total_combined_time = 0
    max_bt_time = 0
    max_ac3_time = 0
    max_ac3_bt_time = 0
    max_combined_time = 0
    min_bt_time = 0
    min_ac3_time = 0
    min_ac3_bt_time = 0
    min_combined_time = 0

    for problem in sudokus:

        bt_time = backtrack_test(problem)
        total_bt_time += bt_time

        if max_bt_time == 0:
            max_bt_time = bt_time
            min_bt_time = bt_time
        if bt_time > max_bt_time:
            max_bt_time = bt_time
        if bt_time < min_bt_time:
            min_bt_time = bt_time

        ac3_time, ac3_bt_time = ac3_test(problem)
        combined_time = ac3_time + ac3_bt_time

        total_ac3_time += ac3_time
        total_ac3_bt_time += ac3_bt_time
        total_combined_time += combined_time

        if max_ac3_time == 0:
            max_ac3_time = ac3_time
            min_ac3_time = ac3_time
        if ac3_time > max_ac3_time:
            max_ac3_time = ac3_time
        if ac3_time < min_ac3_time:
            min_ac3_time = ac3_time

        if max_ac3_bt_time == 0:
            max_ac3_bt_time = ac3_bt_time
            min_ac3_bt_time = ac3_bt_time
        if ac3_bt_time > max_ac3_bt_time:
            max_ac3_bt_time = ac3_bt_time
        if ac3_bt_time < min_ac3_bt_time:
            min_ac3_bt_time = ac3_bt_time

        if max_combined_time == 0:
            max_combined_time = combined_time
            min_combined_time = combined_time
        if combined_time > max_combined_time:
            max_combined_time = combined_time
        if combined_time < min_combined_time:
            min_combined_time = combined_time

    print("\nTotal backtrack time: ", total_bt_time, file=open(os.path.join("result", "results.txt"), "a"))
    print("Minimum backtrack time: ", min_bt_time, file=open(os.path.join("result", "results.txt"), "a"))
    print("Maximum backtrack time: ", max_bt_time, file=open(os.path.join("result", "results.txt"), "a"))

    print("\nTotal AC3 time: ", total_ac3_time, file=open(os.path.join("result", "results.txt"), "a"))
    print("Minimum AC3 time: ", min_ac3_time, file=open(os.path.join("result", "results.txt"), "a"))
    print("Maximum AC3 time: ", max_ac3_time, file=open(os.path.join("result", "results.txt"), "a"))

    print("\nTotal backtrack after AC3 time: ", total_ac3_bt_time,
          file=open(os.path.join("result", "results.txt"), "a"))
    print("Minimum backtrack after AC3 time: ", min_ac3_bt_time, file=open(os.path.join("result", "results.txt"), "a"))
    print("Maximum backtrack after AC3 time: ", max_ac3_bt_time, file=open(os.path.join("result", "results.txt"), "a"))

    print("\nTotal combined time: ", total_combined_time, file=open(os.path.join("result", "results.txt"), "a"))
    print("Minimum combined time: ", min_combined_time, file=open(os.path.join("result", "results.txt"), "a"))
    print("Maximum combined time: ", max_combined_time, file=open(os.path.join("result", "results.txt"), "a"))


def basic_analysis():
    with open(os.path.join("data", "sudokus_start.txt")) as f:
        sudokus = f.readlines()

    improvement_count = 0
    total_improvement = 0
    min_improvement = 0
    max_improvement = 0
    decrease_count = 0
    total_decrease = 0
    min_decrease = 0
    max_decrease = 0

    for problem in sudokus:
        bt_time = backtrack_test(problem)
        ac3_time, ac3_bt_time = ac3_test(problem)
        combined_time = ac3_time + ac3_bt_time

        if bt_time < combined_time:
            decrease_count += 1
            decrease_time = bt_time - combined_time
            total_decrease += decrease_time
            if max_decrease == 0:
                max_decrease = decrease_time
                min_decrease = decrease_time
            if decrease_time > max_decrease:
                max_decrease = decrease_time
            if decrease_time < min_decrease:
                min_decrease = decrease_time
        else:
            improvement_count += 1
            improvement_time = combined_time - bt_time
            total_improvement += improvement_time
            if max_improvement == 0:
                max_improvement = improvement_time
                min_improvement = improvement_time
            if improvement_time > max_improvement:
                max_improvement = improvement_time
            if improvement_time < min_improvement:
                min_improvement = improvement_time

    print("\nImprovement count: ", improvement_count, file=open(os.path.join("result", "results.txt"), "a"))
    print("Maximum improvement time: ", max_improvement, file=open(os.path.join("result", "results.txt"), "a"))
    print("Minimum improvement time: ", min_improvement, file=open(os.path.join("result", "results.txt"), "a"))
    print("Average improvement time: ", total_improvement / improvement_count,
          file=open(os.path.join("result", "results.txt"), "a"))

    print("\nDecrease count: ", decrease_count, file=open(os.path.join("result", "results.txt"), "a"))
    print("Maximum decrease time: ", max_decrease, file=open(os.path.join("result", "results.txt"), "a"))
    print("Minimum decrease time: ", min_decrease, file=open(os.path.join("result", "results.txt"), "a"))
    print("Average decrease time: ", total_decrease / decrease_count,
          file=open(os.path.join("result", "results.txt"), "a"))


def backtrack_test(problem):
    """
    Runs backtrack algorithm and returns the execution time
    :param problem:
    :return:
    """
    problem = init_sudoku(problem)
    start_time = time.time()
    backtrack_solve(problem)
    return time.time() - start_time


def ac3_test(problem):
    """
    Runs AC-3 and backtrack and returns execution time for both
    :param problem:
    :return:
    """
    sudoku = init_sudoku(problem)
    ac3_start = time.time()
    AC3(sudoku)
    ac3_end = time.time()

    bt_start = time.time()
    backtrack_solve(sudoku)
    bt_end = time.time()

    return ac3_end - ac3_start, bt_end - bt_start


if __name__ == "__main__":
    start = datetime.datetime.now()
    print("Start time of program: ", start.isoformat(), file=open(os.path.join("result", "results.txt"), "a"))
    print("\nStart of 5 basic comparison", file=open(os.path.join("result", "results.txt"), "a"))
    for i in range(5):
        basic_comparison()

    print("\nStart of 5 basic analysis", file=open(os.path.join("result", "results.txt"), "a"))
    for j in range(5):
        basic_analysis()
