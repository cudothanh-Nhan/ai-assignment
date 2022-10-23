from bloxorz.algorithm.traversal.traversal import TraversableNode, Traversal


class DFS(Traversal):
    def __init__(self, start_node: TraversableNode):
        self.visited = set()
        self.visited.add(start_node.get_hash())

        self.dfs_stack = []
        self.dfs_stack.append(start_node)

    def is_done(self):
        return len(self.dfs_stack) == 0

    def cur_node(self) -> TraversableNode:
        return self.dfs_stack[-1]

    def iterate(self):
        node = self.cur_node()
        self.dfs_stack = self.dfs_stack[:-1]
        for neighbor in node.get_neighbors():
            neighborHash = neighbor.get_hash()
            if neighborHash not in self.visited:
                self.dfs_stack.append(neighbor)
                self.visited.add(neighborHash)
