class Board():
    def __init__(self):
        self.whites_turn = True
        self.move_log = []
        self.initial_state = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.board_state = self.initial_state
        self.move_functions = {"P": self.pawn_moves, "R": self.rook_moves, "B": self.bishop_moves, "N": self.knight_moves, "Q": self.queen_moves, "K": self.king_moves}

    def get_valid_moves(self):
        moves = []
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state[row])):
                piece = self.board_state[row][col][1]
                if piece != "-":
                    self.move_functions[piece](row, col, moves)

        return moves

    def pawn_moves(self, row, col, moves):
        if self.whites_turn:
            if self.board_state[row][col] == "wP":
                if self.board_state[row-1][col] == "--":
                    moves.append(Move(self.board_state, (row, col), (row-1, col)))
                    if row == 6 and self.board_state[row-2][col] == "--":
                        moves.append(Move(self.board_state, (row, col), (row-2, col)))
                if col > 0:
                    if self.board_state[row-1][col-1][0] == "b":
                        moves.append(Move(self.board_state, (row, col), (row-1, col-1)))
                if col < 7:
                    if self.board_state[row-1][col+1][0] == "b":
                        moves.append(Move(self.board_state, (row, col), (row-1, col+1)))
        elif not self.whites_turn:
            if self.board_state[row][col] == "bP":
                if self.board_state[row+1][col] == "--":
                    moves.append(Move(self.board_state, (row, col), (row+1, col)))
                    if row == 1 and self.board_state[row+2][col] == "--":
                        moves.append(Move(self.board_state, (row, col), (row+2, col)))
                if col > 0:
                    if self.board_state[row+1][col-1][0] == "w":
                        moves.append(Move(self.board_state, (row, col), (row+1, col-1)))
                if col < 7:
                    if self.board_state[row+1][col+1][0] == "w":
                        moves.append(Move(self.board_state, (row, col), (row+1, col+1)))

    def rook_moves(self, row, col, moves):
        pass

    def knight_moves(self, row, col, moves):
        pass

    def bishop_moves(self, row, col, moves):
        pass

    def queen_moves(self, row, col, moves):
        pass

    def king_moves(self, row, col, moves):
        pass


    def make_move(self, move):
        self.board_state[move.start_row][move.start_col] = "--"
        self.board_state[move.end_row][move.end_col] = move.moved_piece
        self.whites_turn = not self.whites_turn
        self.move_log.append(move)
        print(move.get_chess_notation(move.start_row, move.start_col) + move.get_chess_notation(move.end_row, move.end_col))

    def undo_move(self):
        if len(self.move_log) > 0:
            prev_move = self.move_log.pop()
            self.board_state[prev_move.end_row][prev_move.end_col] = prev_move.captured_piece
            self.board_state[prev_move.start_row][prev_move.start_col] = prev_move.moved_piece
            self.whites_turn = not self.whites_turn


class Move():
    def __init__(self, board, start, end):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece = board[self.end_row][self.end_col]

    def check_eq(self, other_move):
        first = self.start_col * 1000 + self.start_row * 100 + self.end_row * 10 + self.end_col
        second = other_move.start_col * 1000 + other_move.start_row * 100 + other_move.end_row * 10 + other_move.end_col
        return first == second

    def get_chess_notation(self, row, col):
        letters = "hgfedcba"
        return letters[7-col] + str(8-row)

    

