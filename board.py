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
        if (self.whites_turn and self.board_state[row][col][0] == "b") or (not self.whites_turn and self.board_state[row][col][0] == "w"):
            return
        piece_dir = [(1,0), (0,1), (-1,0), (0,-1)]
        enemy_color = "b" if self.whites_turn else "w"
        for dir in piece_dir:
            for i in range(1, 8):
                end_row = row + dir[0] * i
                end_col = col + dir[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if self.board_state[end_row][end_col] == "--": 
                        moves.append(Move(self.board_state, (row, col), (end_row, end_col)))
                    elif self.board_state[end_row][end_col][0] == enemy_color:
                        moves.append(Move(self.board_state, (row, col), (end_row, end_col)))
                        break
                    else:
                        break
                else:
                    break

    def knight_moves(self, row, col, moves):
        if (self.whites_turn and self.board_state[row][col][0] == "b") or (not self.whites_turn and self.board_state[row][col][0] == "w"):
            return
        enemy_color = "b" if self.whites_turn else "w"
        piece_moves = [(-2, 1), (-2,-1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        for move in piece_moves:
            new_row = row + move[0]
            new_col = col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board_state[new_row][new_col][0] == "-" or self.board_state[new_row][new_col][0] == enemy_color:
                    moves.append(Move(self.board_state, (row, col), (new_row, new_col)))



    def bishop_moves(self, row, col, moves):
        if (self.whites_turn and self.board_state[row][col][0] == "b") or (not self.whites_turn and self.board_state[row][col][0] == "w"):
            return
        piece_dir = [(1,1), (-1,1), (-1,-1), (1,-1)]
        enemy_color = "b" if self.whites_turn else "w"
        for dir in piece_dir:
            for i in range(1, 8):
                end_row = row + dir[0] * i
                end_col = col + dir[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if self.board_state[end_row][end_col] == "--": 
                        moves.append(Move(self.board_state, (row, col), (end_row, end_col)))
                    elif self.board_state[end_row][end_col][0] == enemy_color:
                        moves.append(Move(self.board_state, (row, col), (end_row, end_col)))
                        break
                    else:
                        break
                else:
                    break

    def queen_moves(self, row, col, moves):
        self.bishop_moves(row, col, moves)
        self.rook_moves(row, col, moves)

    def king_moves(self, row, col, moves):
        if (self.whites_turn and self.board_state[row][col][0] == "b") or (not self.whites_turn and self.board_state[row][col][0] == "w"):
            return
        enemy_color = "b" if self.whites_turn else "w"
        piece_moves = [(-1, 1), (-1,-1), (1, 1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for move in piece_moves:
            new_row = row + move[0]
            new_col = col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board_state[new_row][new_col][0] == "-" or self.board_state[new_row][new_col][0] == enemy_color:
                    moves.append(Move(self.board_state, (row, col), (new_row, new_col)))


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

    

