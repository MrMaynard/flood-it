import random
from Solver import Solver

class RandomSolver(Solver):

    def choose(self, board):
        return [random.randint(board.low, board.high + 1)]
