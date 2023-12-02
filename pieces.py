from board import Move, Board
from dataclasses import dataclass

@dataclass
class Piece:
    def __init__(self) -> None:
        pass

    def move():
        return

@dataclass
class Pawn(Piece):
    name: str
    color: str
    current_pos: tuple
    moves = [(0, 1), (0, 2)]
    attacks = [(1, 1), (-1, 1)]

@dataclass
class Rook(Piece):
    name: str
    color: str
    current_pos: str
    moves = ["h", "v"]
    attacks = ["h", "v"]

@dataclass
class Knight(Piece):
    name: str
    color: str
    current_pos: str
    moves = [(-2, 1), (-2,-1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
    attacks = [(-2, 1), (-2,-1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]

@dataclass
class Bishop(Piece):
    name: str
    color: str
    current_pos: str
    moves = ["d"]
    attacks = ["d"]

@dataclass
class Queen(Piece):
    name: str
    color: str
    current_pos: str
    moves = ["h", "d", "v"]
    attacks = ["h", "d", "v"]

@dataclass
class King(Piece):
    name: str
    color: str
    current_pos: str
    moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    attacks = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]



