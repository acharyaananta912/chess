from dataclasses import dataclass, field
from typing import List

@dataclass
class Player:

    """Represents a chess player."""

    name: str
    color: str  # should be "white" or "black"
    pieces: List['ChessPiece'] = field(default_factory=list)
    captured_pieces: List['ChessPiece'] = field(default_factory=list)
    _is_winner: bool = field(default=False, init=False, repr=False)

    def __post_init__(self):
        if self.color not in ("white", "black"):
            raise ValueError("Player color must be 'white' or 'black'")

    @property
    def is_winner(self) -> bool:
        return self._is_winner

    @is_winner.setter
    def is_winner(self, value: bool):
        self._is_winner = bool(value)

    def add_piece(self, piece: 'ChessPiece') -> None:
        """Register a piece as belonging to this player."""
        self.pieces.append(piece)

    def capture_piece(self, piece: 'ChessPiece') -> None:
        """Record that this player has captured `piece`."""
        piece.is_captured = True
        self.captured_pieces.append(piece)
