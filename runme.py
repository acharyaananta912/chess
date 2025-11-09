import pygame
from chess.gameplay import ChessBoard

# --- Config ---
TILE_SIZE = 80
BOARD_SIZE = 8
MARGIN_X = 120  # horizontal margin (left & right)
MARGIN_Y = 60   # vertical margin (top & bottom)
LIGHT = (240, 217, 181)
DARK = (60, 90, 150)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BLUE_HIGHLIGHT = (100, 149, 237, 120)   # bluish shadow
GRAY_OVERLAY   = (169, 169, 169, 150)   # for moves
GREEN_OVERLAY  = (50, 205, 50, 150)     # for captures
wrong_click_piece = None
wrong_click_timer = 0




# Board pixel dimensions
BOARD_WIDTH = TILE_SIZE * BOARD_SIZE
BOARD_HEIGHT = TILE_SIZE * BOARD_SIZE
WIDTH = BOARD_WIDTH + MARGIN_X * 2
HEIGHT = BOARD_HEIGHT + MARGIN_Y * 2 + 100

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess")

font_label = pygame.font.SysFont("Arial", 24)
font_piece = pygame.font.SysFont("Apple Symbols", 64)

# --- Init ---
# ... (other init code) ...

font_label = pygame.font.SysFont("Arial", 24)
font_piece = pygame.font.SysFont("Apple Symbols", 64)
# --- ADD THIS LINE ---
font_game_over = pygame.font.SysFont("Arial", 72, bold=True)


board = ChessBoard()
board.initialize_standard_board()

selected_piece = None
running = True

symbol_map = {
    "Pawn": {"white": "♟", "black": "♟"},
    "Rook": {"white": "♜", "black": "♜"},
    "Knight": {"white": "♞", "black": "♞"},
    "Bishop": {"white": "♝", "black": "♝"},
    "Queen": {"white": "♛", "black": "♛"},
    "King": {"white": "♚", "black": "♚"},
}

# --- Draw board ---

def draw_labels():
    """Draw A–H and 1–8 labels around the board."""
    cols = "ABCDEFGH"
    for i in range(BOARD_SIZE):
        # Column labels (top & bottom)
        letter = font_label.render(cols[i], True, BLACK)
        x = MARGIN_X + i * TILE_SIZE + TILE_SIZE // 2 - 8
        screen.blit(letter, (x, MARGIN_Y - 35))  # top
        screen.blit(letter, (x, MARGIN_Y + BOARD_HEIGHT + 5))  # bottom

        # Row labels (left & right)
        number = font_label.render(str(BOARD_SIZE - i), True, BLACK)
        y = MARGIN_Y + i * TILE_SIZE + TILE_SIZE // 2 - 10
        screen.blit(number, (MARGIN_X - 25, y))  # left
        screen.blit(number, (MARGIN_X + BOARD_WIDTH + 10, y))  # right

def draw_turn_indicator():
    """Draw a circle showing whose turn it is."""
    if board.turn == "white":
        cx, cy = WIDTH // 2, HEIGHT - 140
    else:
        cx, cy = WIDTH // 2, 40
    color = WHITE if board.turn == "white" else BLACK
    pygame.draw.circle(screen, color, (cx, cy), 10)
    # pygame.draw.circle(screen, GREY, (cx, cy), 15, 2)


def draw_captured():
    """Show captured pieces on the sides (white → right, black → left)."""
    spacing = TILE_SIZE * 0.8
    margin_x = TILE_SIZE * 0.3  # distance from board edge

    # Calculate starting positions
    y_start_white = MARGIN_Y + (BOARD_HEIGHT - spacing * 8) / 2
    y_start_black = MARGIN_Y + (BOARD_HEIGHT - spacing * 8) / 2

    # White captured → right side
    x_white = MARGIN_X + BOARD_WIDTH + TILE_SIZE * 0.3 + margin_x

    # Black captured → left side
    x_black = MARGIN_X - TILE_SIZE - margin_x

    # Draw captured pieces
    y_white, y_black = y_start_white, y_start_black
    for p in board.pieces:
        if getattr(p, "is_captured", False):
            sym = symbol_map[p.__class__.__name__][p.color]
            color = WHITE if p.color == "white" else BLACK
            text = font_piece.render(sym, True, color)

            if p.color == "white":
                screen.blit(text, (x_white, y_white))
                y_white += spacing
            else:
                screen.blit(text, (x_black, y_black))
                y_black += spacing



