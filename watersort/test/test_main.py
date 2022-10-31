import unittest

from watersort.board import Board
from watersort.glass import Glass
from watersort.algorithm.blindsearch.solver import solver

class TestMain(unittest.TestCase):

    @staticmethod
    def solve(board):
        result = solver(board)
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
        self.solve(board)