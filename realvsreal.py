###################################
#                                 #
#    Created By DrFrostij         #
#                                 #
###################################


########################
# The imports section  #
########################


import os                       # this is used to get the images + sounds we want                   # (needs pip installment)
# https://docs.python.org/3/library/os.html                                                         #OS documentation
import chess                    # this is for the chess board logic                                 # (needs pip installment)
#https://python-chess.readthedocs.io/en/latest/                                                     #Chess documentation
import pygame                   # this is for the graphics and sounds                               # (needs pip installment)
#https://www.pygame.org/docs/                                                                       #Pygame documentation
import customtkinter as customtkinter  # this is for the GUI                                        # (needs pip installment)
#https://customtkinter.tomschimansky.com                                                            #Custom Tkinter documentation
import bcrypt                         # this is for the password hashing                            # (needs pip installment)    
#https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/                      #Bcrypt documentation
from PIL import Image, ImageTk          # this is for loading images                                # (needs pip installment)
#https://pillow.readthedocs.io/en/stable/                                                           #PIL documentation
from tkinter import HORIZONTAL, Button, Scale, mainloop, messagebox    #pop ups                     # (needs pip installment)
#https://docs.python.org/3/library/tkinter.messagebox.html                                          #Message box documentation    
import tkinter                                                                                      #PIL documentation
#https://docs.python.org/3/library/tkinter.html                                                     #Tkinter documentation

##############################
# Importing from other files #
##############################

import pygame
import chess
from soundimagedatabase import sound, pieces

##########################
# Main Startup Code Area #
##########################

pygame.init()
pygame.mixer.init()

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60

########################
# Main game            #
########################

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ChessQuest: Real vs Real")
    clock = pygame.time.Clock()
    board = chess.Board()
    selected_square = None
    running = True

    # Game start sound
    sound["game_start"].play()

    while running:
        for event in pygame.event.get():

            ########################
            # Close game           #
            ########################

            if event.type == pygame.QUIT:
                running = False

            ########################
            # Mouse click          #
            ########################

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // SQ_SIZE
                row = mouse_y // SQ_SIZE

                # Convert screen position to chess square
                square = chess.square(col, 7 - row)

                ########################
                # Nothing selected     #
                ########################

                if selected_square is None:
                    piece = board.piece_at(square)

                    if piece is not None:
                        # Only allow the player to select their own pieces
                        if piece.color == board.turn:
                            selected_square = square

                ########################
                # Piece already selected
                ########################

                else:
                    piece = board.piece_at(selected_square)

                    ########################
                    # Check promotion      #
                    ########################

                    if (
                        piece
                        and piece.piece_type == chess.PAWN
                        and chess.square_rank(square) in [0, 7]
                    ):
                        promotion_piece = promotionPopup(screen, board.turn)

                        if promotion_piece is None:
                            selected_square = None
                            continue

                        move = chess.Move(
                            selected_square,
                            square,
                            promotion=promotion_piece
                        )
                    else:
                        move = chess.Move(
                            selected_square,
                            square
                        )

                    ########################
                    # Check legal move     #
                    ########################

                    if move in board.legal_moves:
                        is_capture = board.is_capture(move)
                        is_castle = board.is_castling(move)
                        is_promotion = move.promotion is not None

                        ########################
                        # Make move            #
                        ########################

                        board.push(move)

                        ########################
                        # Play sounds          #
                        ########################

                        if is_promotion:
                            sound["promote"].play()
                        elif is_castle:
                            sound["castle"].play()
                        elif is_capture:
                            sound["capture"].play()
                        else:
                            sound["move-self"].play()

                        ########################
                        # Check                #
                        ########################

                        if board.is_check():
                            sound["move-check"].play()

                        ########################
                        # Checkmate            #
                        ########################

                        if board.is_checkmate():
                            sound["game-end"].play()

                            if board.turn == chess.WHITE:
                                winner = "Black"
                            else:
                                winner = "White"

                            result = checkmatePopup(screen, winner)

                            if result == "reset":
                                board.reset()
                                selected_square = None
                                sound["game_start"].play()

                            elif result == "quit":
                                running = False

                            continue

                        selected_square = None

                    ########################
                    # Illegal move         #
                    ########################

                    else:
                        sound["illegal"].play()

                        # If another one of the player's pieces was clicked, select it
                        new_piece = board.piece_at(square)

                        if (
                            new_piece is not None
                            and new_piece.color == board.turn
                        ):
                            selected_square = square
                        else:
                            selected_square = None

        ########################
        # Draw game            #
        ########################

        drawGameState(screen, board, selected_square)
        pygame.display.flip()
        clock.tick(MAX_FPS)

    ########################
    # Close pygame         #
    ########################

    pygame.quit()

