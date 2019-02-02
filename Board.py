import numpy as np


class Board(object):

    def __init__(self, board=None, shape=(12, 12), low=1, high=6):
        if board:
            self._board = np.copy(board._board)
            self.low = np.min(self._board)
            self.high = np.max(self._board)
        else:
            self._board = np.random.randint(low, high + 1, size=shape)
            self.low = low
            self.high = high
        self.max_score = shape[0] * shape[1]

    def _get_neighbors(self, x, y, value):
        results = []
        for check in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            temp_x = x + check[0]
            temp_y = y + check[1]
            if temp_x >= 0 and temp_x < self._board.shape[0]:
                if temp_y >= 0 and temp_y < self._board.shape[1]:
                    if self._board[temp_x][temp_y] == value:
                        results.append((temp_x, temp_y))
        return results

    # gets the shape starting from some set of coordinates
    # returns a set of pixel coordinates for the shape
    def get_shape(self, value, x=0, y=0, boost=None):
        shape = set()
        if boost:
            new_neighbors = boost
        else:
            new_neighbors = {(x, y)}
        while new_neighbors:
            next_new_neighbors = set()
            for neighbor in new_neighbors:
                temp = self._get_neighbors(neighbor[0], neighbor[1], value)
                for result in temp:
                    if result not in shape:
                        next_new_neighbors.add(result)
            shape.update(new_neighbors)
            new_neighbors = next_new_neighbors
        return shape

    def get(self, x, y):
        return self._board[x][y]

    # gets the shape starting from some set of coordinates
    # returns a set of pixel coordinates for the shape
    def test_shape(self, value, x=0, y=0):
        shape = {(x, y)}
        new_neighbors = set()
        if self._board[x + 1][y] == value:
            new_neighbors.add((x + 1, y))
        if self._board[x][y + 1] == value:
            new_neighbors.add((x, y + 1))

        while new_neighbors:
            next_new_neighbors = set()
            for neighbor in new_neighbors:
                temp = self._get_neighbors(neighbor[0], neighbor[1], value)
                for result in temp:
                    if result not in next_new_neighbors and result not in new_neighbors and result not in shape:
                        next_new_neighbors.add(result)
            shape.update(new_neighbors)
            new_neighbors = next_new_neighbors
        return shape

    # floods with *choice* from 0,0
    def flood(self, choice, x=0, y=0):
        choice_shape = self.get_shape(self._board[x][y], x, y)
        for pixel in choice_shape:
            self._board[pixel[0], pixel[1]] = choice
        return choice_shape

    # returns whether or not the board is solved
    def is_solved(self):
        return len(np.unique(self._board)) == 1

    def existing_color(self):
        return self._board[0][0]

    def hash_value(self):
        return hash(str(self._board))