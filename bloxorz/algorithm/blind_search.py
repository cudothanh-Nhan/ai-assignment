from __future__ import annotations
import time
import psutil
from bloxorz.algorithm.algorithm import Algorithm
from bloxorz.algorithm.traversal.dfs import DFS
from bloxorz.algorithm.traversal.traversal import TraversableNode
from bloxorz.gameround import GameRound


class GameState:
    def __init__(self, game_round: GameRound):
        self.GAME_ROUND = game_round
        self.block_state = self.GAME_ROUND.get_start_state()

    def get_next_valid_moves(self):
        return self.GAME_ROUND.get_next_valid_moves(self.block_state)

    def clone_and_apply_move(self, move):
        block_state = self.GAME_ROUND.calc_new_state(self.block_state, move)
        res = GameState(self.GAME_ROUND)
        res.block_state = block_state
        return res

    def is_finish(self):
        return self.GAME_ROUND.is_reach_goal(self.block_state)

    def get_hash(self):
        block = self.block_state
        return hash('{}-{}:{}'.format(block.head, block.tail, len(block.bridges)))


class GraphNode(TraversableNode):
    def __init__(self, game_state: GameState, prev_move, prev_node: GraphNode):
        self.prev_node = prev_node
        self.game_state = game_state
        self.prev_move = prev_move

    @staticmethod
    def get_start_node(game_round: GameRound):
        return GraphNode(GameState(game_round), None, None)

    @classmethod
    def parse(cls, o):
        assert type(o) is GraphNode
        return cls(o.game_state, o.prev_move, o.prev_node)

    def get_neighbors(self):
        n = list()
        for move in self.game_state.get_next_valid_moves():
            new_state = self.game_state.clone_and_apply_move(move)
            n.append(GraphNode(new_state, move, self))
        return n

    def get_hash(self):
        return self.game_state.get_hash()

    def is_finish_node(self):
        return self.game_state.is_finish()

    def get_moves_to_node(self):
        moves = []
        if self.prev_node is not None:
            moves.extend(self.prev_node.get_moves_to_node())
        if self.prev_move is not None:
            moves.append(self.prev_move)
        return moves


class BlindSearchAlgorithm(Algorithm):
    def __init__(self, game_round, timeout_secs):
        self._timeout = timeout_secs
        self._moves = None
        self._start_node = GraphNode.get_start_node(game_round)
        self._num_total_iterations = 0
        self.is_found = False

    def found_solution(self):
        return self.is_found

    def get_solution(self):
        return self._moves

    def run(self):
        self._num_total_iterations = 0
        traversal = DFS(self._start_node)
        start_time = time.time()
        before_run_mem = psutil.Process().memory_info().rss
        running_mem = psutil.Process().memory_info().rss
        while not traversal.is_done() and (time.time() - start_time) < self._timeout:
            self._num_total_iterations += 1
            current_node = GraphNode.parse(traversal.cur_node())
            is_solved = current_node.is_finish_node()
            running_mem = max(running_mem, psutil.Process().memory_info().rss)
            if is_solved:
                self.is_found = True
                self._moves = current_node.get_moves_to_node()
                break
            traversal.iterate()

        self.elapsed_time = time.time() - start_time
        self.max_mem_use = (running_mem - before_run_mem) / (1024.0)

    def __repr__(self):
        return 'DFS algorithm'
