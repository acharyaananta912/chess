from .linear_move import get_linear_moves
from .step_move import get_step_moves
from .jump_move import get_jump_moves
from .pawn_move import get_pawn_moves, get_pawn_captures
from .castling_move import get_castling_moves

class ValidMoves:
    def __init__(self, get_piece_func):
        self.get_piece_at = get_piece_func

    def _is_valid_position(self, position):
        x, y = position
        return 0 <= x < 8 and 0 <= y < 8

    def get_linear_moves(self, position, directions, color):
        return get_linear_moves(self, position, directions, color)

    def get_step_moves(self, position, directions, color):
        return get_step_moves(self, position, directions, color)

    def get_jump_moves(self, position, jumps, color):
        return get_jump_moves(self, position, jumps, color)

    def get_pawn_moves(self, position, color):
        return get_pawn_moves(self, position, color)

    def get_pawn_captures(self, position, color):
        return get_pawn_captures(self, position, color)

    def get_castling_moves(self, position, color):
        return get_castling_moves(self, position, color)