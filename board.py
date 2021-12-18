import math
import pieces

class Board:
    def __init__(self):
        self.board_letters = "hgfedcba"
        self.board_squares = [[x + str(y) for y in range(1, 9)] for x in self.board_letters]
        self.initial_state = setup()
        self.board_state = self.initial_state

def setup():
        start_pieces = {"a1": pieces.Rook("a1", "white"), "b1": pieces.Knight("b1", "white"), 
            "c1": pieces.Bishop("c1", "white"), "d1": pieces.Queen("d1", "white"), 
            "e1": pieces.King("e1", "white"), "f1": pieces.Bishop("f1", "white"), 
            "g1": pieces.Knight("g1", "white"), "h1": pieces.Rook("h1", "white"),
            "a2": pieces.Pawn("a2", "white"), "b2": pieces.Pawn("b2", "white"), 
            "c2": pieces.Pawn("c2", "white"), "d2": pieces.Pawn("d2", "white"),
            "e2": pieces.Pawn("e2", "white"), "f2": pieces.Pawn("f2", "white"), 
            "g2": pieces.Pawn("g2", "white"), "h2": pieces.Pawn("h2", "white"),
            "a8": pieces.Rook("a8", "black"), "b8": pieces.Knight("b8", "black"), 
            "c8": pieces.Bishop("c8", "black"), "d8": pieces.Queen("d8", "black"), 
            "e8": pieces.King("e8", "black"), "f8": pieces.Bishop("f8", "black"), 
            "g8": pieces.Knight("g8", "black"), "h8": pieces.Rook("h8", "black"),
            "a7": pieces.Pawn("a7", "black"), "b7": pieces.Pawn("b7", "black"), 
            "c7": pieces.Pawn("c7", "black"), "d7": pieces.Pawn("d7", "black"),
            "e7": pieces.Pawn("e7", "black"), "f7": pieces.Pawn("f7", "black"), 
            "g7": pieces.Pawn("g7", "black"), "h7": pieces.Pawn("h7", "black")}

        return start_pieces

board = Board()

print(board.initial_state["h8"].name)