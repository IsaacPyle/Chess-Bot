import pygame as py
import board
import random
import bot


WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
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

def main():
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color("white"))
    bd = board.Board()
    AI = bot.Bot()
    load_initial_images()
    running = True
    selected_square = ()
    clicks = []
    valid_moves = bd.get_valid_moves()

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
                    if bd.board_state[clicks[0][0]][clicks[0][1]] != "--":
                        move = board.Move(bd.board_state, clicks[0], clicks[1])
                        for other in valid_moves:
                            if move.check_eq(other):
                                bd.make_move(move)
                                # Uncomment for AI to make random move, only random and not using AI at the moment
                                valid_moves = bd.get_valid_moves()
                                # valid_moves = AI.make_move(valid_moves, bd)
                                for move in valid_moves:
                                    if move.enpassant_move:
                                        print(move.start_row, move.start_col, move.end_row, move.end_col)
                    selected_square = ()
                    clicks = []
                    
            elif e.type == py.KEYDOWN: # Handles 'u' key being pressed, indicating the user wants to undo a move
                if e.key == py.K_u:
                    bd.undo_move()


        drawGame(screen, bd, selected_square)
        clock.tick(MAX_FPS)
        py.display.flip()

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

if __name__ == "__main__":
    main()
