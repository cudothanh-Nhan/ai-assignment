import copy

MAX_SIZE_OF_GLASS = 6


class Move:
    def __init__(self, _from: int, _to: int) -> None:
        self._from = _from
        self._to = _to

    def __str__(self) -> str:
        return self._from + "->" + self._to


def generate_id() -> str:
    None


class Glass:
    colors: list[int]

    def __init__(self, colors: list[int]) -> None:
        self.colors = colors

    def get_curr_capacity(self) -> int:
        return len(self.colors)

    def top(self) -> int:
        return self.colors[-1]

    def pop(self) -> int:
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
    glasses: list[Glass]
    num_colors: int
    move: Move

    def __init__(self, data: list[list[int]], num_colors: int) -> None:
        self.glasses = list()
        for colors in data:
            self.glasses.append(Glass(colors))
        self.num_colors = num_colors

    def __eq__(self, __o: 'GameBoard') -> bool:
        if (not isinstance(__o, GameBoard)):
            return False
        return self.to_str() == __o.to_str()

    def clone_with_move(self, move: Move) -> 'GameBoard':
        clone = copy.deepcopy(self)
        clone.transit = move
        return clone

    def get_num_blocks(self) -> int:
        num_blocks: int = 0
        for glass in self.glasses:
            num_blocks += glass.get_num_blocks()
        return num_blocks

    def is_complete(self) -> bool:
        return self.get_num_blocks() == self.num_colors

    def to_str(self) -> str:
        s = ""
        for glass in self.glasses:
            s += str(glass.colors)
        return s

    def transit(self, move: Move) -> 'GameBoard':
        if (MAX_SIZE_OF_GLASS - self.glasses[move._to].get_curr_capacity == MAX_SIZE_OF_GLASS):
            return None

        new_board = self.clone_with_move(move)
        from_glass = new_board.glasses[move._from]
        to_glass = new_board.glasses[move._to]

        if from_glass.top() == to_glass.top():
            to_glass_remain_capacity = MAX_SIZE_OF_GLASS - \
                to_glass.get_curr_capacity()
            if (from_glass[from_glass.get_curr_capacity() - 2 - to_glass_remain_capacity] == to_glass.top()):
                return None
            while to_glass.top() == from_glass.top:
                to_glass.colors.append(from_glass.pop())
            return new_board
        return None


class Graph:
    num_steps: int

    # B - C
    def __init__(self, num_colors: int, num_init_blocks: int) -> None:
        self.num_steps = num_init_blocks - num_colors

    # Heuristic function
    def h(self, board: GameBoard) -> int:
        return self.num_steps - board.get_num_blocks()

    def get_neighbors(self, board: GameBoard) -> list[GameBoard]:
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

    def solve_by_astar_algorithm(self, start_node: GameBoard):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected

        open_list: list[GameBoard] = list([start_node])
        closed_list: list[GameBoard] = list()

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g: dict[str, int] = {}
        g[start_node.to_str()] = 0

        # parents contains an adjacency map of all nodes
        parents: dict[str, GameBoard] = {}
        parents[start_node.to_str()] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v.to_str()] + self.h(v) < g[n.to_str()] + self.h(v):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n.is_complete():
                reconst_path: list[str] = []

                while parents[n.to_str()] != n:
                    reconst_path.append(str(n.transit))
                    n = parents[n]

                reconst_path.append(str(start_node.transit))
                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for m in self.get_neighbors(n):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.append(m)
                    parents[m.to_str()] = n
                    g[m.to_str()] = g[n.to_str()] + 1

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m.to_str()] > g[n.to_str()] + 1:
                        g[m] = g[n] + 1
                        parents[m.to_str()] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.append(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.append(n)

        print('Solution does not exist!')
        return None


board = GameBoard([
    [1, 2, 3, 1],
    [2, 2, 3, 1],
    [3, 1, 2, 3],
    # [1,1,1,1],
    # [2,2,2,2],
    # [3,3,3,3],
    [], []
], 3)
print(board.get_num_blocks())
print(board.to_str())
print(board.is_complete())
