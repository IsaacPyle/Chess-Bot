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

    def check_move(self, move):
        if (move.moved_piece[0] == "w" and not self.whites_turn) or (move.moved_piece[0] == "b" and self.whites_turn):
            return False
        
        piece = move.moved_piece
        if piece == "wP":
            if piece in [x.moved_piece for x in self.move_log]:
                if (move.start_row == move.end_row + 1 or move.start_row == move.end_row + 2) and move.start_col == move.end_col:
                    return True
                else:
                    return False
            else:
                if move.start_row == move.end_row + 1 and move.start_col == move.end_col:
                    return True
                else:
                    return False

        if piece == "bP":
            if move.start_row == move.end_row - 1 and move.start_col == move.end_col:
                return True
            else:
                return False

        return True
        


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

    def get_chess_notation(self, row, col):
        letters = "hgfedcba"
        return letters[7-col] + str(8-row)

    

