import os
import time
import csv
import argparse
from backtrack.Backtrack import backtrack_solve
from AC3.AC3 import AC3
from utils.SudokuInitialisation import init_sudoku


def basic_comparison(file):
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

    print("\nTotal backtrack time: ", total_bt_time, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Minimum backtrack time: ", min_bt_time, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Maximum backtrack time: ", max_bt_time, file=open(os.path.join("result", file + ".txt"), "a"))

    print("\nTotal AC3 time: ", total_ac3_time, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Minimum AC3 time: ", min_ac3_time, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Maximum AC3 time: ", max_ac3_time, file=open(os.path.join("result", file + ".txt"), "a"))

    print("\nTotal backtrack after AC3 time: ", total_ac3_bt_time,
          file=open(os.path.join("result", file + ".txt"), "a"))
    print("Minimum backtrack after AC3 time: ", min_ac3_bt_time, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Maximum backtrack after AC3 time: ", max_ac3_bt_time, file=open(os.path.join("result", file + ".txt"), "a"))

    print("\nTotal combined time: ", total_combined_time, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Minimum combined time: ", min_combined_time, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Maximum combined time: ", max_combined_time, file=open(os.path.join("result", file + ".txt"), "a"))


def basic_analysis(file):
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

    print("\nImprovement count: ", improvement_count, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Maximum improvement time: ", max_improvement, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Minimum improvement time: ", min_improvement, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Average improvement time: ", total_improvement / improvement_count,
          file=open(os.path.join("result", "results.txt"), "a"))

    print("\nDecrease count: ", decrease_count, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Maximum decrease time: ", max_decrease, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Minimum decrease time: ", min_decrease, file=open(os.path.join("result", file + ".txt"), "a"))
    print("Average decrease time: ", total_decrease / decrease_count,
          file=open(os.path.join("result", file + ".txt"), "a"))


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


def str2bool(v):
    """
    Taken from :
    https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse

    Used to parse boolean from cli
    """
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def check_number(value):
    """
    Taken from :
    https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers

    takes positive int from 1 and 400
    """
    ivalue = int(value)
    if ivalue <= 0 or ivalue > 400:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value, must be between 1 and 400" % value)
    return ivalue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysis class for solving sudokus")
    parser.add_argument('-n', '--number', dest='number', nargs='?', const=400, default=400, type=check_number,
                        help='Number of sudoku to use for the analysis. Max is 400, min is 1')
    parser.add_argument('-p', '--percentage', dest='percentage', nargs='?', const=True, type=str2bool, default=True,
                        help='Decides if percentage is used, True by default.')
    parser.add_argument('-o', '--ordered', dest='ordered', const=True, type=str2bool, nargs='?', default=True,
                        help='Decides if the results are are sorted grouped by hint number, True by default')
    parser.add_argument('-r', '--results', dest='results', default="results",
                        help='File name to put results in, file located in result folder. File will overwrite current'
                             'file. Default file is "results"')
    parser.add_argument('--basic_comparison', dest='basic_comparison',
                        const=False, type=str2bool, nargs='?', default=False,
                        help='Performs basic comparison, ignores all arguments but results file, default is False')
    parser.add_argument('--basic_analysis', dest='basic_analysis', const=False, type=str2bool, nargs='?', default=False,
                        help='Performs basic analysis, ignores all arguments but results file, default is False')
    args = parser.parse_args()

    if args.basic_comparison and args.basic_analysis:
        raise argparse.ArgumentTypeError('Only comparison or analysis can be true, not both')
    elif args.basic_comparison:
        basic_comparison(args.results)
    elif args.basic_analysis:
        basic_analysis(args.results)

    with open(os.path.join("data", "sudokus_start.txt")) as f:
        sudokus = f.readlines()

    if args.percentage:
        fields = ['Average Ratio', 'Max Ratio', 'Min Ratio']
    else:
        fields = ['Average Backtrack', 'Max Backtrack', 'Min Backtrack',
              'Average AC3', 'Max AC3', 'Min AC3',
              'Average AC3 Backtrack', 'Max AC3 Backtrack', 'Min AC3 Backtrack',
              'Average Combined', 'Max Combined', 'Min Combined']
    if args.ordered:
        fields.insert(0, 'Example Count')
        fields.insert(0, 'Hint Count')

    file = open(os.path.join('result', args.results+'.csv'), "w+")
    writer = csv.writer(file)

    writer.writerow(fields)

    data = []

    if args.ordered:
        for i in range(81):
            if args.percentage:
                data.append([0, 0, 0, 99999])
            else:
                data.append([0, 0, 0, 99999, 0, 0, 99999, 0, 0, 99999, 0, 0, 99999])
    else:
        if args.percentage:
            data.append([0, 0, 99999])
        else:
            data.append([0, 0, 99999, 0, 0, 99999, 0, 0, 99999, 0, 0, 99999])

    for i in range(args.number):
        problem = sudokus[i]

        backtrack_time = backtrack_test(problem)
        ac3_time, abacktrack_time = ac3_test(problem)

        if args.ordered:
            count = 0
            for j in problem:
                if j != "0":
                    count += 1
            data[count][0] += 1
            if args.percentage:
                percentage = (ac3_time + abacktrack_time) / backtrack_time
                data[count][1] += percentage
                if percentage > data[count][2]:
                    data[count][2] = percentage
                if percentage < data[count][3]:
                    data[count][3] = percentage
            else:
                data[count][1] += backtrack_time
                if backtrack_time > data[count][2]:
                    data[count][2] = backtrack_time
                if backtrack_time < data[count][3]:
                    data[count][3] = backtrack_time
                data[count][4] += ac3_time
                if ac3_time > data[count][5]:
                    data[count][5] = ac3_time
                if ac3_time < data[count][6]:
                    data[count][6] = ac3_time
                data[count][7] += abacktrack_time
                if abacktrack_time > data[count][8]:
                    data[count][8] = abacktrack_time
                if abacktrack_time < data[count][9]:
                    data[count][9] = abacktrack_time
                combined_time = ac3_time + abacktrack_time
                data[count][10] += combined_time
                if backtrack_time > data[count][11]:
                    data[count][11] = combined_time
                if backtrack_time < data[count][12]:
                    data[count][12] = combined_time
        else:
            if args.percentage:
                percentage = (ac3_time + abacktrack_time) / backtrack_time
                data[0] += percentage
                if percentage > data[1]:
                    data[1] = percentage
                if percentage < data[2]:
                    data[2] = percentage
            else:
                data[0] += backtrack_time
                if backtrack_time > data[1]:
                    data[1] = backtrack_time
                if backtrack_time < data[2]:
                    data[2] = backtrack_time
                data[3] += ac3_time
                if ac3_time > data[4]:
                    data[4] = ac3_time
                if ac3_time < data[5]:
                    data[5] = ac3_time
                data[6] += abacktrack_time
                if abacktrack_time > data[7]:
                    data[7] = abacktrack_time
                if abacktrack_time < data[8]:
                    data[8] = abacktrack_time
                combined_time = ac3_time + abacktrack_time
                data[9] += combined_time
                if backtrack_time > data[10]:
                    data[10] = backtrack_time
                if backtrack_time < data[11]:
                    data[11] = backtrack_time

    if args.ordered:
        for i in range(81):
            if data[i][0] > 0:
                if args.percentage:
                    data[i][1] = data[i][1] / data[i][0]
                else:
                    for j in range(4):
                        data[i][j*3 + 1] = data[i][j*3 + 1] / data[i][0]
            data[i].insert(0, i+1)
        writer.writerows(data)
    else:
        if args.percentage:
            data[0] = data[0] / args.number
        else:
            for j in range(4):
                data[j * 3] = data[j * 3] / args.number
        writer.writerow(data)
