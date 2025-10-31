def get_jump_moves(self, position, jumps, color):

    """ This function is very similar to linear_move.py.
        Unlike it, this function does not continiously scan new position.
        This can be applied to Knight which can have only 4 jump moves possible.
        
        Parameters:
                position: Get current position of the chess piece.
                jumps: Gives potential moving direction of chess piece.
                color: Get information whether piece is Black or White.
        Output:
                moves: Possible moves for the chess piece.
                       Move may be invalid when King is in check.
    """

    moves = [] # initialize a list for possible moves
    x, y = position # this is the current position of the selected Knight

    for dx, dy in directions: # gets (x, y) coordinates from the jumps
        new_pos = (x + dx, y + dy) # calculating possible moves

        if self.is_valid_position(new_pos):
            piece = self.get_piece_at(new_pos) # info of piece at new calculated move

            if piece is None or piece.color != color: # is selected piece and piece at new position empty or different?
                    moves.append(new_pos)
                break

            moves.append(new_pos)
     
     return moves # return possible moves filtering out the positions where there is piece of same color

