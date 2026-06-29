"""
board.py
Board cell representation class and coordinate helpers
"""


from __future__ import annotations
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum, auto


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
    
    def distance(self, other: Hex) -> int:
        d = self - other
        return max(abs(d.q), abs(d.r), abs(d.s))
    
    def neighbors(self) -> list[Hex]:
        return [self + d for d in AXIAL_DIRECTIONS]
    
    def neighbor(self, direction: int) -> Hex:
        return self + AXIAL_DIRECTIONS[direction % 6]


"""
  3 4
2  S  5
  1 6
The six axial directions as Hex's that can be added to a Hex to find cells 1 unit away in each direction.
They are arranged in order, so consecutive entries correspond to consecutive neighboring cells.
"""
AXIAL_DIRECTIONS: tuple[Hex, ...] = (
    Hex(1, 0), # 1
    Hex(1, -1),
    Hex(0, -1),
    Hex(-1, 0),
    Hex(-1, 1),
    Hex(0, 1) # 6
)


class TileType(Enum):
    """
    The possible types of spaces, including empty
    """
    AIR = auto()
    FIRE = auto()
    WATER = auto()
    EARTH = auto()
    SALT = auto()
 
    VITAE = auto()
    MORS = auto()
 
    QUICKSILVER = auto()
    LEAD = auto()
    TIN = auto()
    IRON = auto()
    COPPER = auto()
    SILVER = auto()
    GOLD = auto()

    EMPTY = auto()


# The four cardinal elements as a set
ELEMENTS: frozenset[TileType] = frozenset(
    {TileType.AIR, TileType.FIRE, TileType.WATER, TileType.EARTH}
)


# The metals in the order that they have to be matched
METAL_SEQUENCE: tuple[TileType, ...] = (
    TileType.LEAD,
    TileType.TIN,
    TileType.IRON,
    TileType.COPPER,
    TileType.SILVER,
    TileType.GOLD
)