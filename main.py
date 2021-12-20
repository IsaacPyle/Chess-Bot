import pygame as py
from pygame import color
from pygame.constants import MOUSEBUTTONDOWN, QUIT
import board


WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_initial_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bQ", "bK", "bB", "bN", "bR", "bP"]
    for piece in pieces:
        IMAGES[piece] = py.transform.scale(py.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color("white"))
    bd = board.Board()
    load_initial_images()
    running = True
    selected_square = ()
    clicks = []
    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                loc = py.mouse.get_pos()
                col = loc[0] // SQUARE_SIZE
                row = loc[1] // SQUARE_SIZE
                if selected_square == (row, col):
                    selected_square == ()
                    clicks == []
                else:
                    selected_square = (row, col)
                    clicks.append(selected_square)
                if len(clicks) == 2:
                    move = board.Move(bd.board_state, clicks[0], clicks[1])
                    bd.make_move(move)
                    selected_square = ()
                    clicks = []


        drawGame(screen, bd, selected_square)
        clock.tick(MAX_FPS)
        py.display.flip()

def drawGame(screen, game, selected_square):
    if selected_square != ():
        drawBoard(screen, selected_square)
    else:
        drawBoard(screen)

    drawPieces(screen, game.board_state)

def drawBoard(screen, selected=None):
    colors = [py.Color("#FAEBD7"), py.Color("#CDAA7D")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2] 
            py.draw.rect(screen, color, py.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if selected:
        py.draw.rect(screen, py.Color("#FFFF00"), py.Rect(selected[1]*SQUARE_SIZE, selected[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c] 
            if piece != "--":
                screen.blit(IMAGES[piece], py.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

if __name__ == "__main__":
    main()
