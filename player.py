from pieces import *
import pieces

class Player:
    def __init__(self):
        self.opponent_pieces = []

    def get_piece(self, this_piece) -> Piece:
        for piece in pieces:
            if piece.name == this_piece:
                return piece

    # def move(self, piece, initial_pos, end_pos):

    #     if (initial_pos[0] - end_pos[0], initial_pos[1] - end_pos[1]) in piece.moves and end_pos in board.Board.board_squares:

        