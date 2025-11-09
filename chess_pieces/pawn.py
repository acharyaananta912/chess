from ..game import ChessPiece

class Pawn(ChessPiece):
    """Represents a pawn piece."""

    def available_moves(self, board):
        
        """ 
           This functions returns available moves for the pawn
        """

        return board.get_pawn_moves(self.position, self.color)

    def available_captures(self, board):

        """ 
           This functions returns available captures for the pawn
        """

        return board.get_pawn_captures(self.position, self.color)
