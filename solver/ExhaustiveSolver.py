import numpy as np
from Board import Board
from Solver import Solver


class ExhaustiveSolver(Solver):

    _cache = dict()
    _redundancy_cache = dict()
    _movement_cache = dict()

    def __init__(self, depth=2):
        self._depth = depth

    def clone(self):
        return ExhaustiveSolver(self._depth)


    def clear_cache(self):
        self._cache = dict()
        self._redundancy_cache = dict()
        self._movement_cache = dict()

    def choose(self, board, raw=False):

        if self._depth == 1:
            return self._solver.choose(board)

        # generate a list of all possible options (or pull it from cache)
        options = range(board.low, board.high + 1)
        movement_key = (hash(str(board._board)), self._depth)
        if movement_key not in self._movement_cache:
            all_combinations = []
            combinations = list([(x,) for x in options])
            all_combinations.extend(combinations)
            for i in range(1, self._depth):
                new_combinations = []
                for combination in combinations:
                    for option in options:
                        if option != combination[-1]:
                            new_combinations.append(tuple(list(combination) + [option]))
                all_combinations.extend(new_combinations)
                combinations = new_combinations
            self._movement_cache[movement_key] = all_combinations
        all_combinations = filter(lambda p: p[0] != board.existing_color(), self._movement_cache[movement_key])

        # try all options (with memoized boards for sub-movements)
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
            if len(combination) < self._depth:
                self._cache[combination] = working_table
            results[combination] = (working_table, len(working_table.get_shape(working_table.existing_color())))

        if raw:
            return results
        else:
            max = -1
            best = [-1]
            for key, value in results.iteritems():
                if value[1] > max or value[1] == max and len(key) < len(best):
                    best = key
                    max = value[1]
            return best
