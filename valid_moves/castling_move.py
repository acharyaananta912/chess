def get_castling_moves(self, position, color):

    """ This function allows castling between Rook and King.
        Conditions to be met:
            1. No King and Rook (the one trying to castle) movement.
            2. Squares between King and Rook should be empty.
            3. Two castling possible: (a) Queen side (b) King side

        Parameters:
            position: position of the King or Rook
            color: Black or White

        Output: 
             moves: possible moves for the castling
    """
    
    moves = []
    x, y = position

    king = self.get_piece_at(position) # position of the king

    # Checking condition 1 (Has king moved?)
    if (
        not king
        or king.__class__.__name__ != "King"
        or king.color != color
        or king.has_moved
        ):

        return moves                   # empty

    # Checking condition 2 for kingside castling (Has rook moved?)
    rook = self.get_piece_at((7, y)) # find rook on kings side
    if (
        rook
        and rook.__class__.__name__ == "Rook"
        and rook.color == color
        and not rook.has_moved
        ):
       
        # Checking condition 2 (Are spaces empty?)
        if all(self.get_piece_at((x_i, y)) is None for x_i in (5, 6)):
            moves.append((6, y))

    # Checking condition 1 for queenside castling (Has rook moved?)
    rook = self.get_piece_at((0, y))
    if (
        rook 
        and rook.__class__.__name__ == "Rook"
        and rook.color == color
        and not rook.has_moved
        ):
    
        # Checking condition 2 (Are spaces empty?)
        if all(self.get_piece_at((x_i, y)) is None for x_i in (1, 2, 3)):
            moves.append((2, y))
    
    return moves
