from ..game import ChessPiece

class Bishop(ChessPiece):
    
    """ This is the property of Bishop. The class adresses two functions:
        1. Finding available moves for Bishop
        2. Finding available capture for Bishop
        
        The class Bishop inherits a class ChessPiece
    """

    def available_moves(self, board):

        """ It finds available moves for bishop
            
            Parameters:
                board: instance of the current board
            
            Output:
                 possible moves: list(tuple(int, int))

        """

        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        color = self.color

        return board.get_linear_moves(self.position, directions, color)
    
    def available_captures(self, board):
        
        """ For Bishop available moves also allow capture in the same position
            if the piece is of opposite color
        """
        
        captures = []

        for pos in self.available_moves(board): # scan all positions
            piece = board.get_piece_at(pos)     # find if any pieces are in the way of available moves

            if piece is not None and piece.color != self.color: # check if there is capture
                captures.append(pos)

        return captures

