# Main ChessBoard Class


from chess.chess_pieces import Bishop, Rook, Knight, Queen, King, Pawn
from chess.valid_moves import ValidMoves
from chess.player import Player
from chess.game_status import Checkmate, Stalemate, Checked


class ChessBoard(ValidMoves):

    """
       1. This class initializes board and setup.
       2. Move pieces
       3. Check game status (Running, Checked, Checkedmate, Stalemate)
    """
    
    def __init__(self):
        
        super().__init__(self.get_piece_at)
        self.pieces = []
        self.players = []
        self.status = "in-progress"
        self.turn = "white"
        self.winner = None

        self.checkmate = Checkmate()
        self.stalemate = Stalemate()
        self.checked = Checked()
        self.en_passant_target = None

# ****************************************************************************

    def initialize_standard_board(self):
        
        """Generate the standard board"""
        
        self.pieces = self._generate_initial_setup()

# *****************************************************************************

    def _generate_initial_setup(self):
        pieces = []

        color = "black"
        pieces += [
            Rook(color, (0, 7)), Knight(color, (1, 7)), Bishop(color, (2, 7)),
            Queen(color, (3, 7)), King(color, (4, 7)),
            Bishop(color, (5, 7)), Knight(color, (6, 7)), Rook(color, (7, 7))
        ]
        for x in range(8):
            pieces.append(Pawn(color, (x, 6)))

        # White pieces
        color = "white"
        pieces += [
            Rook(color, (0, 0)), Knight(color, (1, 0)), Bishop(color, (2, 0)),
            Queen(color, (3, 0)), King(color, (4, 0)),
            Bishop(color, (5, 0)), Knight(color, (6, 0)), Rook(color, (7, 0))
        ]
        for x in range(8):
            pieces.append(Pawn(color, (x, 1)))

        return pieces

# *****************************************************************************

    def get_piece_at(self, position):
        
        """ Get the piece at the given postion."""

        for p in self.pieces:
            if not p.is_captured and p.position == position:
                return p
        return None

# *****************************************************************************

    def is_square_attacked(self, position, color):
        
        """Return True: opponent attack the given square"""
    
        opponent_color = "black" if color == "white" else "white"
        for piece in self.pieces:
            if piece.color == opponent_color and not piece.is_captured:
                if position in piece.available_captures(self):
                    return True
        return False

# ****************************************************************************

    def get_legal_moves(self, piece):

        if piece is None or piece.is_captured:
            return []
        
        legal_moves = []
        possible = []
        
        possible += piece.available_moves(self)
        possible += piece.available_captures(self)

        for move in possible:
            original_pos = piece.position
            target = self.get_piece_at(move)
            captured_piece = None

            if target and target.color != piece.color:
                target.is_captured = True
                captured_piece = target

            piece.position = move

            if not self.checked.is_in_check(self, piece.color):
                legal_moves.append(move)

            # undo move
            piece.position = original_pos
            if captured_piece:
                captured_piece.is_captured = False

        return legal_moves

# ***************************************************************************

    def _check_for_game_end(self):
    
        current_color = self.turn
        in_check = self.checked.is_in_check(self, current_color)

        has_any_move = False
        for piece in self.pieces:
            if piece.color != current_color or piece.is_captured:
                continue
            if self.get_legal_moves(piece):
                has_any_move = True
                break

        if not has_any_move:
            if in_check:
                self.status = "game-over"
                self.winner = "black" if current_color == "white" else "white"
            else:
                self.status = "stalemate"

# ****************************************************************************

    def move_piece(self, start_pos, end_pos):
        """
        Attempt to move the piece at `start_pos` to `end_pos`.
        Returns True if the move succeeds, False otherwise.
        """
        piece = self.get_piece_at(start_pos)
        if not piece:
            return False
        if piece.color != self.turn:
            return False

        # gather possible moves
        possible: List[Tuple[int, int]] = []
        possible += piece.available_moves(self)
        possible += piece.available_captures(self)

        # include castling moves for kings
        castle_moves: List[Tuple[int, int]] = []
        if isinstance(piece, King):
            castle_moves = self.get_castling_moves(start_pos, piece.color)

        # if end_pos is not legal
        if end_pos not in possible + castle_moves:
            return False

        # castling logic
        if isinstance(piece, King) and abs(end_pos[0] - start_pos[0]) == 2:
            if self.checkmate.is_in_check(self, piece.color):
                return False

            sx, sy = start_pos
            ex, ey = end_pos
            # kingside
            if ex - sx == 2:
                rook = self.get_piece_at((7, sy))
                if (rook and isinstance(rook, Rook) and not rook.has_moved and
                        all(self.get_piece_at((x, sy)) is None for x in (5, 6)) and
                        not any(self.is_square_attacked((x, sy), piece.color) for x in (5, 6))):
                    rook.move((5, sy))
                else:
                    return False
            # queenside
            elif ex - sx == -2:
                rook = self.get_piece_at((0, sy))
                if (rook and isinstance(rook, Rook) and not rook.has_moved and
                        all(self.get_piece_at((x, sy)) is None for x in (1, 2, 3)) and
                        not any(self.is_square_attacked((x, sy), piece.color) for x in (2, 3))):
                    rook.move((3, sy))
                else:
                    return False

        # simulate move to ensure the king isn't left in check
        original_pos = piece.position
        target = self.get_piece_at(end_pos)
        captured_piece: Optional[ChessPiece] = None
        if target and target.color != piece.color:
            target.is_captured = True
            captured_piece = target

        piece.position = end_pos
        in_check = self.checked.is_in_check(self, piece.color)

        if in_check:
            piece.position = original_pos
            if captured_piece:
                captured_piece.is_captured = False
            return False



        # en-passant capture
        if isinstance(piece, Pawn) and end_pos == self.en_passant_target:
            x, y = end_pos
            direction = -1 if piece.color == "white" else 1
            captured_pos = (x, y + direction)
            captured_pawn = self.get_piece_at(captured_pos)
            if captured_pawn:
                captured_pawn.is_captured = True


        # finalize move
        piece.move(end_pos)  # sets _has_moved = True

        # en-passant target
        self.en_passant_target = None
        if isinstance(piece, Pawn):
            sx, sy = start_pos
            ex, ey = end_pos
            if piece.color == "white" and sy == 1 and ey == 3:
                self.en_passant_target = (ex, 2)
            elif piece.color == "black" and sy == 6 and ey == 4:
                self.en_passant_target = (ex, 5)


        if isinstance(piece, Pawn): #Pawn Promotion
            x, y = end_pos
            if piece.color == "white" and y == 7:
                self._promote_pawn_to_queen(piece)

            elif piece.color == "black" and y == 0:
                self._promote_pawn_to_queen(piece)

        self.turn = "black" if self.turn == "white" else "white"
        self.checked.check_both_kings(self)
        self._check_for_game_end()
        return True

# **********************************************************************************
    def _promote_pawn_to_queen(self, pawn):

        """ This helps to promote the pawn to queen if the pawn
        reaches the other end. """

        px, py = pawn.position
        color = pawn.color 

        pawn.is_captured = True # pawn is removed

        new_piece = Queen(color, (px, py))
        self.pieces.append(new_piece)



# ******************************** END *********************************************
