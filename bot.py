import random
from typing import List
from board import Board, Castles, Move

class Bot():
    def __init__(self):
        # Ideas here
        self.piece_values = {'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 9, '-': 0} # <-- will be used for evaluation of capturing pieces
        self.enpassant = ()
        self.castles = ()
        self.checkmate = False
        self.stalemate = False

    def make_move(self, moves: List[Move], board: Board) -> List[Move]:
        if len(moves) < 1:
            return False
        
        # preferred_move = (0, self.getRandomMove(moves))
        values = self.getNextMoveValues(moves)
        bestAndValue = self.getBestMove(values, board)
        print(bestAndValue[1])
        if bestAndValue[1] == None:
            return
        print(bestAndValue[0], bestAndValue[1].captured_piece)
        best = bestAndValue[1]

        board.make_move(moves[moves.index(best)])
        # board.make_move(preferred_move[1])
        return board.get_valid_moves()
    
    # Find the best move, which is equal to the worst move for opponent after making this move.
    # Worst move for opponent is best for us, which is why we need the depth value
    def getBestMove(self, moves, board: Board, depth=2) -> List:
        # If no moves to make, return
        if not moves or moves == []:
            return [0, None]
        
        # If depth == 0, we don't want to recurse anymore. Return
        if depth == 0:
            best = max(moves, key = lambda x : x[0])[0]
            # Might be multiple moves with the same value, going to return a random move with that value
            bestMoves = [[i, j] for i, j in moves if i == best]
            return random.choice(bestMoves)
        
        # For each move available at this state
        options = []

        for move in moves:
            # We want to save the current state of the board, so it can be reset at the end
            self.saveBoard(board)
            # Actually make the move
            board.make_move(move[1])
            # Get all valid moves for the opponent, and their values (Based on capturing pieces only)
            validMoves = self.getNextMoveValues(board.get_valid_moves())
            # If no valid moves for the next plater, this is the best move. Return this with an essentially infinite value
            if len(validMoves) == 0:
                board.undo_move()
                self.resetBoardVars(board)
                return [1000000, move]

            # out of all of the valid moves, find one with the largest value for the opponent
            bestNextMove = max(validMoves, key = lambda x : x[0])
            bestNextVal = bestNextMove[0]

            bestNextVal += self.getBestMove(validMoves, board, depth - 1)[0]
            
            move = list(move)
            move[0] -= bestNextVal if depth % 2 == 0 else move[0] + bestNextVal
            options.append(move)

            board.undo_move()
            self.resetBoardVars(board)

        bestMoves = list(filter(lambda f: f == max(options, key = lambda x : x[0]), options))
        return random.choice(bestMoves)
    
    def saveBoard(self, board: Board):
        self.enpassant = board.enpassant
        self.castles = Castles(board.castle_moves.wks, board.castle_moves.wqs, board.castle_moves.bks, board.castle_moves.bqs)
        self.checkmate = board.checkmate
        self.stalemate = board.stalemate

    def resetBoardVars(self, board: Board):
        board.enpassant = self.enpassant
        board.castle_moves = self.castles
        board.checkmate = self.checkmate
        board.stalemate = self.stalemate

    def getRandomMove(self, moves) -> Move:
        random_move_index = random.randint(0, len(moves) - 1)
        return moves[random_move_index]
    
    def getNextMoveValues(self, moves: List[Move]) -> List:
        return [(self.piece_values[move.captured_piece[1]], move) for move in moves]