########################
# Promotion popup      #
########################

def promotionPopup(screen, turn):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)

    ########################
    # Popup                #
    ########################

    popup_width = 400
    popup_height = 250
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    pygame.draw.rect(
        overlay,
        pygame.Color("white"),
        (popup_x, popup_y, popup_width, popup_height)
    )

    pygame.draw.rect(
        overlay,
        pygame.Color("black"),
        (popup_x, popup_y, popup_width, popup_height),
        4
    )

    ########################
    # Text                 #
    ########################

    title = font.render(
        "Choose promotion",
        True,
        pygame.Color("black")
    )

    screen.blit(overlay, (0, 0))

    screen.blit(
        title,
        (
            popup_x + (popup_width - title.get_width()) // 2,
            popup_y + 25
        )
    )

    ########################
    # Promotion options    #
    ########################

    options = [
        ("Queen", chess.QUEEN),
        ("Rook", chess.ROOK),
        ("Bishop", chess.BISHOP),
        ("Knight", chess.KNIGHT)
    ]

    buttons = []
    button_width = 160
    button_height = 40

    for index, (name, piece_type) in enumerate(options):
        x = popup_x + 20
        y = popup_y + 75 + index * 40

        rect = pygame.Rect(
            x,
            y,
            button_width,
            button_height
        )

        pygame.draw.rect(
            screen,
            pygame.Color("lightgray"),
            rect
        )

        pygame.draw.rect(
            screen,
            pygame.Color("black"),
            rect,
            2
        )

        text = small_font.render(
            name,
            True,
            pygame.Color("black")
        )

        screen.blit(
            text,
            (
                rect.centerx - text.get_width() // 2,
                rect.centery - text.get_height() // 2
            )
        )

        buttons.append((rect, piece_type))

    pygame.display.flip()

    ########################
    # Wait for selection   #
    ########################

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, piece_type in buttons:
                    if rect.collidepoint(event.pos):
                        return piece_type

        pygame.time.Clock().tick(60)

########################
# Checkmate popup      #
########################

