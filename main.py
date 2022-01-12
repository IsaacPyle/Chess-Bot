import pygame as py
from pygame import display
from pygame.constants import CONTROLLERAXISMOTION
import board
import random
import bot


WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
ICON_IMAGES = {}
IMAGES_MAIN = {}
IMAGES_ALT = {}

def load_initial_images():
    '''
    Loads in our chess piece images, which only needs to happen once. 
    An expensive process which happends prior to the board displaying.
    '''
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bQ", "bK", "bB", "bN", "bR", "bP"]
    for piece in pieces:
        IMAGES_MAIN[piece] = py.transform.scale(py.image.load("images/" + piece + ".png").convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
    ICON_IMAGES["Icon"] = py.transform.scale(py.image.load("images/icon.png").convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    load_initial_images()
    py.display.set_caption('A Game of Chess')
    py.display.set_icon(ICON_IMAGES["Icon"])
    font = py.font.Font('freesansbold.ttf', 32)
    clock = py.time.Clock()
    screen.fill(py.Color("white"))
    bd = board.Board()
    AI = bot.Bot()
    selected_square = ()
    clicks = []
    valid_moves = bd.get_valid_moves()
    running = True
    made_move = False
    animate = False
    game_over = False

    while running: # Main gameplay loop
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                loc = py.mouse.get_pos()
                col = loc[0] // SQUARE_SIZE
                row = loc[1] // SQUARE_SIZE
                if selected_square == (row, col): # User clicked the same square twice, we want to deselect it
                    selected_square = ()
                    clicks = []
                else:
                    selected_square = (row, col)
                    clicks.append(selected_square)
                if len(clicks) == 2: # two different squares have been clicked, begin moving piece from first to second
                    move = board.Move(bd.board_state, clicks[0], clicks[1])
                    for other in valid_moves:
                        if move.check_eq(other):
                            bd.make_move(move)
                            made_move = True
                            animate = True
                            selected_square = ()
                            clicks = []
                    if not made_move:
                        clicks = [selected_square]
                    
            elif e.type == py.KEYDOWN: # Handles 'z' key being pressed, indicating the user wants to undo a move
                if e.key == py.K_z:
                    bd.undo_move()
                    valid_moves = bd.get_valid_moves()
                if e.key == py.K_r:
                    bd = board.Board()
                    valid_moves = bd.get_valid_moves()
                    selected_square = ()
                    clicks = []
                    made_move = False
                    animate = False

        if made_move:
            if animate:
                animate_move(bd.move_log[-1], screen, bd, clock)
            valid_moves = bd.get_valid_moves()
            made_move = False
            animate = False
            
        drawGame(screen, bd, selected_square)

        # Check for checkmate
        if bd.checkmate:
            game_over = True
            if bd.whites_turn:
                drawText(screen, "Black wins!")
            else:
                drawText(screen, "White wins!")

        # Check for stalemate
        elif bd.stalemate:
            game_over = True
            drawText(screen, "Stalemate!")


        clock.tick(MAX_FPS)
        py.display.flip()

def highlight(screen, bd, valid_moves, selected_square):
    if selected_square != ():
        row, col = selected_square
        if bd.board_state[row][col][0] == ('w' if bd.whites_turn else 'b'):
            square = py.Surface((SQUARE_SIZE, SQUARE_SIZE))
            square.set_alpha(100)
            square.fill(py.Color('#FFFF00'))
            screen.blit(square, (col*SQUARE_SIZE, row*SQUARE_SIZE))

            square.fill(py.Color('blue'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(square, (move.end_col*SQUARE_SIZE, move.end_row*SQUARE_SIZE))

def drawGame(screen, game, selected_square):
    '''
    Handles drawing of both board and pieces, and if a square is selected currently it draws that square also.
    '''
    if selected_square != ():
        drawBoard(screen, selected_square)
    else:
        drawBoard(screen)

    drawPieces(screen, game)

def drawBoard(screen, selected=None):
    '''
    Draws background board, and draws highlighted square if one is selected.
    '''
    global colors
    colors = [py.Color("#FAEBD7"), py.Color("#CDAA7D")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2] 
            py.draw.rect(screen, color, py.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if selected:
        py.draw.rect(screen, py.Color("#FFFF00"), py.Rect(selected[1]*SQUARE_SIZE, selected[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, game):
    '''
    Draws each piece individually to the board after the background board has been drawn 
    '''
    board = game.board_state
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c] 
            if piece != "--":
                screen.blit(IMAGES_MAIN[piece], py.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Here depending on further implementation we could invert the board when opponent's turn

def animate_move(move, screen, board, clock):
    global colors
    row_dist = move.end_row - move.start_row
    col_dist = move.end_col - move.start_col
    frames = 10
    total_frames = frames + int((1.2 * abs(row_dist) + abs(col_dist)))# (abs(row_dist) + abs(col_dist)) * frames


    for frame in range(total_frames + 1):
        row, col = (move.start_row + row_dist*frame/total_frames, move.start_col+ col_dist*frame/total_frames)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = py.Rect(move.end_col*SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        py.draw.rect(screen, color, end_square)
        if move.captured_piece != '--':
            screen.blit(IMAGES_MAIN[move.captured_piece], end_square)

        screen.blit(IMAGES_MAIN[move.moved_piece], py.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        clock.tick(60)
        py.display.flip()

def drawText(screen, text):
    font = py.font.SysFont('Helvetica', 32, True, False)
    obj = font.render(text, 0, py.Color('Grey'))
    location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - obj.get_width()/2, HEIGHT/2 - obj.get_height()/2)
    screen.blit(obj, location)
    obj = font.render(text, 0, py.Color('Black'))
    screen.blit(obj, location.move(2, 2))

if __name__ == "__main__":
    main()
