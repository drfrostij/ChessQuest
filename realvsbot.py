##############################
# Importing from other files #
##############################

import pygame
import chess
import chess.engine

from soundimagedatabase import sound, pieces


import pygame
import chess
import chess.engine
from soundimagedatabase import sound, pieces

# SETTINGS
WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 60

STOCKFISH_PATH = (
    r"C:\Users\moses_phub\Downloads\Archives\extrra unwanted"
    r"\stockfish-windows-x86-64-avx2\stockfish"
    r"\stockfish-windows-x86-64-avx2.exe"
)

# COLOURS
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED_COLOUR = (255, 255, 0)
LEGAL_MOVE_COLOUR = (80, 200, 80)
POPUP_BACKGROUND = (40, 40, 40)
POPUP_TEXT = (255, 255, 255)

# DRAW BOARD
def draw_board(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            colour = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, colour, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# DRAW PIECES
def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)
        piece_name = "w" if piece.color == chess.WHITE else "b"
        piece_name += piece.symbol().upper()
        if piece.piece_type == chess.PAWN:
            piece_name = piece_name[0] + "p"
        image = pygame.transform.smoothscale(pieces[piece_name], (SQ_SIZE, SQ_SIZE))
        screen.blit(image, (col * SQ_SIZE, row * SQ_SIZE))

# DRAW LEGAL MOVES
def draw_legal_moves(screen, board, selected_square):
    if selected_square is None:
        return
    for move in board.legal_moves:
        if move.from_square != selected_square:
            continue
        row = 7 - chess.square_rank(move.to_square)
        col = chess.square_file(move.to_square)
        centre = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
        pygame.draw.circle(screen, LEGAL_MOVE_COLOUR, centre, 10)

# HIGHLIGHT SELECTED SQUARE
def draw_selected_square(screen, selected_square):
    if selected_square is None:
        return
    row = 7 - chess.square_rank(selected_square)
    col = chess.square_file(selected_square)
    pygame.draw.rect(screen, SELECTED_COLOUR, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 4)

# GET SQUARE FROM MOUSE
def get_square_from_mouse(pos):
    x, y = pos
    col = x // SQ_SIZE
    row = y // SQ_SIZE
    if not (0 <= col < 8 and 0 <= row < 8):
        return None
    return chess.square(col, 7 - row)

# PROMOTION POPUP
def promotion_popup(screen, board, move):
    options = [
        (chess.QUEEN, "Queen"),
        (chess.ROOK, "Rook"),
        (chess.BISHOP, "Bishop"),
        (chess.KNIGHT, "Knight")
    ]
    popup_width = 300
    popup_height = 240
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    font = pygame.font.SysFont(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for index, (piece_type, name) in enumerate(options):
                    button_y = popup_y + 45 + index * 45
                    button_rect = pygame.Rect(popup_x + 25, button_y, popup_width - 50, 35)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        promotion_move = chess.Move(move.from_square, move.to_square, promotion=piece_type)
                        if promotion_move in board.legal_moves:
                            return promotion_move

        draw_board(screen)
        draw_pieces(screen, board)
        pygame.draw.rect(screen, POPUP_BACKGROUND, pygame.Rect(popup_x, popup_y, popup_width, popup_height))
        title = font.render("Choose Promotion", True, POPUP_TEXT)
        screen.blit(title, (popup_x + 65, popup_y + 10))

        for index, (_, name) in enumerate(options):
            button_rect = pygame.Rect(popup_x + 25, popup_y + 45 + index * 45, popup_width - 50, 35)
            pygame.draw.rect(screen, (80, 80, 80), button_rect)
            text = font.render(name, True, POPUP_TEXT)
            screen.blit(text, (button_rect.x + 10, button_rect.y + 5))

        pygame.display.flip()

# CHECKMATE POPUP
def checkmate_popup(screen, board):
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)
    winner = "Black wins!" if board.turn == chess.WHITE else "White wins!"
    popup_width = 320
    popup_height = 180
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                reset_button = pygame.Rect(popup_x + 25, popup_y + 105, 120, 40)
                quit_button = pygame.Rect(popup_x + 175, popup_y + 105, 120, 40)
                if reset_button.collidepoint(x, y):
                    return "reset"
                if quit_button.collidepoint(x, y):
                    return "quit"

        draw_board(screen)
        draw_pieces(screen, board)
        pygame.draw.rect(screen, POPUP_BACKGROUND, pygame.Rect(popup_x, popup_y, popup_width, popup_height))

        title = font.render("Checkmate!", True, POPUP_TEXT)
        winner_text = small_font.render(winner, True, POPUP_TEXT)
        screen.blit(title, (popup_x + 100, popup_y + 15))
        screen.blit(winner_text, (popup_x + 115, popup_y + 55))

        reset_button = pygame.Rect(popup_x + 25, popup_y + 105, 120, 40)
        quit_button = pygame.Rect(popup_x + 175, popup_y + 105, 120, 40)

        pygame.draw.rect(screen, (80, 80, 80), reset_button)
        pygame.draw.rect(screen, (80, 80, 80), quit_button)

        reset_text = small_font.render("Reset", True, POPUP_TEXT)
        quit_text = small_font.render("Quit", True, POPUP_TEXT)

        screen.blit(reset_text, (reset_button.x + 35, reset_button.y + 7))
        screen.blit(quit_text, (quit_button.x + 40, quit_button.y + 7))
        pygame.display.flip()

