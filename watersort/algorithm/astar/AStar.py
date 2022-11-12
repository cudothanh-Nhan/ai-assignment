import copy
import json


class Move:
    def __init__(self, _from: int, _to: int) -> None:
        self._from = _from
        self._to = _to

    def __str__(self) -> str:
        return str(self._from + 1) + "->" + str(self._to + 1)


def generate_id() -> str:
    None


class Glass:

    colors: list[int]

    def __init__(self, colors: list[int]) -> None:
        self.colors = colors

    def get_curr_capacity(self) -> int:
        return len(self.colors)

    def top(self) -> int:
        if (len(self.colors) == 0):
            return None
        return self.colors[-1]

    def pop(self) -> int:
        if (len(self.colors) == 0):
            return None
        return self.colors.pop()

    def get_num_blocks(self) -> int:
        colors_len = len(self.colors)
        if (colors_len == 0):
            return 0
        num_blocks = 1
        for i in range(1, colors_len):
            if (self.colors[i] != self.colors[i - 1]):
                num_blocks += 1

        return num_blocks


class GameBoard:
    MAX_SIZE_OF_GLASS: int = 4

    glasses: list[Glass]
    num_colors: int
    move: Move

    _str: str
    _num_blocks: int

    @staticmethod
    def set_max_size_of_glass(size: int) -> None:
        GameBoard.MAX_SIZE_OF_GLASS = size

    def __init__(self, data: list[list[int]], num_colors: int) -> None:
        self.glasses = list()
        for colors in data:
            self.glasses.append(Glass(colors))
        self.num_colors = num_colors
        self.move = None

        # For caching
        self._str = None
        self._num_blocks = None

    def __eq__(self, __o: 'GameBoard') -> bool:
        if (not isinstance(__o, GameBoard)):
            return False
        return self.to_str() == __o.to_str()

    def clone_with_move(self, move: Move) -> 'GameBoard':
        clone = copy.deepcopy(self)
        clone._str = None
        clone._num_blocks = None
        clone.move = move
        return clone

    def get_num_blocks(self) -> int:
        if self._num_blocks == None:
            self._num_blocks: int = 0
            for glass in self.glasses:
                self._num_blocks += glass.get_num_blocks()
        return self._num_blocks

    def is_complete(self) -> bool:
        return self._num_blocks == self.num_colors

    def to_str(self) -> str:
        if self._str == None:
            self._str = ",".join([str(glass.colors) for glass in self.glasses])
        return self._str

    def transit(self, move: Move) -> 'GameBoard':
        if (self.glasses[move._to].get_curr_capacity() == GameBoard.MAX_SIZE_OF_GLASS):
            return None

        if (self.glasses[move._from].top() == None):
            return None

        new_board = self.clone_with_move(move)
        from_glass = new_board.glasses[move._from]
        to_glass = new_board.glasses[move._to]

        if from_glass.top() == to_glass.top() or to_glass.top() == None:
            to_glass_remain_capacity = GameBoard.MAX_SIZE_OF_GLASS - \
                to_glass.get_curr_capacity()

            num_of_tops = 1
            for i in reversed(range(from_glass.get_curr_capacity() - 1)):
                if (from_glass.colors[i] != from_glass.top()):
                    break
                num_of_tops += 1

            if num_of_tops > to_glass_remain_capacity:
                return None

            while to_glass.top() == from_glass.top() or to_glass.top() == None:
                to_glass.colors.append(from_glass.pop())
            return new_board
        return None


class Graph:
    num_steps: int
    start_node: GameBoard

    # B - C
    def __init__(self, start_node: GameBoard) -> None:
        self.start_node = start_node
        self.num_steps = start_node.get_num_blocks() - start_node.num_colors

    # Heuristic function
    def h(self, board: GameBoard) -> int:
        return self.num_steps - board.get_num_blocks()

    def get_neighbors(self, board: GameBoard) -> list[GameBoard]:
        if (board == None):
            return []
        neighbors: list[GameBoard] = list()
        num_glasses = len(board.glasses)
        for i in range(num_glasses):
            for j in range(num_glasses):
                if (i == j):
                    continue
                neighbor = board.transit(Move(i, j))
                if (neighbor != None):
                    neighbors.append(neighbor)

        return neighbors

    def solve_by_astar_algorithm(self):
        openedl: list[GameBoard] = list([self.start_node])
        closedl: list[GameBoard] = list()

        g: dict[str, int] = {}
        g[self.start_node.to_str()] = 0

        # parents contains an adjacency map of all nodes
        parents: dict[str, GameBoard] = {}
        parents[self.start_node.to_str()] = self.start_node

        while len(openedl) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for p in openedl:
                if n == None or g[p.to_str()] + self.h(p) < g[n.to_str()] + self.h(p):
                    n = p
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the self.start_node
            if n.is_complete():
                reconst_path: list[str] = []

                while parents[n.to_str()] != n:
                    reconst_path.append(str(n.move))
                    n = parents[n.to_str()]

                # reconst_path.append(str(self.start_node.move))
                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            neighbors = self.get_neighbors(n)
            for neighbor in neighbors:
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and n node as it's parent
                if neighbor not in openedl and neighbor not in closedl:
                    openedl.append(neighbor)
                    parents[neighbor.to_str()] = n
                    g[neighbor.to_str()] = g[n.to_str()] + 1

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                elif g[neighbor.to_str()] > g[n.to_str()] + 1:
                    g[neighbor.to_str()] = g[n.to_str()] + 1
                    parents[neighbor.to_str()] = n

                    if neighbor in closedl:
                        closedl.remove(neighbor)
                        openedl.append(neighbor)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            if (n != None):
                openedl.remove(n)
                closedl.append(n)
        print('Solution does not exist!')


rounds = [[
    [1, 2, 3, 1],
    [2, 2, 3, 1],
    [3, 1, 2, 3],
    [],
    []
], [
    [1, 2],
    [2, 1],
    []
], [
    [1, 2, 3, 2],
    [1, 4, 4, 1],
    [2, 3, 3, 4],
    [2, 3, 4, 1],
    [],
    []
], [
    [1, 2, 3],
    [2, 1, 3],
    [3, 1, 2],
    [],
    []
]]


class AStar:
    def __init__(self, round: int) -> None:
        round_file = open('watersort/rounds/{}.json'.format(round), 'r')
        json_obj = json.loads(round_file.read())
        init = json_obj['board']
        size = len(set([item for sublist in init for item in sublist]))

        GameBoard.set_max_size_of_glass(json_obj['capacity'])
        board = GameBoard(init, size)
        self.graph = Graph(board)

    def solve(self):
        self.graph.solve_by_astar_algorithm()
