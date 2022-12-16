import unittest

from vietnamesechess import game
from vietnamesechess.game import Move


class TestStringMethods(unittest.TestCase):

    def test_convert_board_1(self):
        board = [
            [0, 0,  0, 0, 0],
            [0, 1, -1, 1, 0],
            [1, 1,  0, 1, 0],
            [0, 1,  0, 1, 0],
            [0, 0,  0, 0, 0]
        ]
        move = Move(1, 2, 2, 2)
        new_board = game.convert_board(board, move, -1)
        expected_board = [
            [0,  0,  0,  0, 0],
            [0, -1,  0, -1, 0],
            [1, -1, -1, -1, 0],
            [0, -1,  0, -1, 0],
            [0,  0,  0,  0, 0]
        ]
        self.assertEqual(new_board, expected_board)
if __name__ == '__main__':
    unittest.main()