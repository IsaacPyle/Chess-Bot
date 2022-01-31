import pygame as py
from pygame.constants import CONTROLLERAXISMOTION
import board
import bot


WIDTH = HEIGHT = 512
SIDE_BAR_MULTIPLIER = 1.3
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 10
ICON_IMAGES = {}
IMAGES_MAIN = {}
IMAGES_SMALL = {}
IMAGES_ALT = {}
BACKGROUND = py.Color("grey")

def load_initial_images():
    '''
    Loads in our chess piece images, which only needs to happen once. 
    An expensive process which happends prior to the board displaying.
    '''
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bQ", "bK", "bB", "bN", "bR", "bP"]
    for piece in pieces:
        IMAGES_MAIN[piece] = py.transform.smoothscale(py.image.load("resources/" + piece + ".png").convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES_SMALL[piece] = py.transform.smoothscale(IMAGES_MAIN[piece], (SQUARE_SIZE // 2, SQUARE_SIZE // 2))

    ICON_IMAGES["Icon"] = py.transform.scale(py.image.load("resources/icon.png").convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))

def draw_gui_elements(screen, font):
    label = "Captured Pieces"
    # py.font.SysFont('Helvetica', 16, True, False)

    obj = font.render(label, 0, py.Color('Black'))
    location = py.Rect(WIDTH, 0, (WIDTH*SIDE_BAR_MULTIPLIER)-WIDTH, HEIGHT).move((((WIDTH * SIDE_BAR_MULTIPLIER) - WIDTH)/2) - obj.get_width()/2, HEIGHT * .7 - obj.get_height()/2)
    screen.blit(obj, location)
    obj = font.render(label, 0, py.Color('White'))
    screen.blit(obj, location.move(-2, -2))

    obj = font.render(label, 0, py.Color('White'))
    location = py.Rect(WIDTH, 0, (WIDTH*SIDE_BAR_MULTIPLIER)-WIDTH, HEIGHT).move((((WIDTH * SIDE_BAR_MULTIPLIER) - WIDTH)/2) - obj.get_width()/2, HEIGHT * .05 + obj.get_height()/2)
    screen.blit(obj, location)
    obj = font.render(label, 0, py.Color('Black'))
    screen.blit(obj, location.move(-2, -2))

def main():
    py.init()
    font = py.font.Font('./resources/Roboto-Medium.ttf', WIDTH // 32)
    screen = py.display.set_mode((WIDTH * SIDE_BAR_MULTIPLIER, HEIGHT))
    load_initial_images()
    py.display.set_caption('Chess-Bot')
    py.display.set_icon(ICON_IMAGES["Icon"])
    clock = py.time.Clock()
    screen.fill(BACKGROUND)
    draw_gui_elements(screen, font)
    bd = board.Board()
    AI = bot.Bot()
    selected_square = ()
    clicks = []
    valid_moves = bd.get_valid_moves()
    running = True
    made_move = False
    animate = False
    game_over = False
    king_check = False

    while running: # Main gameplay loop
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    loc = py.mouse.get_pos()
                    col = loc[0] // SQUARE_SIZE
                    row = loc[1] // SQUARE_SIZE
                    if col < 8:
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
                                    bd.make_move(other)
                                    made_move = True
                                    animate = True
                                    selected_square = ()
                                    clicks = []
                                    king_check = False

                            if not made_move:
                                clicks = [selected_square]
                                if (move.moved_piece[0] == "w" and bd.whites_turn) or (move.moved_piece[0] == "b" and not bd.whites_turn):
                                    bd.make_move(move)
                                    bd.whites_turn = not bd.whites_turn
                                    if bd.check():
                                        king_check = True
                                    bd.whites_turn = not bd.whites_turn
                                    bd.undo_move()
                            
                    
            elif e.type == py.KEYDOWN: # Handles 'z' key being pressed, indicating the user wants to undo a move
                if e.key == py.K_z:
                    bd.undo_move()
                    valid_moves = bd.get_valid_moves()
                    bd.checkmate = False
                    bd.stalemate = False
                    game_over = False
                if e.key == py.K_r:
                    bd = board.Board()
                    valid_moves = bd.get_valid_moves()
                    selected_square = ()
                    clicks = []
                    made_move = False
                    animate = False
                    game_over = False

        if made_move:
            if animate:
                animate_move(bd.move_log[-1], screen, bd, clock)
                
            valid_moves = bd.get_valid_moves()
            made_move = False
            animate = False
            makeAIMove(AI, valid_moves, bd, screen, clock)
            valid_moves = bd.get_valid_moves()
            
            
        drawGame(screen, bd, selected_square, king_check)

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

def makeAIMove(AI, moves, board, screen, clock):
    moves = board.get_valid_moves()
    new_moves = AI.make_move(moves, board)
    moves = new_moves
    py.time.wait(300)
    animate_move(board.move_log[-1], screen, board, clock)
    

def drawGame(screen, game, selected_square, king_check):
    '''
    Handles drawing of both board and pieces, and if a square is selected currently it draws that square also.
    '''
    king = game.white_king_loc if game.whites_turn else game.black_king_loc
    if selected_square != () and king_check:
        drawBoard(screen, selected_square, king)
    elif king_check:
        drawBoard(screen, None, king)
    elif selected_square != ():
        drawBoard(screen, selected_square)
    else:
        drawBoard(screen)

    drawPieces(screen, game)
    drawSidebar(screen, game)

def drawBoard(screen, selected=None, king_check=None):
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

    if king_check:
        py.draw.rect(screen, py.Color("#FF4242"), py.Rect(king_check[1]*SQUARE_SIZE, king_check[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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

def drawSidebar(screen, game):
    white_pieces = game.captured_white_pieces
    black_pieces = game.captured_black_pieces
    sidebar_size = WIDTH * 0.3
    start_horiz = WIDTH
    size = SQUARE_SIZE // 2

    if white_pieces != []:
        start_vert = HEIGHT * .125
        for i, piece in enumerate(white_pieces):
            x = start_horiz + ((sidebar_size // 4) * (i % 4))
            y = start_vert + (size * (i // 4))
            screen.blit(IMAGES_SMALL[piece], py.Rect(x, y, size, size))
        for i in range(len(white_pieces), 16):
            x = start_horiz + ((sidebar_size // 4) * (i % 4))
            y = start_vert + (size * (i // 4))
            py.draw.rect(screen, BACKGROUND, py.Rect(x, y, size, size))
    else:
        py.draw.rect(screen, BACKGROUND, py.Rect(WIDTH, HEIGHT * .125, WIDTH * (SIDE_BAR_MULTIPLIER - 1), HEIGHT // 4))

    if black_pieces != []:
        start_vert = HEIGHT * .75
        for i, piece in enumerate(black_pieces):
            x = start_horiz + ((sidebar_size // 4) * (i % 4))
            y = start_vert + (size * (i // 4))
            screen.blit(IMAGES_SMALL[piece], py.Rect(x, y, size, size))
        for i in range(len(black_pieces), 16):
            x = start_horiz + ((sidebar_size // 4) * (i % 4))
            y = start_vert + (size * (i // 4))
            py.draw.rect(screen, BACKGROUND, py.Rect(x, y, size, size))
    else:
        py.draw.rect(screen, BACKGROUND, py.Rect(WIDTH, HEIGHT * .75, WIDTH * (SIDE_BAR_MULTIPLIER - 1), HEIGHT // 4))


def animate_move(move, screen, board, clock):
    global colors
    row_dist = move.end_row - move.start_row
    col_dist = move.end_col - move.start_col
    frames = 10
    total_frames = frames + int((1.2 * abs(row_dist) + abs(col_dist)))


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
