from dataclasses import dataclass
from typing import List

@dataclass
class Move():
    '''
    Initializes with the current board state, a starting location, and an ending location. 
    Saves the piece that was moved and the piece that was captured ('--' if ending location was empty).
    '''
    board: list
    start: tuple
    end: tuple
    enpassant_possible: bool = False
    castling: bool = False

    def __post_init__(self):
        self.start_row, self.start_col = self.start
        self.end_row, self.end_col = self.end
        self.moved_piece = self.board[self.start_row][self.start_col]
        self.captured_piece = self.board[self.end_row][self.end_col]
        self.pawn_promotion = (self.moved_piece == "wP" and self.end_row == 0) or (self.moved_piece == "bP" and self.end_row == 7)
        self.player_moved = True if self.captured_piece != "--" else False

        if self.enpassant_possible:
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
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return self.moved_piece < other.moved_piece

class Board:
    def __init__(self):
            self.whites_turn = True
            self.move_log: List[Move] = []
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
            self.move_functions = {"P": self.pawn_moves, "R": self.rook_moves,
                                            "B": self.bishop_moves, "N": self.knight_moves,
                                            "Q": self.queen_moves, "K": self.king_moves}
            self.white_king_loc = (7, 4)
            self.black_king_loc = (0, 4)
            self.castle_moves = Castles()
            self.castles_log = [Castles(self.castle_moves.wks, self.castle_moves.wqs,
                                                  self.castle_moves.bks, self.castle_moves.bqs)]
            self.enpassant = ()
            self.checkmate = False
            self.stalemate = False
            self.captured_white_pieces = []
            self.captured_black_pieces = []

    def __eq__(self, other: object) -> bool:
        state = self.board_state == other.board_state
        castles = self.castle_moves == other.castle_moves
        turn = self.whites_turn == other.whites_turn
        return state and castles and turn
    
    def __hash__(self) -> int:
        return id(self)

    def get_valid_moves(self, isRealMove=True) -> List[Move]:
        '''
        Gets all possible moves and removes moves that leave or put the king in check. 
        Requires making all possible moves by the current player, then checking all possible moves from the opponent,
        to see if the king could be captured. Naive algorithm, and can be improved.
        '''
        temp_enpassant = self.enpassant
        temp_castles = Castles(self.castle_moves.wks, self.castle_moves.wqs, self.castle_moves.bks, self.castle_moves.bqs)
        moves = self.get_all_moves()
        if self.whites_turn:
            self.get_castle_moves(self.white_king_loc[0], self.white_king_loc[1], moves)
        else:
            self.get_castle_moves(self.black_king_loc[0], self.black_king_loc[1], moves)

        for move in moves[::-1]:
            self.make_move(move)
            self.whites_turn = not self.whites_turn
            if self.check():
                moves.remove(move)
            self.whites_turn = not self.whites_turn
            self.undo_move()

        self.enpassant = temp_enpassant
        self.castle_moves = temp_castles

        if len(moves) == 0 and isRealMove:
            if self.check():
                self.checkmate = True
            else:
                self.stalemate = True

        return moves

    def get_all_moves(self) -> List[Move]:
        '''
        Gets all moves possible for the current board state.
        '''
        moves = []
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state[0])):
                current = self.board_state[row][col][0]
                if (current == 'w' and self.whites_turn) or (current == 'b' and not self.whites_turn):
                    piece = self.board_state[row][col][1]
                    if piece != "-":
                        self.move_functions[piece](row, col, moves)
        return moves

    def check(self) -> bool:
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
            if move.end_row == row and move.end_col == col:
                return True
        return False

    def pawn_moves(self, row, col, moves: List[Move]):
        '''
        Gets all possible moves for the pawn at (row, col) in the board_state, including captures and regular movement.
        Does not handle en passant or pawn promotion.
        '''
        if self.whites_turn:
            if self.board_state[row-1][col] == "--":
                moves.append(Move(self.board_state, (row, col), (row-1, col)))
                if row == 6 and self.board_state[row-2][col] == "--":
                    moves.append(Move(self.board_state, (row, col), (row-2, col)))
            if col > 0:
                if self.board_state[row-1][col-1][0] == "b":
                    moves.append(Move(self.board_state, (row, col), (row-1, col-1)))
                elif (row-1, col-1) == self.enpassant:
                    moves.append(Move(self.board_state, (row, col), (row-1, col-1), enpassant_possible=True))
            if col < 7:
                if self.board_state[row-1][col+1][0] == "b":
                    moves.append(Move(self.board_state, (row, col), (row-1, col+1)))
                elif (row-1, col+1) == self.enpassant:
                    moves.append(Move(self.board_state, (row, col), (row-1, col+1), enpassant_possible=True))
        else:
            if self.board_state[row+1][col] == "--":
                moves.append(Move(self.board_state, (row, col), (row+1, col)))
                if row == 1 and self.board_state[row+2][col] == "--":
                    moves.append(Move(self.board_state, (row, col), (row+2, col)))
            if col > 0:
                if self.board_state[row+1][col-1][0] == "w":
                    moves.append(Move(self.board_state, (row, col), (row+1, col-1)))
                elif (row+1, col-1) == self.enpassant:
                    moves.append(Move(self.board_state, (row, col), (row+1, col-1), enpassant_possible=True))
            if col < 7:
                if self.board_state[row+1][col+1][0] == "w":
                    moves.append(Move(self.board_state, (row, col), (row+1, col+1)))
                elif (row+1, col+1) == self.enpassant:
                    moves.append(Move(self.board_state, (row, col), (row+1, col+1), enpassant_possible=True))

    def rook_moves(self, row, col, moves: List[Move]):
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

    def knight_moves(self, row, col, moves: List[Move]):
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


    def bishop_moves(self, row, col, moves: List[Move]):
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

    def queen_moves(self, row, col, moves: List[Move]):
        '''
        Gets all possible moves for the queen at (row, col) in the board_state, including captures and regular movement.
        Because the queen acts as a bishop and a rook combined, their logic is used to generate possible moves for the queen.
        '''
        self.bishop_moves(row, col, moves)
        self.rook_moves(row, col, moves)


    def king_moves(self, row, col, moves: List[Move]):
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


    def get_castle_moves(self, row, col, moves: List[Move]):
        if self.check():
            return

        if self.whites_turn:
            if self.castle_moves.wks:
                if self.board_state[row][col+1] == "--" and self.board_state[row][col+2] == "--":
                    if not self.piece_attacked(row, col+1) and not self.piece_attacked(row, col+2):
                        moves.append(Move(self.board_state, (row, col), (row, col+2), castling=True))

            if self.castle_moves.wqs:
                if self.board_state[row][col-1] == "--" and self.board_state[row][col-2] == "--" and self.board_state[row][col-3] == "--":
                    if not self.piece_attacked(row, col-1) and not self.piece_attacked(row, col-2):
                        moves.append(Move(self.board_state, (row, col), (row, col-2), castling=True))

        elif not self.whites_turn:
            if self.castle_moves.bks:
                if self.board_state[row][col+1] == "--" and self.board_state[row][col+2] == "--":
                    if not self.piece_attacked(row, col+1) and not self.piece_attacked(row, col+2):
                        moves.append(Move(self.board_state, (row, col), (row, col+2), castling=True))

            if self.castle_moves.bqs:
                if self.board_state[row][col-1] == "--" and self.board_state[row][col-2] == "--" and self.board_state[row][col-3] == "--":
                    if not self.piece_attacked(row, col-1) and not self.piece_attacked(row, col-2):
                        moves.append(Move(self.board_state, (row, col), (row, col-2), castling=True))


    def make_move(self, move: Move):
        '''
        Takes a move, updates the board_state and king location variables, inverts whites_turn variable, 
        and appends the move to move_log.
        '''
        self.board_state[move.start_row][move.start_col] = "--"
        self.board_state[move.end_row][move.end_col] = move.moved_piece
        self.whites_turn = not self.whites_turn
        self.move_log.append(move)

        if move.moved_piece == "wK":
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.moved_piece == "bK":
            self.black_king_loc = (move.end_row, move.end_col)

        if move.pawn_promotion:
            self.board_state[move.end_row][move.end_col] = move.moved_piece[0] + "Q"
        
        if move.enpassant_possible:
            self.board_state[move.start_row][move.end_col] = "--"

        if move.moved_piece[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.enpassant = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.enpassant = ()

        if move.player_moved:
            if move.captured_piece[0] == "w":
                self.captured_white_pieces.append(move.captured_piece)

            elif move.captured_piece[0] == "b":
                self.captured_black_pieces.append(move.captured_piece)

        if move.castling:
            if move.end_col - move.start_col == 2:
                self.board_state[move.end_row][move.end_col-1] = self.board_state[move.end_row][move.end_col+1]
                self.board_state[move.end_row][move.end_col+1] = "--"

            else:
                self.board_state[move.end_row][move.end_col+1] = self.board_state[move.end_row][move.end_col-2]
                self.board_state[move.end_row][move.end_col-2] = "--"

        self.updateCastles(move)
        self.castles_log.append(Castles(self.castle_moves.wks, self.castle_moves.wqs, self.castle_moves.bks, self.castle_moves.bqs))


    def undo_move(self):
        '''
        Takes the most recent move from the move_log, pops it and does the opposite. 
        Also reverts whites turn and updates king location variables if necessary
        '''
        if len(self.move_log) > 0:
            prev_move = self.move_log.pop()
            self.board_state[prev_move.start_row][prev_move.start_col] = prev_move.moved_piece
            self.board_state[prev_move.end_row][prev_move.end_col] = prev_move.captured_piece
            self.whites_turn = not self.whites_turn

            if prev_move.moved_piece == "wK":
                self.white_king_loc = (prev_move.start_row, prev_move.start_col)
            elif prev_move.moved_piece == "bK":
                self.black_king_loc = (prev_move.start_row, prev_move.start_col)

            if prev_move.enpassant_possible:
                self.board_state[prev_move.end_row][prev_move.end_col] = "--"
                self.board_state[prev_move.start_row][prev_move.end_col] = prev_move.captured_piece
                self.enpassant = (prev_move.end_row, prev_move.end_col)

            if prev_move.moved_piece[1] == 'P' and abs(prev_move.start_row - prev_move.end_row) == 2:
                self.enpassant = ()

            if prev_move.player_moved:
                if prev_move.captured_piece[0] == "w":
                    self.captured_white_pieces.pop()

                elif prev_move.captured_piece[0] == "b":
                    self.captured_black_pieces.pop()

            self.castles_log.pop()
            current_castles = self.castles_log[-1]
            self.castle_moves = Castles(current_castles.wks, current_castles.wqs, current_castles.bks, current_castles.bqs)

            if prev_move.castling:
                if prev_move.end_col - prev_move.start_col == 2:
                    self.board_state[prev_move.end_row][prev_move.end_col + 1] = self.board_state[prev_move.end_row][prev_move.end_col - 1]
                    self.board_state[prev_move.end_row][prev_move.end_col - 1] = "--"
                else:
                    self.board_state[prev_move.end_row][prev_move.end_col - 2] = self.board_state[prev_move.end_row][prev_move.end_col + 1]
                    self.board_state[prev_move.end_row][prev_move.end_col + 1] = "--"

    def updateCastles(self, move: Move):
        if move.moved_piece == "wK":
            self.castle_moves.wks = False
            self.castle_moves.wqs = False
        elif move.moved_piece == "bK":
            self.castle_moves.bks = False
            self.castle_moves.bqs = False
        elif move.moved_piece == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.castle_moves.wqs = False
                elif move.start_col == 7:
                    self.castle_moves.wks = False
        elif move.moved_piece == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.castle_moves.bqs = False
                elif move.start_col == 7:
                    self.castle_moves.bks = False
        elif move.captured_piece[1] == "R":
            if move.end_row == 7:
                if move.end_col == 0:
                    self.castle_moves.wqs = False
                elif move.end_col == 7:
                    self.castle_moves.wks = False
            elif move.end_row == 0:
                if move.end_col == 0:
                    self.castle_moves.bqs = False
                elif move.end_col == 7:
                    self.castle_moves.bks = False


@dataclass
class Castles:
    wks: bool = True
    wqs: bool = True
    bks: bool = True
    bqs: bool = True

    

