import numpy as np
from Board import Board
from Solver import Solver


class GreedySolver(Solver):

    def test_flood(self, board, color):
        pass

    def choose(self, board):
        results = []
        existing_color = board.existing_color()
        for option in range(board.low, board.high + 1):
            if option != existing_color:
                clone = Board(board)  # todo implement test flood without cloning the whole thing
                flood_shape = clone.flood(option, 0, 0)
                results.append(len(clone.get_shape(clone.existing_color(), boost=flood_shape)))
            else:
                results.append(-1)
        return [np.argmax(results) + board.low]
