import numpy as np
from Board import Board
from Solver import Solver
from ExhaustiveSolver import ExhaustiveSolver

class GenerationalSolver(Solver):

    _solver = ExhaustiveSolver(2)
    _cache = dict()
    _redundancy_cache = dict()

    def __init__(self, depth=3, survivors=5):
        self._depth = depth
        self._solver = ExhaustiveSolver(depth)
        self._survivors = survivors

    def clone(self):
        return GenerationalSolver(self._depth, self._survivors)

    def clear_cache(self):
        self._cache = dict()
        self._redundancy_cache = dict()

    def _find_best_result(self, results):
        max = -1
        best = [-1]
        for moves, score, table in results:
            if score > max or score == max and len(moves) < len(best):
                best = moves
                max = score
        return best

    # board is a board, this isn't modified
    # choices is a list of tuple: moves: tuple(int), score: int)
    # choices should be filtered down before being passed in
    def _recursive_choose(self, choices, max_score=144):
        if max_score in map(lambda x: x[1], choices):
            max = -1
            best = [-1]
            for moves, score, table in choices:
                if score > max or score == max and len(moves) < len(best):
                    best = moves
                    max = score
            return best
        else:
            all_choices = []
            for moves, score, table in choices:
                raw_choices = self._solver.choose(table, raw=True)
                qualified_choices = map(lambda x: (moves + x[0], x[1][1], x[1][0]), raw_choices.items())
                all_choices.extend(qualified_choices)
            best = self._find_best_result(all_choices)
            all_choices = filter(lambda x: len(x[0]) <= len(best), all_choices)
            best_choices = sorted(all_choices, key=lambda x: x[1], reverse=True)[:self._survivors]
            return self._recursive_choose(best_choices, max_score)

    def choose(self, board):
        return self._recursive_choose([((), -1, board)], board.max_score)
