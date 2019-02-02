import numpy as np
from Board import Board
from Solver import Solver
from graph.Node import Node
from scipy.sparse import csgraph

class GraphSolver(Solver):

    def test_flood(self, board, color):
        pass

    def __init__(self, samples=2):
        self._samples = samples

    def clone(self):
        return GraphSolver(self._samples)

    _lut = dict()
    def _add_children(self, board, node):
        self._lut[node.coordinates] = node
        x = node.coordinates[0]
        y = node.coordinates[1]
        for check in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            temp_x = x + check[0]
            temp_y = y + check[1]
            if temp_x >= 0 and temp_x < board._board.shape[0]:
                if temp_y >= 0 and temp_y < board._board.shape[1]:
                    if (temp_x, temp_y) not in self._lut:
                        temp = Node(board._board[temp_x][temp_y], (temp_x, temp_y))
                        self._add_children(board, temp)
                    else:
                        temp = self._lut[(temp_x, temp_y)]
                    if (temp_x, temp_y) not in map(lambda x: x[0], node.links) and \
                            node.coordinates not in map(lambda x: x[0], temp.links):
                        if temp.value == node.value:
                            node.links.append((temp.coordinates, 0.0000001))
                            temp.links.append((node.coordinates, 0.0000001))
                        else:
                            node.links.append((temp.coordinates, 1))
                            temp.links.append((node.coordinates, 1))



    def _build_graph(self, board):
        self._root = Node(board.get(0, 0), (0, 0))
        self._lut[(0, 0)] = self._root
        self._add_children(board, self._root)

    def _discretize_coordinates(self, board, (r, c)):
        return c + (r * board._board.shape[0])  # TODO should this be shape[1]? try non-square charts

    def _reverse_discretize(self, board, d):
        r = d / board._board.shape[0]
        c = d % board._board.shape[0]
        return (r, c)

    def _build_adjacency_matrix(self, board):
        num_nodes = board._board.shape[0] * board._board.shape[1]
        matrix = np.full((num_nodes, num_nodes), np.inf)
        for x in range(board._board.shape[0]):
            for y in range(board._board.shape[1]):
                discrete_coordinates = self._discretize_coordinates(board, (x, y))
                node = self._lut[(x, y)]
                links = node.links
                links_discrete_coordinates = map(lambda x: (self._discretize_coordinates(board, x[0]), x[1]), links)
                matrix[discrete_coordinates][discrete_coordinates] = 0
                for l in links_discrete_coordinates:
                    matrix[discrete_coordinates][l[0]] = l[1]
        self._matrix = matrix

    def minDistance(self, dist, queue):
        minimum = np.inf
        min_index = -1
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def dijkstra(self, graph):
        row = len(graph)
        col = len(graph[0])
        dist = [np.inf] * row
        parent = [-1] * row
        dist[0] = 0
        queue = []
        rows = range(row)
        np.random.shuffle(rows)
        for i in rows:
            queue.append(i)
        while queue:
            u = self.minDistance(dist, queue)
            if u in queue:
                queue.remove(u)
            columns = range(col)
            np.random.shuffle(columns)
            for i in columns:
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
        return dist, parent


    def choose_one(self, board):
            self.V = board._board.shape[0] * board._board.shape[1]
            self._lut = dict()
            self._build_graph(board)
            self._build_adjacency_matrix(board)
            matrix_as_list = []
            for r in range(self._matrix.shape[0]):
                matrix_as_list.append(self._matrix[r].tolist())
            distances, steps = self.dijkstra(matrix_as_list)

            # take the move that minimizes the most distance (there may be uncaptured paths to each node)
            # construct all paths
            paths = []
            for node in range(len(distances)):
                target_node = node
                paths.append([])
                while target_node != 0:
                    paths[node].append(target_node)
                    target_node = steps[target_node]
            for p in paths:
                p.reverse()
            qualified_paths = [map(lambda x: self._reverse_discretize(board, x), p) for p in paths]
            choice_paths = [map(lambda x: board.get(x[0], x[1]), p) for p in qualified_paths]
            all_choices = []
            for path in choice_paths:
                temp = []
                last_value = -1
                for item in path:
                    if item != last_value:
                        last_value = item
                        temp.append(item)
                all_choices.append(temp)
            trimmed_choices = [x[1:] if len(x) > 0 and x[0] == board.existing_color() else x for x in all_choices]
            choices = filter(lambda x: len(x) > 0, trimmed_choices)
            first_choices = map(lambda x: x[0], choices)
            choice_counts = np.bincount(first_choices)
            most_frequent_choice = np.argmax(choice_counts)
            return [most_frequent_choice]


            # fully move to farthest node
            # target_node = np.argmax(distances)
            # path = []
            # while target_node != 0:
            #     path.append(target_node)
            #     target_node = steps[target_node]
            # path.reverse()
            # true_path = map(lambda x: self._reverse_discretize(board, x), path)
            # raw_choices = map(lambda x: board.get(x[0], x[1]), true_path)
            # choices = []
            # last_value = -1
            # for item in raw_choices:
            #     if item != last_value:
            #         last_value = item
            #         choices.append(item)
            # return choices
    def choose(self, board):
        votes = []
        for s in range(self._samples):
            votes.append(self.choose_one(board)[0])
        vote_counts = np.bincount(votes)
        return [np.argmax(vote_counts)]

