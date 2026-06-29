"""
board.py
Board cell representation class and coordinate helpers
"""


from __future__ import annotations
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True) # makes __init__ and stuff, frozen makes fields immutable
class Hex:
    """
    A board cell with coordinates (q, r).
    """

    q: int
    r: int

    @property # calculate s on demand instead of storing but access it like a field
    def s(self) -> int:
        return -self.q - self.r
    
    
