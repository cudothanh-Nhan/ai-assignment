import math
from enum import Enum


class Move(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class BlockState:

    def __init__(self, head, tail, bridges):
        self.head = head
        self.tail = tail
        self.bridges = bridges

    def __hash__(self):
        return hash('{}-{}'.format(self.head, self.tail))

    def __eq__(self, other):
        return isinstance(other, BlockState) and \
               self.head == other.head and \
               self.tail == other.tail
    def __repr__(self):
        return 'Head = {}. Tail = {}'.format(self.head, self.tail)
    def is_vertical(self):
        return self.head[0] == self.tail[0] and self.head[1] == self.tail[1]

    def euclidean_dist(self, hole):
        head_diff_0 = self.head[0] - hole[0]
        head_diff_1 = self.head[1] - hole[1]
        head_dist = math.sqrt(head_diff_0 *head_diff_0 + head_diff_1 * head_diff_1)

        tail_diff_0 = self.tail[0] - hole[0]
        tail_diff_1 = self.tail[1] -hole[1]
        tail_dist = math.sqrt(tail_diff_0 * tail_diff_0 + tail_diff_1 * tail_diff_1)

        return min(head_dist, tail_dist)

