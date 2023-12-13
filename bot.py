from dataclasses import dataclass
import heapq
import random
from typing import List
from board import Board, Castles, Move

@dataclass
class BoardStateVars:
    checkmate: bool
    stalemate: bool

class Bot():
    def __init__(self, depth: int = 0):
        self.piece_values = {'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 9, '-': 0} # used for evaluation of capturing pieces
        self.evaluated = 0
        self.pruned = 0
        self.depth = depth

    def make_move(self, moves: List[Move], board: Board) -> List[Move]:
        self.evaluated = 0
        if len(moves) < 1:
            return False
        
        print(board.castle_moves)
        
        move = self.getBestMove(moves, board)
        print(f"checked {self.evaluated} moves, pruned {self.pruned} moves")
        if not move:
            board.checkmate = True
            return board.get_valid_moves()

        board.make_move(move)
        return board.get_valid_moves()
    
    # Find the best move, which is equal to the worst move for opponent after making this move.
    # Worst move for opponent is best for us, which is why we need the depth value
    def getBestMove(self, moves: List[Move], board: Board) -> Move:
        # If no moves to make, return
        if not moves or moves == []:
            return None
        
        # For each move available at this state
        bestMoves = moves
        bestEval = -999
        print(board.castle_moves)
        for move in moves:
            # We want to save the current state of the board, so it can be reset at the end
            bsv = self.saveBoardVars(board)
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
            self.resetBoardVars(bsv, board)
        print(board.castle_moves)
        
        print(f"Found {len(bestMoves)} moves with an eval of {bestEval}")
        return random.choice(bestMoves)
    
    def orderMoves(self, moves: List[Move]) -> List[Move]:
        moveTuples = []
        for move in moves:
            guess = 0
            if move.captured_piece != '--':
                guess = self.piece_values[move.captured_piece[1]]

            if move.pawn_promotion:
                guess += self.piece_values['Q'] # Could make this be whatever the best option is, assuming queen for now

            if Board().piece_attacked(move.end[0], move.end[1]):
                guess -= self.piece_values[move.captured_piece[1]]
            
            heapq.heappush(moveTuples, (guess, move))
        
        # print([guess for guess, _ in moveTuples], [guess for guess, _ in list(reversed(moveTuples))])
        return [move for _, move in list(reversed(moveTuples))]
    
    def search(self, board: Board, depth: int, alpha: int, beta: int) -> int:
        if depth == 0:
            return self.evaluate(board)
        
        moves = board.get_valid_moves(isRealMove=False)
        if len(moves) == 0:
            if board.check():
                return -100000
            return 0
        # print("before:", moves[0].moved_piece)
        moves = self.orderMoves(moves)
        # print("after:", moves[0].moved_piece)

        for move in moves:
            bsv = self.saveBoardVars(board)
            board.make_move(move)
            evaluation = -self.search(board, depth-1, -beta, -alpha)
            board.undo_move()
            self.resetBoardVars(bsv, board)
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
    
    def saveBoardVars(self, board: Board) -> BoardStateVars:
        return BoardStateVars(board.checkmate, board.stalemate)

    def resetBoardVars(self, bsv: BoardStateVars, board: Board):
        board.checkmate = bsv.checkmate
        board.stalemate = bsv.stalemate

    def getRandomMove(self, moves) -> Move:
        random_move_index = random.randint(0, len(moves) - 1)
        return moves[random_move_index]
    
    def getNextMoveValues(self, moves: List[Move]) -> List:
        return [(self.piece_values[move.captured_piece[1]], move) for move in moves]