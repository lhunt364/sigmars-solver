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

    def place(self, hex: Hex, tile: TileType) -> None:
        if hex not in self._cells:
            raise ValueError(f"{hex} is outside of board")
        self._cells[hex] = tile
    
    def remove(self, hex: Hex) -> TileType:
        """
        Empties given cell and returns the type of tile that was there
        """
        if hex not in self._cells:
            raise ValueError(f"{hex} is outside of board")
        old_type = self._cells[hex]
        self._cells[hex] = TileType.EMPTY
        return old_type
    
    def is_empty(self, hex: Hex) -> bool:
        return self._cells[hex] is TileType.EMPTY
    
    def is_non_blocking(self, hex: Hex) -> bool:
        """
        Returns true if the cell is empty or if it's off the board
        """
        return self._cells.get(hex, TileType.EMPTY) is TileType.EMPTY
    
    def is_unblocked(self, hex: Hex) -> bool:
        """
        Checks if given cell has three consecutive empty neighboring cells and therefore is unblocked from being removed
        """
        run = 0
        nbrs = [self.is_non_blocking(n) for n in hex.neighbors()]
        for n in nbrs + nbrs: # wrap the neighbors so ..4501.. is continuous
            if n: # if cell is empty or off board then continue run, otherwise reset it
                run += 1
            else:
                run = 0
            if run >= 3:
                return True
        return False
    
    def non_empty_count(self) -> int:
        """
        Returns the number of cells on the board that are not empty, or the number of marbles on the board
        """
        return sum(1 for t in self._cells.values() if t is not TileType.EMPTY)
    
    def non_empty(self) -> Iterator[tuple[Hex, TileType]]:
        """
        Returns (Hex, TileType) for each non-empty cell
        """
        return ((h, t) for h, t in self._cells.items() if t is not TileType.EMPTY)
    
    def unblocked(self) -> Iterator[tuple[Hex, TileType]]:
        """
        Returns (Hex, TileType) for each non-empty cell that is unblocked
        """
        return ((h, t) for h, t in self.non_empty() if self.is_unblocked(h))
