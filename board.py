import math
import pieces

class Board:
    def __init__(self):
        self.board.size = [["[]" for x in range(8)] for i in range(8)]
        self.initial_state = {"a1": pieces.Rook("a1", "black")}
        self.board_state