def draw_board():
    """Draw the chessboard and all pieces."""
    screen.fill(GREY)

    # Draw border
    pygame.draw.rect(
        screen, BLACK,
        (MARGIN_X - 3, MARGIN_Y - 3, BOARD_WIDTH + 6, BOARD_HEIGHT + 6),
        3
    )

    # Draw tiles
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            color = LIGHT if (x + y) % 2 == 0 else DARK
            rect = (MARGIN_X + x * TILE_SIZE, MARGIN_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

    highlight_squares(selected_piece)

    # Draw pieces
    for p in board.pieces:
        if getattr(p, "is_captured", False):
            continue
        x, y = p.position
        symbol = symbol_map[p.__class__.__name__][p.color]
        color = (255, 255, 255) if p.color == "white" else (0, 0, 0)
        text = font_piece.render(symbol, True, color)
        piece_pos = (MARGIN_X + x * TILE_SIZE + 20, MARGIN_Y + (7 - y) * TILE_SIZE + 10)
        screen.blit(text, piece_pos)

        # 🔴 Show red tint briefly for wrong click
        if wrong_click_piece == p and pygame.time.get_ticks() - wrong_click_timer < 600:
            overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 120))  # translucent red
            screen.blit(overlay, (MARGIN_X + x * TILE_SIZE, MARGIN_Y + (7 - y) * TILE_SIZE))


    # UI elements
    draw_labels()
    draw_turn_indicator()
    draw_captured()
    highlight_checked_kings()
    draw_game_over_message()


# --- Mouse position to board coordinate ---
def get_square_under_mouse(pos):
    """Convert mouse position (pixels) into board coordinates (x, y)."""
    x, y = pos

    # Adjust for margins
    board_x = (x - MARGIN_X) // TILE_SIZE
    board_y = 7 - ((y - MARGIN_Y) // TILE_SIZE)

    # Ensure within bounds
    if not (0 <= board_x < 8 and 0 <= board_y < 8):
        return None  # Click outside board area

    return (board_x, board_y)


def highlight_squares(selected_piece):
    legal_moves = board.get_legal_moves(selected_piece)

    """Highlight the selected piece, possible moves (green), and invalid ones due to check (red)."""
    if not selected_piece:
        return

    overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # --- Highlight selected piece square ---
    overlay.fill((100, 149, 237, 100))  # bluish tint
    x, y = selected_piece.position
    screen.blit(overlay, (MARGIN_X + x * TILE_SIZE, MARGIN_Y + (7 - y) * TILE_SIZE))

    # --- Gather all theoretical moves ---
    possible_moves = []
    if hasattr(selected_piece, "available_moves"):
        possible_moves += selected_piece.available_moves(board)
    if hasattr(selected_piece, "available_captures"):
        possible_moves += selected_piece.available_captures(board)

    # --- Filter legal moves ---
    legal_moves = board.get_legal_moves(selected_piece)

    for move in possible_moves:
        mx, my = move
        target = board.get_piece_at(move)

        # Determine legality and choose color
        if move in legal_moves:
            # ✅ Legal move — king remains safe
            color = (50, 205, 50, 150) if not target else (255, 215, 0, 150)  # green / gold capture
        else:
            # ❌ Invalid because it leaves king in check
            color = (255, 0, 0, 100)  # translucent red

        overlay.fill(color)
        screen.blit(overlay, (MARGIN_X + mx * TILE_SIZE, MARGIN_Y + (7 - my) * TILE_SIZE))


def highlight_checked_kings():
    """Highlight the king's tile red if that color is in check."""
    # Ask the board logic which side(s) are in check
    white_in_check = board.checked.is_in_check(board, "white")
    black_in_check = board.checked.is_in_check(board, "black")

    # Find each king on the board
    white_king = next(
        (p for p in board.pieces if p.__class__.__name__ == "King" and p.color == "white" and not p.is_captured),
        None
    )
    black_king = next(
        (p for p in board.pieces if p.__class__.__name__ == "King" and p.color == "black" and not p.is_captured),
        None
    )

    # Draw red overlay on the checked king’s tile
    overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    overlay.fill((255, 0, 0, 120))  # translucent red

    if white_in_check and white_king:
        x, y = white_king.position
        screen.blit(overlay, (MARGIN_X + x * TILE_SIZE, MARGIN_Y + (7 - y) * TILE_SIZE))

    if black_in_check and black_king:
        x, y = black_king.position
        screen.blit(overlay, (MARGIN_X + x * TILE_SIZE, MARGIN_Y + (7 - y) * TILE_SIZE))

def draw_game_over_message():
    """If the game is over, draw an overlay and the result text."""
    
    # Do nothing if the game is still in progress
    if board.status == "in-progress":
        return

    # Create a dark, semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 180))  # RGBA: Dark gray, 180/255 opacity
    screen.blit(overlay, (0, 0))

    # Determine the message
    message = ""
    if board.status == "game-over":
        winner = board.winner.title()
        message = f"Checkmate! {winner} Wins!"
    elif board.status == "stalemate":
        message = "Stalemate! It's a Draw."

    # Render and center the text
    text = font_game_over.render(message, True, WHITE) # White text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)


# --- Main Loop ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            coord = get_square_under_mouse(pos)
            if coord is None:
                continue

            if selected_piece:
                if hasattr(board, "move_piece") and board.move_piece(selected_piece.position, coord):
                    selected_piece = None
                else:
                    selected_piece = None
            else:
                piece = board.get_piece_at(coord)
                if piece and not getattr(piece, "is_captured", False):
                    if piece.color != board.turn:
                        wrong_click_piece = piece
                        wrong_click_timer = pygame.time.get_ticks()
                        print(f"⚠️ It's {board.turn}'s turn! You clicked {piece.color}.")
                    else:
                        selected_piece = piece


    draw_board()
    pygame.display.flip()

pygame.quit()
