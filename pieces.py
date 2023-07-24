from board import Move, Board

class Piece:
    def __init__(self) -> None:
        pass

    def move():
        return

class Pawn(Piece):
    def __init__(self, name, pos, color):
        self.name = name
        self.color = color
        self.current_pos = pos
        self.moves = [(0, 1), (0, 2)]
        self.attacks = [(1, 1), (-1, 1)]

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

class Rook:
    def __init__(self, name, pos, color):
        self.name = name
        self.color = color
        self.current_pos = pos
        self.moves = ["h", "v"]
        self.attacks = ["h", "v"]

class Knight:
    def __init__(self, name, pos, color):
        self.name = name
        self.color = color
        self.current_pos = pos
        self.moves = [(-2, 1), (-2,-1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        self.attacks = [(-2, 1), (-2,-1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]

class Bishop:
    def __init__(self, name, pos, color):
        self.name = name
        self.color = color
        self.current_pos = pos
        self.moves = ["d"]
        self.attacks = ["d"]

class Queen:
    def __init__(self, name, pos, color):
        self.name = name
        self.color = color
        self.current_pos = pos
        self.moves = ["h", "d", "v"]
        self.attacks = ["h", "d", "v"]

class King:
    def __init__(self, name, pos, color):
        self.name = name
        self.color = color
        self.current_pos = pos
        self.moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.attacks = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]



