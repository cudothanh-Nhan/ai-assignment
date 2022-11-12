from watersort.algorithm.blindsearch.BFS import BFS
import timeit
from watersort.board import Board

class GraphNode:
    def __init__(self, board: Board, prev_node, prev_move):
        self.board = board
        self.prev_node = prev_node
        self.prev_move = prev_move
    
    def get_board(self):
        return self.board
    
    def get_neighbors(self):
        neighbors = list()
        for move in self.board.calc_all_potential_moves():
            if self.board.is_glass_complete(move._from):
                continue
            new_board = self.board.clone()
            new_board.move_ball(move)
            neighbors.append(GraphNode(new_board, self, move))
        return neighbors
    
    def get_hash(self):
        glasses = self.board.get_glasses_list()
        return ";".join([glasses[i].to_string(i) for i in range(len(glasses))])
    
    def get_moves_to_node(self):
        moves = list()
        if self.prev_node is not None:
            moves.extend(self.prev_node.get_moves_to_node())
        if self.prev_move is not None:
            moves.append(self.prev_move)
        return moves

def BFSsolver(board):
    start_time = timeit.default_timer()
    startNode = GraphNode(board, None, None)
    traversal = BFS(startNode)
    iterate_num = 0
    while not traversal.is_done():
        iterate_num += 1
        currentNode = traversal.cur_node()
        isSolved = currentNode.get_board().is_complete()
        if isSolved:
            end_time = timeit.default_timer()
            elapsed_time = end_time - start_time
            return {
                "isSolved": True,
                "moves": currentNode.get_moves_to_node(),
                "time": elapsed_time,
                "iterate": iterate_num
            }
        traversal.iterate()
    return {
        "isSolved": False,
        "moves": [],
        "time": 0,
        "iterate": iterate_num
    }
