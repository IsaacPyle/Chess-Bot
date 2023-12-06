import heapq
import random
from typing import List
from board import Board, Castles, Move

class Bot():
    def __init__(self, depth: int = 2):
        # Ideas here
        self.piece_values = {'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 9, '-': 0} # <-- will be used for evaluation of capturing pieces
        self.enpassant = ()
        self.castles = ()
        self.checkmate = False
        self.stalemate = False
        self.evaluated = 0
        self.pruned = 0
        self.depth = depth

    def make_move(self, moves: List[Move], board: Board) -> List[Move]:
        self.evaluated = 0
        if len(moves) < 1:
            return False
        
        # preferred_move = (0, self.getRandomMove(moves))
        move = self.getBestMove(moves, board)
        print(f"checked {self.evaluated} moves, pruned {self.pruned} moves")
        if not move:
            return board.get_valid_moves()

        board.make_move(move)
        return board.get_valid_moves()
    
    # Find the best move, which is equal to the worst move for opponent after making this move.
    # Worst move for opponent is best for us, which is why we need the depth value
    def getBestMove(self, moves, board: Board) -> Move:
        # If no moves to make, return
        if not moves or moves == []:
            return None
        
        # For each move available at this state
        bestMoves = []
        bestEval = -999

        for move in moves:
            # We want to save the current state of the board, so it can be reset at the end
            self.saveBoardVars(board) # This doesn't work here and in the search method, need to redo
            # Actually make the move
            board.make_move(move)
            # Get all valid moves for the opponent, and their values (Based on capturing pieces only)
            evaluation = -self.search(board, self.depth, -999, 999)
            if evaluation > bestEval:
                bestEval = evaluation
                bestMoves = [move]
            if evaluation == bestEval:
                bestMoves.append(move)

            board.undo_move()
            self.resetBoardVars(board)
        
        print(f"Found {len(bestMoves)} moves with an eval of {bestEval}")
        return random.choice(bestMoves)
    
    def orderMoves(self, moves: List[Move]):
        moveTuples = []
        for move in moves:
            guess = 0
            if move.captured_piece != '--':
                guess = self.piece_values[move.captured_piece[1]]

            if move.pawn_promotion:
                guess += self.piece_values['Q'] # Could make this be whatever the best option is, assuming queen for now
            
            heapq.heappush(moveTuples, (guess, move))
        
        # print([guess for guess, _ in moveTuples], [guess for guess, _ in list(reversed(moveTuples))])
        moves = [move for _, move in list(reversed(moveTuples))]
    
    def search(self, board: Board, depth: int, alpha: int, beta: int) -> int:
        if depth == 0:
            return self.evaluate(board)
        
        moves = board.get_valid_moves()
        if len(moves) == 0:
            if board.check():
                return -100000
            return 0
        # print("before:", moves[0].moved_piece)
        self.orderMoves(moves)
        # print("after:", moves[0].moved_piece)

        for move in moves:
            self.saveBoardVars(board)
            board.make_move(move)
            evaluation = -self.search(board, depth-1, -beta, -alpha)
            board.undo_move()
            self.resetBoardVars(board)
            if evaluation >= beta:
                self.pruned += 1
                return beta
            alpha = max(alpha, evaluation)

        return alpha

    def evaluate(self, board: Board) -> int:
        whiteEval = 0
        for piece in board.captured_black_pieces:
            whiteEval += self.piece_values[piece[1]]
        
        for piece in board.captured_white_pieces:
            whiteEval -= self.piece_values[piece[1]]
        
        self.evaluated += 1
        
        if board.whites_turn:
            return whiteEval

        return -1 * whiteEval
    
    def saveBoardVars(self, board: Board):
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
