import numpy as np
from Board import Board
from Solver import Solver
from ExhaustiveSolver import ExhaustiveSolver

class GenerationalSolver(Solver):

    _solver = ExhaustiveSolver(2)
    _cache = dict()
    _redundancy_cache = dict()

    def __init__(self, depth=3, survivors=5):
        self._solver = ExhaustiveSolver(depth)
        self._survivors = survivors


    def clear_cache(self):
        self._cache = dict()
        self._redundancy_cache = dict()

    def _find_best_result(self, results):
        max = -1
        best = [-1]
        for key, value in results:
            if value > max or value == max and len(key) < len(best):
                best = key
                max = value
        return best

    # board is a board, this isn't modified
    # choices is a list of tuple: moves: tuple(int), score: int)
    # choices should be filtered down before being passed in
    def _recursive_choose(self, choices):
        if self._board.max_score in map(lambda x: x[1], choices):
            max = -1
            best = [-1]
            for key, value in choices:
                if value > max or value == max and len(key) < len(best):
                    best = key
                    max = value
            return best
        else:
            all_choices = []
            moves = map(lambda x: x[0], choices)
            for moveset in moves:
                temp_clone = Board(self._board)
                for move in moveset:
                    temp_clone.flood(move)
                raw_choices = self._solver.choose(temp_clone, raw=True)
                qualified_choices = map(lambda x: (moveset + x[0], x[1]), raw_choices.items())
                all_choices.extend(qualified_choices)
            best = self._find_best_result(all_choices)
            all_choices = filter(lambda x: len(x[0]) <= len(best), all_choices)
            best_choices = sorted(all_choices, key=lambda x: x[1], reverse=True)[:self._survivors]
            return self._recursive_choose(best_choices)

    def choose(self, board):
        self._board = board
        return self._recursive_choose([((), -1)])
