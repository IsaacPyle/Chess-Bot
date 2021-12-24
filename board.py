
class Board():
    '''
    Stores all information regarding current and starting board state, and handles generating possible moves for each piece. 
    Keeps a log of moves made to be able to undo moves using the "u" key.
    '''
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
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)
        self.enpassant = ()

    def get_valid_moves(self):
        '''
        Gets all possible moves and removes moves that leave or put the king in check. 
        Requires making all possible moves by the current player, then checking all possible moves from the opponent,
        to see if the king could be captured. Naive algorithm, and can be improved.
        '''
        temp_enpassant = self.enpassant
        valid_moves = self.get_all_moves()
        for i in range(len(valid_moves) - 1, -1, -1):
            self.make_move(valid_moves[i])
            self.whites_turn = not self.whites_turn
            if self.check():
                valid_moves.remove(valid_moves[i])
            self.whites_turn = not self.whites_turn
            self.undo_move()
        
        self.enpassant = temp_enpassant
        print(self.enpassant)

        return valid_moves

    def get_all_moves(self):
        '''
        Gets all moves possible for the current board state.
        '''
        moves = []
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state[row])):
                piece = self.board_state[row][col][1]
                if piece != "-":
                    self.move_functions[piece](row, col, moves)

        return moves

    def check(self):
        '''
        Checks if the current player's king is being attacked by any enemy piece, using the "piece_attacked" method 
        '''
        if self.whites_turn:
            return self.piece_attacked(self.white_king_loc[0], self.white_king_loc[1])
        else:
            return self.piece_attacked(self.black_king_loc[0], self.black_king_loc[1])

    def piece_attacked(self, row, col):
        '''
        Checks is a particular piece is being attacked. Makes all moves by opponent, and sees
        if any of them can capture the piece.
        '''
        self.whites_turn = not self.whites_turn
        opponent_moves = self.get_all_moves()
        self.whites_turn = not self.whites_turn
        for move in opponent_moves:
            if move.end_col == col and move.end_row == row:
                return True
        return False

    def pawn_moves(self, row, col, moves):
        '''
        Gets all possible moves for the pawn at (row, col) in the board_state, including captures and regular movement.
        Does not handle en passant or pawn promotion.
        '''
        if self.whites_turn:
            if self.board_state[row][col] == "wP":
                if self.board_state[row-1][col] == "--":
                    moves.append(Move(self.board_state, (row, col), (row-1, col)))
                    if row == 6 and self.board_state[row-2][col] == "--":
                        moves.append(Move(self.board_state, (row, col), (row-2, col)))
                if col > 0:
                    if self.board_state[row-1][col-1][0] == "b":
                        moves.append(Move(self.board_state, (row, col), (row-1, col-1)))
                    elif (row-1, col-1) == self.enpassant:
                        moves.append(Move(self.board_state, (row, col), (row-1, col-1), enpassant=True))
                if col < 7:
                    if self.board_state[row-1][col+1][0] == "b":
                        moves.append(Move(self.board_state, (row, col), (row-1, col+1)))
                    elif (row-1, col+1) == self.enpassant:
                        moves.append(Move(self.board_state, (row, col), (row-1, col+1), enpassant=True))
        else:
            if self.board_state[row][col] == "bP":
                if self.board_state[row+1][col] == "--":
                    moves.append(Move(self.board_state, (row, col), (row+1, col)))
                    if row == 1 and self.board_state[row+2][col] == "--":
                        moves.append(Move(self.board_state, (row, col), (row+2, col)))
                if col > 0:
                    if self.board_state[row+1][col-1][0] == "w":
                        moves.append(Move(self.board_state, (row, col), (row+1, col-1)))
                    elif (row+1, col-1) == self.enpassant:
                        moves.append(Move(self.board_state, (row, col), (row+1, col-1), enpassant=True))
                if col < 7:
                    if self.board_state[row+1][col+1][0] == "w":
                        moves.append(Move(self.board_state, (row, col), (row+1, col+1)))
                    elif (row+1, col+1) == self.enpassant:
                        moves.append(Move(self.board_state, (row, col), (row+1, col+1), enpassant=True))

    def rook_moves(self, row, col, moves):
        '''
        Gets all possible moves for the rook at (row, col) in the board_state, including captures and regular movement.
        '''
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
        '''
        Gets all possible moves for the knight at (row, col) in the board_state, including captures and regular movement.
        '''
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
        '''
        Gets all possible moves for the bishop at (row, col) in the board_state, including captures and regular movement.
        '''
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
        '''
        Gets all possible moves for the queen at (row, col) in the board_state, including captures and regular movement.
        Because the queen acts as a bishop and a rook combined, their logic is used to generate possible moves for the queen.
        '''
        self.bishop_moves(row, col, moves)
        self.rook_moves(row, col, moves)


    def king_moves(self, row, col, moves):
        '''
        Gets all possible moves for the king at (row, col) in the board_state, including captures and regular movement.
        '''
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
        '''
        Takes a move, updates the board_state and king location variables, inverts whites_turn variable, 
        and appends the move to move_log.
        '''
        if self.board_state[move.start_row][move.start_col] == "wK":
            self.white_king_loc = (move.end_row, move.end_col)
        elif self.board_state[move.start_row][move.start_col] == "bK":
            self.black_king_loc = (move.end_row, move.end_col)
        self.board_state[move.start_row][move.start_col] = "--"

        if move.pawn_promotion:
            self.board_state[move.end_row][move.end_col] = move.moved_piece[0] + "Q"
        else:
            self.board_state[move.end_row][move.end_col] = move.moved_piece
        
        if move.enpassant_move:
            print("Captured {}".format((move.start_row, move.end_col)))
            self.board_state[move.start_row][move.end_col] = "--"

        if move.moved_piece[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.enpassant = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.enpassant = ()

        self.whites_turn = not self.whites_turn
        self.move_log.append(move)
        

    def undo_move(self):
        '''
        Takes the most recent move from the move_log, pops it and does the opposite. 
        Also reverts whites turn and updates king location variables if necessary
        '''
        if len(self.move_log) > 0:
            prev_move = self.move_log.pop()
            if self.board_state[prev_move.end_row][prev_move.end_col] == "wK":
                self.white_king_loc = (prev_move.start_row, prev_move.start_col)
            elif self.board_state[prev_move.end_row][prev_move.end_col] == "bK":
                self.black_king_loc = (prev_move.start_row, prev_move.start_col)
            self.board_state[prev_move.end_row][prev_move.end_col] = prev_move.captured_piece
            self.board_state[prev_move.start_row][prev_move.start_col] = prev_move.moved_piece
            self.whites_turn = not self.whites_turn

            if prev_move.enpassant_move:
                self.board_state[prev_move.end_row][prev_move.end_col] = "--"
                self.board_state[prev_move.start_row][prev_move.end_col] = prev_move.captured_piece
                self.enpassant = (prev_move.end_row, prev_move.end_col)

            if prev_move.moved_piece[1] == 'P' and abs(prev_move.start_row - prev_move.end_row) == 2:
                self.enpassant = ()



class Move():
    '''
    Initializes with the current board state, a starting location, and an ending location. 
    Saves the piece that was moved and the piece that was captured ('--' if ending location was empty).

    '''
    def __init__(self, board, start, end, enpassant=False):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.pawn_promotion = False
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece = board[self.end_row][self.end_col]
        if (self.moved_piece == "wP" and self.end_row == 0) or (self.moved_piece == "bP" and self.end_row == 7):
            self.pawn_promotion = True

        self.enpassant_move = enpassant
        if self.enpassant_move:
            self.captured_piece = 'wP' if self.moved_piece == 'bP' else 'bP'

    def check_eq(self, other_move):
        '''
        Confirms that moves are the same, which is needed since we create moves to check against that 
        are different in memory but the same on the board.
        '''
        first = self.start_col * 1000 + self.start_row * 100 + self.end_row * 10 + self.end_col
        second = other_move.start_col * 1000 + other_move.start_row * 100 + other_move.end_row * 10 + other_move.end_col
        return first == second

    def get_chess_notation(self, row, col):
        '''
        Converts (row, col) to chess notation which is 'File-Rank', so moving from the 
        first row first column to the third row first column would be 'a1' to 'a3'.
        '''
        letters = "hgfedcba"
        return letters[7-col] + str(8-row)

    

