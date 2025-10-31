def get_linear_moves(self, position, directions, color):

    """ This function is for linear movement of chess pieces 
        (e.g. Queen, Rook, and Bishop). The move can be straight
        or diagonal depending on the directions argument.
        
        Parameters:
                position: Get current position of the chess piece.
                directions: Gives potential moving direction of chess piece.
                color: Get information whether piece is Black or White.
        Output:
                moves: Possible moves for the chess piece.
                       Move may be invalid when King is in check.
    """

    moves = [] # initialize a list for possible moves

    for dx, dy in directions: # gets (x, y) coordinates from the directions
        x, y = position # this is position of chess piece

        while self.is_valid_position((x + dx, y + dy)):  # ******Discuss Later****
            x += dx # calculating possible move
            y += dy

            piece = self.get_piece_at((x, y)) # info of piece at new calculated move

            if piece: # if there is piece go through condition otherwise add it as valid move
                if piece.color.color != color: # is selected piece and piece at new position different?
                    moves.append((x, y)) # the move is valid (possible capture move)
                break

            moves.append((x,y))
     
     return moves # return possible moves filtering out the positions where there is piece of same color
