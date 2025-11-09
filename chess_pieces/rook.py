from ..game import ChessPiece

class Rook(ChessPiece):

    """Represents a rook piece."""

    def available_moves(self, board):

        """
           This function returns available moves for the Rook 
        """

        directions=[(1,0), (-1,0), (0,1), (0,-1)]

        return board.get_linear_moves(self.position, directions, self.color)

    def available_captures(self, board):

        """ 
           This function returns available captures for the Rook
        """

        captures = []

        for pos in self.available_moves(board): # scan all positions
             piece = board.get_piece_at(pos)    # find if any pieces are in the way of available moves
             
             if piece is not None and piece.color != self.color: # check if there is capture
                captures.append(pos)        

        return captures

