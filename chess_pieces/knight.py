from ..game import ChessPiece

class Knight(ChessPiece):

    """Represents a queen piece."""

    def available_moves(self, board):

        """ This function returns available moves for the Knight
        """
        directions = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]

        return board.get_jump_moves(self.position, directions, self.color)

    def available_captures(self, board):

        """ 
           This function returns available captures for the Knight
        """

        captures = []

        for pos in self.available_moves(board): # scan all positions
             piece = board.get_piece_at(pos)    # find if any pieces are in the way of available moves
             
             if piece is not None and piece.color != self.color: # check if there is capture
                captures.append(pos)        

        return captures
