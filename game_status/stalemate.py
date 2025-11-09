# game_state/stalemate.py
from .checkmate import Checkmate

class Stalemate(Checkmate):
    """Determines if the game is a stalemate (no legal moves but not in check)."""

    def stalemate(self, board, color):
        """Return True if color is NOT in check but has no legal moves."""
        if self.is_in_check(board, color):
            return False  # If in check, not stalemate

        for piece in board.pieces:
            if piece.color == color and not piece.is_captured:
                valid_moves = []
                if hasattr(piece, "available_moves"):
                    valid_moves += piece.available_moves(board)
                if hasattr(piece, "available_captures"):
                    valid_moves += piece.available_captures(board)

                for move in valid_moves:
                    original_pos = piece.position
                    target = board.get_piece_at(move)
                    piece.position = move
                    if target:
                        target.is_captured = True

                    still_in_check = self.is_in_check(board, color)

                    piece.position = original_pos
                    if target:
                        target.is_captured = False

                    if not still_in_check:
                        return False  # Has a legal move, not stalemate

        print("🤝 Stalemate! It's a draw.")
        board.status = "game-over"
        board.winner = None
        return True

