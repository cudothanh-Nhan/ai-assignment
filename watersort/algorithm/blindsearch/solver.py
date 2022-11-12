from watersort.algorithm.blindsearch.BFS import BFS

class GraphNode:
    def __init__(self, board, prev_node, prev_move):
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
        return ";".join([str(glass) for glass in glasses])
    
    def get_moves_to_node(self):
        moves = list()
        if self.prev_node is not None:
            moves.extend(self.prev_node.get_moves_to_node())
        if self.prev_move is not None:
            moves.append(self.prev_move)
        return moves

def BFSsolver(board):
    startNode = GraphNode(board, None, None)
    traversal = BFS(startNode)
    while not traversal.is_done():
        currentNode = traversal.cur_node()
        isSolved = currentNode.get_board().is_complete()
        if isSolved:
            return {
                "isSolved": True,
                "moves": currentNode.get_moves_to_node()
            }
        traversal.iterate()
    return {
        "isSolved": False,
        "moves": []
    }
