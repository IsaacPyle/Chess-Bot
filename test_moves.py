import pytest

import board
from board import Move


class TestClass():
    @pytest.fixture(autouse=True)
    def beforeEach(self):
        self.bd = board.Board()

    def test_init_valid_moves(self):
        moves = self.bd.get_valid_moves()
        assert len(moves) == 20

    def test_make_move(self):
        assert self.bd.whites_turn == True
        self.bd.make_move(Move(self.bd.board_state, (6, 0), (4, 0), True))
        assert self.bd.board_state[4][0] == "wP"
        assert self.bd.enpassant == (5, 0)
        assert self.bd.whites_turn == False

    def test_check(self):
        self.bd = board.Board()
        self.bd.board_state[6][3] = "--"
        self.bd.board_state[3][0] = "bB"
        for row in self.bd.board_state:
            print(row)
        assert self.bd.check() == True