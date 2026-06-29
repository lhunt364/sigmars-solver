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
    
    def __add__(self, other: Hex) -> Hex:
        return Hex(self.q + other.q, self.r + other.r)
    
    def __sub__(self, other: Hex) -> Hex:
        return Hex(self.q - other.q, self.r - other.r)


"""
  3 4
2  S  5
  1 6
The six axial directions as Hex's that can be added to Hex to find cells 1 unit away in each direction.
They are arranged in order, so consecutive entries correspond to consecutive neighboring cells.
"""
AXIAL_DIRECTIONS: tuple[Hex, ...] = (
    Hex(1, 0), # 1
    Hex(1, -1),
    Hex(0, -1),
    Hex(-1, 0),
    Hex(-1, 1),
    Hex(0, 1), # 6
)
