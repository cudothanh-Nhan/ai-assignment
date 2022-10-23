from __future__ import annotations


class Traversal:

    def is_done(self):
        raise NotImplementedError("error: required method 'is_done'")

    def cur_node(self):
        raise NotImplementedError("error: required method 'cur_node'")

    def iterate(self):
        raise NotImplementedError("error: required method 'iterate'")


class TraversableNode:

    def get_hash(self):
        raise NotImplementedError("error: required method 'get_hash'")

    def get_neighbors(self):
        raise NotImplementedError("error: required method 'get_neighbors'")
