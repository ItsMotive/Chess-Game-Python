# ---------------- 1: Importing Modules ----------------
import pygame
import requests
import rembg
from io import BytesIO
import const as CONST

# ---------------- 2: Initialize Pygame and set Chest Game Screen ----------------

# Initialize Pygame module
pygame.init()

# Setting Width and height of Chess Game Screen

screen = pygame.display.set_mode([CONST.WIDTH, CONST.HEIGHT])
pygame.display.set_caption('Chess Game')

# ---------------- 3: Initialize fonts and clock ----------------
font = pygame.font.Font(CONST.FREE_SANS_BOLD, 20)
medium_font = pygame.font.Font(CONST.FREE_SANS_BOLD, 40)
big_font = pygame.font.Font(CONST.FREE_SANS_BOLD, 50)

timer = pygame.time.Clock()

# ---------------- 4: Game Variables and Images ----------------

captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

# ---------------- 5: Loading Game Piece Images ----------------

# Black Queen
black_queen = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[0]).content)))
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

# Black King
black_king = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[1]).content)))
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))

# Black Rook
black_rook = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[2]).content)))
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

# Black Bishop
black_bishop = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[3]).content)))
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

# Black Knight
black_knight = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[4]).content)))
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

# Black Pawn
black_pawn = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[5]).content)))
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

# White Queen
white_queen = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[6]).content)))
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

# White King
white_king = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[7]).content)))
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))

# White Rook
white_rook = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[8]).content)))
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

# White Bishop
white_bishop = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[9]).content)))
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

# White Knight
white_knight = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[10]).content)))
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

# White Pawn
white_pawn = pygame.image.load(
    BytesIO(rembg.remove(requests.get(CONST.IMAGE_URLS[11]).content)))
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

# ---------------- 6: Grouping Piece Images ----------------
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook,white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False

# ---------------- 7: Board Drawing Functions ----------------

# Main Board
def drawBoard():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', 
                             [600 - (column * 200), row * 100, 100, 100])
        
        else: 
            pygame.draw.rect(screen, 'light gray', 
                             [700 - (column * 200), row * 100, 100, 100])
            
        pygame.draw.rect(screen, 'gray',
                         [0, 800, CONST.WIDTH, 100])
        pygame.draw.rect(screen, 'gold', 
                         [0, 800, CONST.WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', 
                         [800, 0, 200, CONST.HEIGHT], 5)
        
        status_text = ['White: Select a Piece to Move.', 'White: Select a Destination',
                       'Black: Select a Piece to Move.', 'Black: Select a Destination']
        
        screen.blit(big_font.render(status_text[turn_step], True, 'black'),
                    (20, 820))
        
        for i in range(9):
            pygame.draw.line(screen, 'black',
                             (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', 
                             (100 * i, 0), (100 * i, 800), 2)
        
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))

# ---------------- 8: Piece Drawing Functions ----------------  

# Draw Pieces on the Board
def drawPieces():
    for i in range(len(CONST.WHITE_PIECES)):
        index = piece_list.index(CONST.WHITE_PIECES[i])
        if CONST.WHITE_PIECES[i] == 'pawn':
            screen.blit( white_pawn, 
                        (CONST.WHITE_LOCATIONS[i][0] * 100 + 22, 
                         CONST.WHITE_LOCATIONS[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], 
                        (CONST.WHITE_LOCATIONS[i][0] * 100 + 10, 
                         CONST.WHITE_LOCATIONS[i][1] * 100 + 10))
            
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', 
                                 [CONST.WHITE_LOCATIONS[i][0] * 100 + 1, 
                                  CONST.WHITE_LOCATIONS[i][1] * 100 + 1, 
                                  100, 100], 2)
                
    for i in range(len(CONST.BLACK_PIECES)):
        index = piece_list.index(CONST.BLACK_PIECES[i])
        if CONST.BLACK_PIECES[i] == 'pawn':
            screen.blit( black_pawn, 
                        (CONST.BLACK_LOCATIONS[i][0] * 100 + 22, 
                         CONST.BLACK_LOCATIONS[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], 
                        (CONST.BLACK_LOCATIONS[i][0] * 100 + 10, 
                         CONST.BLACK_LOCATIONS[i][1] * 100 + 10))
            
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', 
                                 [CONST.BLACK_LOCATIONS[i][0] * 100 + 1, 
                                  CONST.BLACK_LOCATIONS[i][1] * 100 + 1, 
                                  100, 100], 2)
                
# function to check all pieces valid options on board
def checkOptions(pieces, locations, turn):
    move_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]

        if piece == 'pawn':
            move_list = checkPawn(location, turn)

        elif piece == 'rook':
            move_list = checkRook(location, turn)

        elif piece == 'knight':
            move_list = checkKnight(location, turn)

        elif piece == 'bishop':
            move_list = checkBishop(location, turn)

        elif piece == 'queen':
            move_list = checkQueen(location, turn)

        elif piece == 'king':
            move_list = checkKing(location, turn)
        
        all_moves_list.append(move_list)

    return all_moves_list

