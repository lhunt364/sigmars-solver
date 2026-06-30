"""
game.py
Matching and valid move logic
"""

from __future__ import annotations
from dataclasses import dataclass
from board import TileType, ELEMENTS

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
    
    