class Checked:
    """
    Checks if a king is currently under attack (in check) after any move.
    """

    def is_in_check(self, board, color):
        """
        Returns True if the king of the given color is in check.
        """
        # Find the king of the given color
        king = next(
            (p for p in board.pieces
             if p.__class__.__name__ == "King"
             and not getattr(p, "is_captured", False)
             and p.color == color),
            None
        )

        if not king:
            return False  # No king found (already captured)

        king_pos = king.position
        opponent_color = "black" if color == "white" else "white"

        # Check all opponent pieces to see if they attack the king
        for piece in board.pieces:
            if piece.color == opponent_color and not getattr(piece, "is_captured", False):
                if hasattr(piece, "available_captures"):
                    captures = piece.available_captures(board)
                    if king_pos in captures:
                        print(f"⚠️  {color.capitalize()} King is in check by {piece.__class__.__name__} at {piece.position}")
                        return True
        return False

    def check_both_kings(self, board):
        """
        Checks both kings after any move — useful right after a piece moves.
        """
        white_in_check = self.is_in_check(board, "white")
        black_in_check = self.is_in_check(board, "black")

        if not white_in_check and not black_in_check:
            print("✅ No kings are currently in check.")
        return white_in_check, black_in_check
