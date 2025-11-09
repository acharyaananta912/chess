from ..game import ChessPiece

class King(ChessPiece):

    """
       This represents a King.
    """
    
    def available_moves(self, board):

        """King can move one square in any direction, plus possible castling."""

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]

        step_moves = board.get_step_moves(self.position, directions, self.color)

        # Add castling moves if available

        castling_moves = []

        if hasattr(board, "get_castling_moves"):
            castling_moves = board.get_castling_moves(self.position, self.color)

        return step_moves + castling_moves

    def available_captures(self, board):

        """ 
           This function returns available captures for the King
        """

        captures = []

        for pos in self.available_moves(board): # scan all positions
             piece = board.get_piece_at(pos)    # find if any pieces are in the way of available moves
             
             if piece is not None and piece.color != self.color: # check if there is capture
                captures.append(pos)        

        return captures
