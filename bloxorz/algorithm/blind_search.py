from __future__ import annotations
from copy import deepcopy
from time import time
from bloxorz.algorithm.algorithm import Algorithm
from bloxorz.algorithm.traversal.dfs import DFS
from bloxorz.algorithm.traversal.traversal import TraversableNode
from bloxorz.gameround import GameRound


class GameState:
    GAME_ROUND = None

    @staticmethod
    def SET_GAME_ROUND(round_number):
        GameState.GAME_ROUND = GameRound(round_number)

    def __init__(self):
        if type(GameState.GAME_ROUND) is not GameRound:
            raise "error: SET_GAME_ROUND first"
        self.block_state = GameState.GAME_ROUND.get_start_state()

    def get_next_valid_moves(self):
        return GameState.GAME_ROUND.get_next_valid_moves(self.block_state)

    def clone(self):
        return deepcopy(self)

    def apply_move(self, move):
        new_state = GameState.GAME_ROUND.calc_new_state(self.block_state, move)
        self.block_state = new_state

    def is_finish(self):
        return GameState.GAME_ROUND.is_reach_goal(self.block_state)

    def get_hash(self):
        return hash(self.block_state)


class GraphNode(TraversableNode):
    def __init__(self, game_state: GameState, prev_move, prev_node: GraphNode):
        self.prev_node = prev_node
        self.game_state = game_state
        self.prev_move = prev_move

    def get_neighbors(self):
        n = list()
        for move in self.game_state.get_next_valid_moves():
            new_state = self.game_state.clone()
            new_state.apply_move(move)
            n.append(GraphNode(new_state, move, self))
        return n

    def get_hash(self):
        return self.game_state.get_hash()

    def get_moves_to_node(self):
        moves = []
        if self.prev_node is not None:
            moves.extend(self.prev_node.get_moves_to_node())
        if self.prev_move is not None:
            moves.append(self.prev_move)
        return moves


class BlindSearchAlgorithm(Algorithm):
    def __init__(self, game_round, timeout_secs):
        GameState.SET_GAME_ROUND(game_round)
        self._timeout = timeout_secs
        self._is_found = False
        self._moves = None

    def found_solution(self):
        return self._is_found

    def get_solution(self):
        return self._moves

    def run(self):
        ntrial = 0
        startNode = GraphNode(GameState(), None, None)
        traversal = DFS(startNode)
        t0 = time()
        while not traversal.is_done() and (time() - t0) < self._timeout:
            current_node = traversal.cur_node()
            is_solved = current_node.game_state.is_finish()
            if is_solved:
                self._is_found = True
                self._moves = current_node.get_moves_to_node()
                print("ntrial: ", ntrial)
                return
            traversal.iterate()
            ntrial += 1
