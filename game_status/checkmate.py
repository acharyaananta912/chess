class Checkmate:
    """Determines if the current player is checkmated."""

    def is_in_check(self, board, color):
        """Check if the king of a given color is under attack."""
        king = next(
            (p for p in board.pieces if p.__class__.__name__ == "King"
             and not p.is_captured and p.color == color),
            None
        )
        if not king:
            return False  # No king found — likely already game over

        king_pos = king.position
        opponent_color = "black" if color == "white" else "white"

        for piece in board.pieces:
            if piece.color == opponent_color and not piece.is_captured:
                if hasattr(piece, "available_captures") and king_pos in piece.available_captures(board):
                    return True
        return False

    def check_mate(self, board, color):
        """Return True if player of `color` is checkmated."""
        if not self.is_in_check(board, color):
            return False

        for piece in board.pieces:
            if piece.color != color or piece.is_captured:
                continue

            valid_moves = []
            if hasattr(piece, "available_moves"):
                valid_moves += piece.available_moves(board)
            if hasattr(piece, "available_captures"):
                valid_moves += piece.available_captures(board)

            for move in valid_moves:
                target = board.get_piece_at(move)
                if target and target.color == color:
                    continue  # can't capture own piece

                # Simulate move
                original_pos = piece.position
                target_was_captured = False
                if target and target.color != color:
                    target.is_captured = True
                    target_was_captured = True

                piece.position = move
                still_in_check = self.is_in_check(board, color)

                # Undo move
                piece.position = original_pos
                if target_was_captured:
                    target.is_captured = False

                if not still_in_check:
                    return False  # Found an escape move

        print(f"♚ Checkmate! {'Black' if color == 'white' else 'White'} wins!")
        board.status = "game-over"
        board.winner = "black" if color == "white" else "white"
        return True
