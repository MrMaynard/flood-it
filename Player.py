from solver.GreedySolver import GreedySolver
from solver.RandomSolver import RandomSolver
from solver.ExhaustiveSolver import ExhaustiveSolver
from solver.GenerationalSolver import GenerationalSolver
from solver.GraphSolver import GraphSolver
from Board import Board
import time
import threading
import numpy as np


def test(solver, trials=50):
    total_moves = 0
    start = time.time()
    for trial in range(trials):
        board = Board()
        solver.clear_cache()
        moves = 0
        while not board.is_solved():
            choices = solver.choose(board)
            for choice in choices:
                board.flood(choice)
                moves += 1
                #print "------------- " + str(choice) + " --------------"
                #print board._board
        total_moves += moves
    average_time = (time.time() - start) / float(trials)
    average_moves = total_moves / float(trials)
    return average_moves, average_time


def test_multithreaded(solver, trials=20, threads=4):
    def _multithreaded_backend(func, args, res):
        res.append(func(*args))

    res = []
    thread_trials = trials / threads
    thread_list = []
    for i in range(threads):
        thread_list.append(threading.Thread(target=_multithreaded_backend, args=(test, (solver.clone(), thread_trials), res)))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    return np.mean(map(lambda x: x[0], res)), np.mean(map(lambda x: x[1], res))


def main():

    # graph solver
    for s in range(10, 12):
        graph_moves, graph_time = test(GraphSolver(s))
        print "GraphSolver (" + str(s) + ") finished in an average of", graph_moves, \
            "moves and took an average of", graph_time, "s"

    # # random solver
    # random_moves, random_time = test(RandomSolver())
    # print "RandomSolver finished in an average of", random_moves, \
    #     "moves and took an average of", random_time, "s"
    #
    # # greedy solver
    # greedy_moves, greedy_time = test(GreedySolver())
    # print "GreedySolver finished in an average of", greedy_moves, \
    #     "moves and took an average of", greedy_time, "s"
    #
    # #for d in range(2, 4):
    # #    exhaustive_moves, exhaustive_time = test(ExhaustiveSolver(d))
    # #    print "ExhaustiveSolver (" + str(d) + ") finished in an average of", exhaustive_moves, \
    # #        "moves and took an average of", exhaustive_time, "s"
    #
    # for d in range(2, 4):
    #     for survivors in [10, 15, 20]:
    #         generational_moves, generational_time = test(GenerationalSolver(depth=d, survivors=survivors))
    #         print "GenerationalSolver (" + str(d) + " / " + str(survivors) + ") finished in an average of",\
    #             generational_moves, "moves and took an average of", generational_time, "s"

if __name__ == "__main__":
    main()