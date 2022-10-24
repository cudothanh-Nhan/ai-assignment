import os

import unittest

from ..board import Board

class TestMain(unittest.TestCase):

    @staticmethod
    def solve(board):
        result = solver(board)
        if result["isSolved"]:
            print("solved")
            moves = result["moves"]
            for move in moves:
                print(str(move._from) + " " + str(move._to))
            return True
        return False
    
    def test_can_create_multiple_glass(self):
        board = Board([
            Glass.create_glass([2, 1, 1, 1]),
            Glass.create_glass([2, 2, 2]),
            Glass.create_glass([1]),
            Glass.create_glass([])
        ])
        self.solve(board)