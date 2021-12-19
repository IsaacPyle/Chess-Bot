 

class Pawn:
    def __init__(self, pos, color):
        self.name = "Pawn"
        self.color = color
        self.current_pos = pos
        self.moves = [(0, 1), (0, 2)]
        self.attacks = [(1, 1), (-1, 1)]

class Rook:
    def __init__(self, pos, color):
        self.name = "Rook"
        self.color = color
        self.current_pos = pos
        self.moves = ["h", "v"]
        self.attacks = ["h", "v"]

class Knight:
    def __init__(self, pos, color):
        self.name = "Knight"
        self.color = color
        self.current_pos = pos
        self.moves = [(-2, 1), (-2,-1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        self.attacks = [(-2, 1), (-2,-1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]

class Bishop:
    def __init__(self, pos, color):
        self.name = "Bishop"
        self.color = color
        self.current_pos = pos
        self.moves = ["d"]
        self.attacks = ["d"]

class Queen:
    def __init__(self, pos, color):
        self.name = "Queen"
        self.color = color
        self.current_pos = pos
        self.moves = ["h", "d", "v"]
        self.attacks = ["h", "d", "v"]

class King:
    def __init__(self, pos, color):
        self.name = "King"
        self.color = color
        self.current_pos = pos
        self.moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.attacks = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]



