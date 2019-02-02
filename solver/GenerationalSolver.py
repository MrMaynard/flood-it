import numpy as np
from Board import Board
from GreedySolver import GreedySolver
from Solver import Solver


class GenerationalSolver(Solver):

    _solver = GreedySolver()
    _cache = dict()
    _redundancy_cache = dict()

    def __init__(self, depth=2):
        self._depth = depth


    def clear_cache(self):
        self._cache = dict()
        self._redundancy_cache = dict()

    def choose(self, board):

        if self._depth == 1:
            return self._solver.choose(board)

        options = range(board.low, board.high + 1)

        all_combinations = []
        combinations = list([(x,) for x in filter(lambda p: p != board.existing_color(), options)])
        all_combinations.extend(combinations)
        for i in range(1, self._depth):
            new_combinations = []
            for combination in combinations:
                for option in options:
                    if option != combination[-1]:
                        new_combinations.append(tuple(list(combination) + [option]))
            all_combinations.extend(new_combinations)
            combinations = new_combinations

        results = dict()
        self._cache[()] = board
        for combination in all_combinations:
            closest_relative = combination[:-1]
            while closest_relative not in self._cache:
                closest_relative = closest_relative[:-1]
            working_table = Board(self._cache[closest_relative])
            working_moves = combination[len(closest_relative):]
            for move in working_moves:
                working_table.flood(move)
            if(len(combination) < self._depth):
                self._cache[combination] = working_table
            results[combination] = len(working_table.get_shape(working_table.get(0, 0)))

        return max(results.iterkeys(), key=(lambda key: results[key]))
