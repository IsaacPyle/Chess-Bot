import random

class Bot():
    def __init__(self):
        # Ideas here
        # self.layer # <-- current layer in tree for minmax / alpha-beta pruning
        # self.best_move # <-- best move found so far, type Move()
        self.piece_values = {'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9} # <-- will be used for evaluation of capturing pieces
        # self.pawn_structure_score # <-- rates the value of changing a pawn structure, to promote pawns defending each other
        pass

    def make_move(self, moves, board):
        # for move in moves:
        #     if board[move.end_row][move.end_col] != "--":
        if len(moves) < 1:
            return False
        random_move_index = random.randint(0, len(moves) - 1)
        random_move = moves[random_move_index]
        preferred_move = (0, random_move)
        for move in moves:
            if move.captured_piece[1] in self.piece_values and self.piece_values[move.captured_piece[1]] > preferred_move[0]:
                preferred_move = (self.piece_values[move.captured_piece[1]], move)


        # random_move_index = random.randint(0, len(moves) - 1)
        board.make_move(moves[moves.index(preferred_move[1])])
        return board.get_valid_moves()

        