def checkmatePopup(screen, winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))

    ########################
    # Popup                #
    ########################

    popup_width = 400
    popup_height = 220
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    pygame.draw.rect(
        overlay,
        pygame.Color("white"),
        (popup_x, popup_y, popup_width, popup_height)
    )

    pygame.draw.rect(
        overlay,
        pygame.Color("black"),
        (popup_x, popup_y, popup_width, popup_height),
        4
    )

    ########################
    # Text                 #
    ########################

    title_font = pygame.font.Font(None, 40)
    text_font = pygame.font.Font(None, 30)
    button_font = pygame.font.Font(None, 25)

    title = title_font.render(
        "CHECKMATE!",
        True,
        pygame.Color("black")
    )

    winner_text = text_font.render(
        winner + " wins!",
        True,
        pygame.Color("black")
    )

    screen.blit(overlay, (0, 0))

    screen.blit(
        title,
        (
            popup_x + (popup_width - title.get_width()) // 2,
            popup_y + 25
        )
    )

    screen.blit(
        winner_text,
        (
            popup_x + (popup_width - winner_text.get_width()) // 2,
            popup_y + 75
        )
    )

    ########################
    # Buttons              #
    ########################

    reset_button = pygame.Rect(
        popup_x + 40,
        popup_y + 135,
        140,
        50
    )

    quit_button = pygame.Rect(
        popup_x + 220,
        popup_y + 135,
        140,
        50
    )

    pygame.draw.rect(
        screen,
        pygame.Color("lightgray"),
        reset_button
    )

    pygame.draw.rect(
        screen,
        pygame.Color("lightgray"),
        quit_button
    )

    pygame.draw.rect(
        screen,
        pygame.Color("black"),
        reset_button,
        2
    )

    pygame.draw.rect(
        screen,
        pygame.Color("black"),
        quit_button,
        2
    )

    reset_text = button_font.render(
        "Reset",
        True,
        pygame.Color("black")
    )

    quit_text = button_font.render(
        "Quit",
        True,
        pygame.Color("black")
    )

    screen.blit(
        reset_text,
        (
            reset_button.centerx - reset_text.get_width() // 2,
            reset_button.centery - reset_text.get_height() // 2
        )
    )

    screen.blit(
        quit_text,
        (
            quit_button.centerx - quit_text.get_width() // 2,
            quit_button.centery - quit_text.get_height() // 2
        )
    )

    pygame.display.flip()

    ########################
    # Wait for button      #
    ########################

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:

                if reset_button.collidepoint(event.pos):
                    return "reset"

                if quit_button.collidepoint(event.pos):
                    return "quit"

        pygame.time.Clock().tick(60)

########################
# Draw game            #
########################

def drawGameState(screen, board, selected_square):
    drawBoard(screen, selected_square)
    drawValidMoves(screen, board, selected_square)
    drawPieces(screen, board)

########################
# Draw board           #
########################

def drawBoard(screen, selected_square):
    colors = [
        pygame.Color("white"),
        pygame.Color("chocolate4")
    ]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]

            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    c * SQ_SIZE,
                    r * SQ_SIZE,
                    SQ_SIZE,
                    SQ_SIZE
                )
            )

    ########################
    # Highlight selection  #
    ########################

    if selected_square is not None:
        row = 7 - chess.square_rank(selected_square)
        col = chess.square_file(selected_square)

        pygame.draw.rect(
            screen,
            pygame.Color("yellow"),
            pygame.Rect(
                col * SQ_SIZE,
                row * SQ_SIZE,
                SQ_SIZE,
                SQ_SIZE
            ),
            5
        )

########################
# Draw valid moves     #
########################

def drawValidMoves(screen, board, selected_square):
    if selected_square is None:
        return

    for move in board.legal_moves:

        if move.from_square != selected_square:
            continue

        col = chess.square_file(move.to_square)
        row = 7 - chess.square_rank(move.to_square)

        center_x = col * SQ_SIZE + SQ_SIZE // 2
        center_y = row * SQ_SIZE + SQ_SIZE // 2

        ########################
        # Capture indicator    #
        ########################

        if board.piece_at(move.to_square):
            pygame.draw.circle(
                screen,
                pygame.Color("green"),
                (center_x, center_y),
                SQ_SIZE // 2 - 8,
                5
            )

        ########################
        # Normal move          #
        ########################

        else:
            pygame.draw.circle(
                screen,
                pygame.Color("green"),
                (center_x, center_y),
                8
            )

########################
# Draw pieces          #
########################

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)

            if piece:
                ########################
                # White / black         #
                ########################

                color_prefix = (
                    "w"
                    if piece.color == chess.WHITE
                    else "b"
                )

                ########################
                # Pawn naming           #
                ########################

                if piece.piece_type == chess.PAWN:
                    key = color_prefix + "p"

                ########################
                # Other pieces          #
                ########################

                else:
                    key = color_prefix + piece.symbol().upper()

                ########################
                # Draw image            #
                ########################

                screen.blit(
                    pieces[key],
                    pygame.Rect(
                        c * SQ_SIZE,
                        r * SQ_SIZE,
                        SQ_SIZE,
                        SQ_SIZE
                    )
                )

########################
# Start program        #
########################

if __name__ == "__main__":
    main()