# Valid King Moves
def checkKing(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = CONST.BLACK_LOCATIONS
        friend_list = CONST.WHITE_LOCATIONS

    else:
        friend_list = CONST.BLACK_LOCATIONS
        enemies_list = CONST.WHITE_LOCATIONS

    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
               (-1, 1), (-1, -1), (0, 1), (0, -1)]
    
    for i in range(len(targets)):

        target = (position[0] + targets[i][0], 
                  position[1] + targets[i][1])
        
        if target not in friend_list and \
                ( 0 <= target[0] <= 7 ) and \
                ( 0 <= target[1] <= 7 ):
            
            moves_list.append(target)

    return moves_list

# Valid Queen Moves
def checkQueen(position, color):
    moves_list = checkBishop(position, color)
    second_list = checkRook(position, color)

    for i in range(len(second_list)):
        moves_list.append(second_list[i])

    return moves_list

# Valid Bishop Moves
def checkBishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = CONST.BLACK_LOCATIONS
        friend_list = CONST.WHITE_LOCATIONS

    else:
        friend_list = CONST.BLACK_LOCATIONS
        enemies_list = CONST.WHITE_LOCATIONS

    # up-right, up-left, down-right, down-left
    for i in range(4):
        path = True
        chain = 1

        if i == 0:
            x = 1
            y = -1

        elif i == 1:
            x = -1
            y = -1

        elif i == 2:
            x = 1
            y = 1

        else:
            x = -1
            y = 1

        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friend_list and \
                    0 <= position[0] + (chain * x) <= 7 and \
                    0 <= position[1] + (chain * y) <= 7:
                
                moves_list.append((position[0] + (chain * x), 
                                  position[1] + (chain * y))
                                  )

                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
            
                chain += 1

            else:
                path = False

    return moves_list

# Valid Rook Moves
def checkRook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = CONST.BLACK_LOCATIONS
        friend_list = CONST.WHITE_LOCATIONS

    else:
        friend_list = CONST.BLACK_LOCATIONS
        enemies_list = CONST.WHITE_LOCATIONS

    # Down, Up, Right, Left
    for i in range(4):
        path = True
        chain = 1

        if i == 0:
            x = 0
            y = 1
        
        elif i == 1:
            x = 0
            y = -1

        elif i == 2:
            x = 1
            y = 0

        else:
            x = -1
            y = 0

        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friend_list and \
                    0 <= position[0] + (chain * x) <= 7 and \
                    0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x),
                                  position[1] + (chain * y)))
                
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False

                chain += 1
            
            else:
                path = False
    return moves_list

# Valid Pawn Moves
def checkPawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in CONST.WHITE_LOCATIONS and \
                (position[0], position[1] + 1) not in CONST.BLACK_LOCATIONS and \
                position[1] < 7:
            moves_list.append((position[0], position[1] + 1))

        if (position[0], position[1] + 2) not in CONST.WHITE_LOCATIONS and \
                (position[0], position[1] + 2) not in CONST.BLACK_LOCATIONS and \
                position[1] == 1:
            moves_list.append((position[0], position[1] + 2))

        if (position[0] + 1, position[1] + 1) in CONST.BLACK_LOCATIONS:
            moves_list.append((position[0] + 1, position[1] + 1))

        if (position[0] - 1, position[1] + 1) in CONST.BLACK_LOCATIONS:
            moves_list.append((position[0] - 1, position[1] + 1)) 

    else:
        if (position[0], position[1] - 1) not in CONST.WHITE_LOCATIONS and \
                (position[0], position[1] - 1) not in CONST.BLACK_LOCATIONS and \
                position[1] > 0:
            moves_list.append((position[0], position[1] - 1))

        if (position[0], position[1] - 2) not in CONST.WHITE_LOCATIONS and \
                (position[0], position[1] - 2) not in CONST.BLACK_LOCATIONS and \
                position[1] == 6:
            moves_list.append((position[0], position[1] - 2))

        if (position[0] + 1, position[1] - 1) in CONST.WHITE_LOCATIONS:
            moves_list.append((position[0] + 1, position[1] - 1))

        if (position[0] - 1, position[1] - 1) in CONST.WHITE_LOCATIONS:
            moves_list.append((position[0] - 1, position[1] - 1)) 

    return moves_list

# Valid Knight Moves
def checkKnight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = CONST.BLACK_LOCATIONS
        friend_list = CONST.WHITE_LOCATIONS

    else:
        friend_list = CONST.BLACK_LOCATIONS
        enemies_list = CONST.WHITE_LOCATIONS

    # Knights can move two squares one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    
    for i in range(len(targets)):
        target = (position[0] + targets[i][0],
                  position[1] + targets[i][1])
        
        if target not in friend_list and \
                0 <= target[0] <= 7 and \
                0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list

# Checks for valid moves of the selected piece
def checkValidMoves():
    if turn_step < 2:
        options_list = white_options

    else:
        options_list = black_options

    valid_options = options_list[selection]
    return valid_options

