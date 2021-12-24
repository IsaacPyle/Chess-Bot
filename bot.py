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

        random_move_index = random.randint(0, len(moves) - 1)
        board.make_move(moves[random_move_index])
        return board.get_valid_moves()

        