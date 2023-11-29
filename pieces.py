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

    def get_moves(self, moves):
        row = self.current_pos[0]
        col = self.current_pos[1]

        if self.whites_turn:
            if Board.board_state[row-1][col] == "--":
                moves.append(Move(Board.board_state, (row, col), (row-1, col)))
                if row == 6 and Board.board_state[row-2][col] == "--":
                    moves.append(Move(Board.board_state, (row, col), (row-2, col)))
            if col > 0:
                if Board.board_state[row-1][col-1][0] == "b":
                    moves.append(Move(Board.board_state, (row, col), (row-1, col-1)))
                elif (row-1, col-1) == Board.enpassant:
                    moves.append(Move(Board.board_state, (row, col), (row-1, col-1), True))
            if col < 7:
                if Board.board_state[row-1][col+1][0] == "b":
                    moves.append(Move(Board.board_state, (row, col), (row-1, col+1)))
                elif (row-1, col+1) == self.enpassant:
                    moves.append(Move(Board.board_state, (row, col), (row-1, col+1), True))
        else:
            if Board.board_state[row+1][col] == "--":
                moves.append(Move(Board.board_state, (row, col), (row+1, col)))
                if row == 1 and Board.board_state[row+2][col] == "--":
                    moves.append(Move(Board.board_state, (row, col), (row+2, col)))
            if col > 0:
                if Board.board_state[row+1][col-1][0] == "w":
                    moves.append(Move(Board.board_state, (row, col), (row+1, col-1)))
                elif (row+1, col-1) == self.enpassant:
                    moves.append(Move(Board.board_state, (row, col), (row+1, col-1), True))
            if col < 7:
                if Board.board_state[row+1][col+1][0] == "w":
                    moves.append(Move(Board.board_state, (row, col), (row+1, col+1)))
                elif (row+1, col+1) == self.enpassant:
                    moves.append(Move(Board.board_state, (row, col), (row+1, col+1), True))

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



