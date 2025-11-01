def get_pawn_moves(self, position, color):
    
    """ This function handles pawn moves.
        Possible moves: One step
                        Two steps
                        Diagonal capture
        Parameters:
                position: position of the selected pawn. (tuple(int,int)
                color: Black or White (str)
        Output:
                moves: possible moves of the chess piece.
    """

    # Many comments are skipped as they are same as other functions in this directory.

    moves = []
    x, y = position
    direction = 1 if color == "white" else -1 # White: away from white Black: toward white
    one_step = (x, y + direction) # one step is vertical move
    
    if self._is_valid_position(one_step) and self.get_piece_at(one_step) is None: # empty square ahead
        moves.append(one_step) # one_step is a valid move

        start_row = 1 if color == "white" else 6 # initial position of pawns
        two_step = (x, y + 2 * direction) # can only go 2 step ahead

        # For two steps following 4 conditions must be met:
        # 1. Pawn should be in the initial position.
        # 2. One step ahead should be empty. (no jump)
        # 3. Two step ahead should be empty.

        if y == start_row and not self.get_piece_at(one_step) and not self.get_piece_at(two_step):
            moves.append(two_step) 
    
    return moves # returns one step and two step moves (if any)

def get_pawn_captures(self, position, color):
    x, y = position
    direction = 1 if color == "white" else -1
    captures = []
    
    for dx in (-1, 1):

        pos = (x + dx, y + direction)
        if self._is_valid_position(pos):

            piece = self.get_piece_at(pos)
            if piece and piece.color != color:
                if (pos[1] - y) * direction > 0:
                    captures.append(pos)
    return captures
