import unittest

import board
from board import Move

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.bd = board.Board()

    def test_init_valid_moves(self):
        moves = self.bd.get_valid_moves()
        self.assertEqual(len(moves), 20)

    def test_make_move(self):
        self.bd.make_move(Move(self.bd.board_state, (6, 0), (4, 0), True))
        self.assertEqual(self.bd.board_state[4][0], "wP")
        self.assertEqual(self.bd.enpassant, (5, 0))
        self.assertFalse(self.bd.whites_turn)

    def test_check(self):
        self.bd.board_state[6][3] = "--"
        self.bd.board_state[3][0] = "bB"
        self.assertTrue(self.bd.check())



if __name__ == "__main__":
    unittest.main()