# ENGINE SETTINGS
def get_engine_settings(chessbot_elo):
    if chessbot_elo >= 1320:
        return {
            "UCI_LimitStrength": True,
            "UCI_Elo": chessbot_elo,
            "search_time": 0.5
        }

    if chessbot_elo <= 300:
        search_time = 0.03
    elif chessbot_elo <= 500:
        search_time = 0.05
    elif chessbot_elo <= 700:
        search_time = 0.08
    elif chessbot_elo <= 900:
        search_time = 0.12
    elif chessbot_elo <= 1100:
        search_time = 0.18
    else:
        search_time = 0.25

    return {
        "UCI_LimitStrength": True,
        "UCI_Elo": 1320,
        "search_time": search_time
    }

# CHESSBOT MOVE
def get_bot_move(engine, board, chessbot_elo):
    settings = get_engine_settings(chessbot_elo)
    result = engine.play(board, chess.engine.Limit(time=settings["search_time"]))
    return result.move

# MAIN GAME
def main(chessbot_elo):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"ChessQuest - ChessBot {chessbot_elo} Elo")
    clock = pygame.time.Clock()
    board = chess.Board()
    selected_square = None
    player_colour = chess.WHITE
    engine = None

    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        settings = get_engine_settings(chessbot_elo)
        engine.configure({
            "UCI_LimitStrength": settings["UCI_LimitStrength"],
            "UCI_Elo": settings["UCI_Elo"]
        })

        sound["game_start"].play()
        running = True

        while running:
            clock.tick(MAX_FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and board.turn == player_colour and not board.is_game_over():
                    clicked_square = get_square_from_mouse(event.pos)

                    if clicked_square is None:
                        continue

                    if selected_square is None:
                        piece = board.piece_at(clicked_square)
                        if piece is not None and piece.color == player_colour:
                            selected_square = clicked_square

                    else:
                        piece = board.piece_at(clicked_square)

                        if piece is not None and piece.color == player_colour:
                            selected_square = clicked_square
                            continue

                        move = chess.Move(selected_square, clicked_square)

                        if board.piece_at(selected_square).piece_type == chess.PAWN and chess.square_rank(clicked_square) in (0, 7):
                            promotion_move = chess.Move(selected_square, clicked_square, promotion=chess.QUEEN)

                            if promotion_move in board.legal_moves:
                                selected_square = None
                                move = promotion_popup(screen, board, move)

                                if move is None:
                                    continue

                                board.push(move)
                                sound["promote"].play()

                                if board.is_check():
                                    sound["move-check"].play()

                                continue

                        if move in board.legal_moves:
                            is_capture = board.is_capture(move)
                            is_castle = board.is_castling(move)
                            board.push(move)
                            selected_square = None

                            if is_castle:
                                sound["castle"].play()
                            elif is_capture:
                                sound["capture"].play()
                            else:
                                sound["move-self"].play()

                            if board.is_check():
                                sound["move-check"].play()
                        else:
                            sound["illegal"].play()
                            selected_square = None

            if board.turn != player_colour and not board.is_game_over():
                pygame.event.pump()
                bot_move = get_bot_move(engine, board, chessbot_elo)
                is_capture = board.is_capture(bot_move)
                is_castle = board.is_castling(bot_move)
                is_promotion = bot_move.promotion is not None
                board.push(bot_move)

                if is_promotion:
                    sound["promote"].play()
                elif is_castle:
                    sound["castle"].play()
                elif is_capture:
                    sound["capture"].play()
                else:
                    sound["move-opponent"].play()

                if board.is_check():
                    sound["move-check"].play()

            draw_board(screen)
            draw_selected_square(screen, selected_square)
            draw_legal_moves(screen, board, selected_square)
            draw_pieces(screen, board)
            pygame.display.flip()

            if board.is_checkmate():
                sound["game-end"].play()
                result = checkmate_popup(screen, board)

                if result == "reset":
                    board.reset()
                    selected_square = None
                    sound["game_start"].play()
                elif result == "quit":
                    running = False

    finally:
        if engine is not None:
            try:
                engine.quit()
            except Exception:
                pass
        pygame.quit()

if __name__ == "__main__":
    main(1000)