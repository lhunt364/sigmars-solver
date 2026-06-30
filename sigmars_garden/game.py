"""
game.py
Matching and valid move logic
"""

from __future__ import annotations
from dataclasses import dataclass
from board import TileType, ELEMENTS, Board, METAL_SEQUENCE, Hex

def is_pair_match(a: TileType, b: TileType, current_metal: TileType | None) -> bool:
    """
    Returns true if cells of type a and b make a valid pair that can be removed right now (assuming they are unblocked) given the currently free metal
    """
    # same element + same element
    if a in ELEMENTS and a is b:
        return True
    # salt + element or also salt
    if a is TileType.SALT and (b in ELEMENTS or b is TileType.SALT):
        return True
    if b is TileType.SALT and (a in ELEMENTS or a is TileType.SALT):
        return True
    # vitae + mors
    if {a, b} == {TileType.VITAE, TileType.MORS}:
        return True
    # quicksilver + current metal
    if current_metal is not None and current_metal is not TileType.GOLD and {a, b} == {TileType.QUICKSILVER, current_metal}:
        return True
    return False


@dataclass
class _Undo:
    """
    A receipt made when a move is applied.
    It contains the (Hex, TileType) pairs removed and what the metal index was prior in order to undo the move
    """
    removed: list[tuple[Hex, TileType]]
    metal_index: int


@dataclass
class Move:
    """
    A legal move; a pair of cells that can be removed legally (they match and are unblocked).
    Gold is the exception, being removable when the other metals are gone, so a Move can also just have one Hex, the gold
    """

    hexes: tuple[Hex, ...]

    @classmethod
    def pair(cls, a: Hex, b: Hex) -> Move:
        return cls(tuple(sorted((a, b), key=lambda h: (h.q, h.r))))
    
    @classmethod
    def single(cls, g: Hex) -> Move:
        return cls((g,))


class GameState:
    """
    Tracks the board (using a Board) and the metal sequence
    """

    def __init__(self, board: Board) -> None:
        self.board = board
        self._current_metal_index = 0 # index of the current metal in METAL_SEQUENCE

    @property
    def current_metal(self) -> TileType | None:
        """
        Returns the current metal to be removed or None if all have been removed
        """
        if self._current_metal_index < len(METAL_SEQUENCE):
            return METAL_SEQUENCE[self._current_metal_index]
        return None
    
    def legal_moves(self) -> list[Move]:
        """
        Lists every currently legal move
        """
        pass

    def apply(self, move: Move) -> _Undo:
        """
        Applies the given move, emptying the given cells and advancing the current metal index if a metal was removed
        """
        pass

    def undo(self, receipt: _Undo) -> None:
        """
        Undoes the move corresponding to the given receipt information
        """
        pass

    def is_complete(self) -> bool:
        """
        Returns true if the board is empty
        """
        return self.board.non_empty_count() == 0
    