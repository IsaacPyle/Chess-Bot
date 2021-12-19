class Board():
    def __init__(self):
        self.turn = "white"
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

# def setup():
        # start_pieces = {"a1": pieces.Rook("a1", "white"), "b1": pieces.Knight("b1", "white"), 
        #     "c1": pieces.Bishop("c1", "white"), "d1": pieces.Queen("d1", "white"), 
        #     "e1": pieces.King("e1", "white"), "f1": pieces.Bishop("f1", "white"), 
        #     "g1": pieces.Knight("g1", "white"), "h1": pieces.Rook("h1", "white"),
        #     "a2": pieces.Pawn("a2", "white"), "b2": pieces.Pawn("b2", "white"), 
        #     "c2": pieces.Pawn("c2", "white"), "d2": pieces.Pawn("d2", "white"),
        #     "e2": pieces.Pawn("e2", "white"), "f2": pieces.Pawn("f2", "white"), 
        #     "g2": pieces.Pawn("g2", "white"), "h2": pieces.Pawn("h2", "white"),
        #     "a8": pieces.Rook("a8", "black"), "b8": pieces.Knight("b8", "black"), 
        #     "c8": pieces.Bishop("c8", "black"), "d8": pieces.King("d8", "black"), 
        #     "e8": pieces.Queen("e8", "black"), "f8": pieces.Bishop("f8", "black"), 
        #     "g8": pieces.Knight("g8", "black"), "h8": pieces.Rook("h8", "black"),
        #     "a7": pieces.Pawn("a7", "black"), "b7": pieces.Pawn("b7", "black"), 
        #     "c7": pieces.Pawn("c7", "black"), "d7": pieces.Pawn("d7", "black"),
        #     "e7": pieces.Pawn("e7", "black"), "f7": pieces.Pawn("f7", "black"), 
        #     "g7": pieces.Pawn("g7", "black"), "h7": pieces.Pawn("h7", "black")}
        # return start_pieces

    # def move(self, piece, initial_location, end_location):
    #     temp = self.board_state.pop(initial_location)
    #     self.board_state[end_location] = temp
    #     if self.board_state[end_location]:
    #         if self.turn == "white":
    #             self.player.opponent_pieces.append(piece)
    #         else:
    #             self.bot.opponent_pieces.append(piece)