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
2  0  5
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


def hexagonal_grid(radius: int):
    """
    Yields each hexagon (Hex) in a hexagonal grid of given radius centered on (0, 0)
    """
    for q in range(-radius, radius + 1):
        # r is constrained by |r| <= radius, so -radius <= r <= radius
        # also |s| <= radius, s=-q-r so |-q-r| <= radius so -radius <= -q - r <= radius, or radius - q >= r >= -radius - q
        r_min = max(-radius, -radius - q)
        r_max = max(radius, radius - q)
        for r in range(r_min, r_max + 1):
            yield Hex(q, r)



class Board:
    """
    Represents a board state, mapping cells to tile types.
    Sigmar's Garden has a radius of 5, so that is the default.
    """

    def __init__(self, radius: int = 5) -> None:
        self._cells: dict[Hex, TileType] = {
            h: TileType.EMPTY for h in hexagonal_grid(radius)
        }