# Valid Move Visualizer
def drawValid(moves):
    if turn_step < 2:
        color = 'red'
    
    else:
        color = 'blue'
    
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

# Displays captured pieces
def drawCaptured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))

    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))

# Displays King is in check
def drawCheck():
    if turn_step < 2:
        if 'king' in CONST.WHITE_PIECES:
            king_index = CONST.WHITE_PIECES.index('king')
            king_location = CONST.WHITE_LOCATIONS[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [CONST.WHITE_LOCATIONS[king_index][0] * 100 + 1,
                                                              CONST.WHITE_LOCATIONS[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in CONST.BLACK_PIECES:
            king_index = CONST.BLACK_PIECES.index('king')
            king_location = CONST.BLACK_LOCATIONS[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [CONST.BLACK_LOCATIONS[king_index][0] * 100 + 1,
                                                               CONST.BLACK_LOCATIONS[king_index][1] * 100 + 1, 100, 100], 5)

# Game Over Screen                
def drawGameOver():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(
        f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!',
                            True, 'white'), (210, 240))
    
# ---------------- 9: Game Loop and Event Handling ----------------  

# Main Game Loop
black_options = checkOptions(CONST.BLACK_PIECES, CONST.BLACK_LOCATIONS, 'black')
white_options = checkOptions(CONST.WHITE_PIECES, CONST.WHITE_LOCATIONS, 'white')
run = True
while run:
    timer.tick(CONST.FPS)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    drawBoard()
    drawPieces()
    drawCaptured()
    drawCheck()
    if selection != 100:
        valid_moves = checkValidMoves()
        drawValid(valid_moves)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Handling left mouse button clicks when the game is not over
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)

            # Handling player input during the first two turns
            if turn_step <= 1:

                # Check if the player clicked on forfeit squares
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'

                # Check if the clicked coordinates belong to white pieces
                if click_coords in CONST.WHITE_LOCATIONS:
                    selection = CONST.WHITE_LOCATIONS.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1

                # Check if the clicked coordinates are valid moves for the selected white piece
                if click_coords in valid_moves and selection != 100:
                    CONST.WHITE_LOCATIONS[selection] = click_coords

                    # Check for capturing black pieces
                    if click_coords in CONST.BLACK_LOCATIONS:
                        black_piece = CONST.BLACK_LOCATIONS.index(click_coords)
                        captured_pieces_white.append(CONST.BLACK_PIECES[black_piece])
                        if CONST.BLACK_PIECES[black_piece] == 'king':
                            winner = 'white'
                        CONST.BLACK_PIECES.pop(black_piece)
                        CONST.BLACK_LOCATIONS.pop(black_piece)

                    # Update move options for both black and white
                    black_options = checkOptions(
                        CONST.BLACK_PIECES, CONST.BLACK_LOCATIONS, 'black')
                    white_options = checkOptions(
                        CONST.WHITE_PIECES, CONST.WHITE_LOCATIONS, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            # Handling player input during the last two turns
            if turn_step > 1:

                # Check if the player clicked on forfeit squares
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'

                # Check if the clicked coordinates belong to black pieces
                if click_coords in CONST.BLACK_LOCATIONS:
                    selection = CONST.BLACK_LOCATIONS.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3

                # Check if the clicked coordinates are valid moves for the selected black piece
                if click_coords in valid_moves and selection != 100:
                    CONST.BLACK_LOCATIONS[selection] = click_coords

                    # Check for capturing white pieces
                    if click_coords in CONST.WHITE_LOCATIONS:
                        white_piece = CONST.WHITE_LOCATIONS.index(click_coords)
                        captured_pieces_black.append(CONST.WHITE_PIECES[white_piece])
                        if CONST.WHITE_PIECES[white_piece] == 'king':
                            winner = 'black'
                        CONST.WHITE_PIECES.pop(white_piece)
                        CONST.WHITE_LOCATIONS.pop(white_piece)

                    # Update move options for both black and white
                    black_options = checkOptions(
                        CONST.BLACK_PIECES, CONST.BLACK_LOCATIONS, 'black')
                    white_options = checkOptions(
                        CONST.WHITE_PIECES, CONST.WHITE_LOCATIONS, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []

        # Handling key press events when the game is over
        if event.type == pygame.KEYDOWN and game_over:

            # Check if the pressed key is the "Enter" key
            if event.key == pygame.K_RETURN:

                # Resetting the game state when the "Enter" key is pressed
                game_over = False
                winner = ''
                CONST.WHITE_PIECES = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                CONST.WHITE_LOCATIONS = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                CONST.BLACK_PIECES = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                CONST.BLACK_LOCATIONS = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []

                # Update move options for both black and white
                black_options = checkOptions(CONST.BLACK_PIECES, CONST.BLACK_LOCATIONS, 'black')
                white_options = checkOptions(CONST.WHITE_PIECES, CONST.WHITE_LOCATIONS, 'white')

    # Checking for a winner and displaying game over message
    if winner != '':
        game_over = True
        drawGameOver()

    pygame.display.flip()

pygame.quit()