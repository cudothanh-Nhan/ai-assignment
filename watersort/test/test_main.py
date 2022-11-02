import unittest

from watersort.board import Board
from watersort.glass import Glass
from watersort.algorithm.blindsearch.solver import BFSsolver

class TestMain(unittest.TestCase):

    @staticmethod
    def print(board):
        result = BFSsolver(board)
        if result["isSolved"]:
            print("solved")
            moves = result["moves"]
            for move in moves:
                print("move from " +str(move._from) + " to " + str(move._to))
            return True
        return False
    
    def test_can_create_multiple_glass(self):
        board = Board([
            Glass.create_glass([1,2,1,2]),
            Glass.create_glass([2,1,2,1]),
            Glass.create_glass([ ])
        ])
        self.print(board)