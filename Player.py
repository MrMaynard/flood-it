from solver.GreedySolver import GreedySolver
from solver.RandomSolver import RandomSolver
from solver.ExhaustiveSolver import ExhaustiveSolver
from solver.GenerationalSolver import GenerationalSolver
from Board import Board
import time
import numpy as np

def test(solver, trials=100):
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
            # print board._board
            # print "------------- " + str(choice) + " --------------"
        total_moves += moves
    average_time = (time.time() - start) / float(trials)
    average_moves = total_moves / float(trials)
    return average_moves, average_time


def main():

    # random solver
    random_moves, random_time = test(RandomSolver())
    print "RandomSolver finished in an average of", random_moves, \
        "moves and took an average of", random_time, "s"

    # greedy solver
    greedy_moves, greedy_time = test(GreedySolver())
    print "GreedySolver finished in an average of", greedy_moves, \
        "moves and took an average of", greedy_time, "s"

    for d in range(2, 4):
        exhaustive_moves, exhaustive_time = test(ExhaustiveSolver(d))
        print "ExhaustiveSolver (" + str(d) + ") finished in an average of", exhaustive_moves, \
            "moves and took an average of", exhaustive_time, "s"

    for d in range(2, 4):
        for survivors in [5, 10, 15]:
            generational_moves, generational_time = test(GenerationalSolver(depth=d, survivors=survivors))
            print "GenerationalSolver (" + str(d) + " / " + survivors + ") finished in an average of",\
                generational_moves, "moves and took an average of", generational_time, "s"

if __name__ == "__main__":
    main()