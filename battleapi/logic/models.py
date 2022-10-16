"""Definition of the all models used by core logic of the game."""
import dataclasses
import enum
from typing import Union

ShipId = str


@dataclasses.dataclass
class Cell:
    """Representation of the game cell."""

    ship_id: Union[str, None] = None
    has_ship: bool = False
    has_shot: bool = False


Coordinate = tuple[int, int]
Board = list[list[Cell]]


class Direction(enum.Enum):
    """Representation of the ship direction."""

    HORIZONTAL = 0
    VERTICAL = 1


@dataclasses.dataclass
class Ship:
    """Representation of the ship."""

    ship_id: ShipId
    ship_size: int
    direction: Direction = Direction.HORIZONTAL


class ShipType(enum.Enum):
    """Representation of the ship type."""

    PatrolBoat = 0
    Submarine = 1
    Destroyer = 2
    Battleship = 3
    Carrier = 4


@dataclasses.dataclass(unsafe_hash=True)
class ShipConfig:
    """Representation of the configuration of the ship."""

    ship_type: ShipType
    ship_size: int
    ship_amount: int
