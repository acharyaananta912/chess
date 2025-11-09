from abc import ABC, abstractmethod

class ChessPiece(ABC):
    
    """ Class for all the chess pieces."""
    
    def __init__(self, color, position):
        
        self._color = color
        self._position = position
        self._is_captured = False
        self._has_moved = False

    @property
    def color(self):
        return self._color

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def has_moved(self):
        return self._has_moved

    @property
    def is_captured(self):
        return self._is_captured

    @is_captured.setter
    def is_captured(self, value):
        self._is_captured = bool(value)

    @abstractmethod
    def available_moves(self, board):
        pass

    @abstractmethod
    def available_captures(self, board):
        pass

    def move(self, new_position):

        """ Moves the piece to a new position """

        self.position = new_position
        self._has_moved = True
