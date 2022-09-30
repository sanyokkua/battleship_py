"""Definition of the all models used by core logic of the game."""
import dataclasses
import enum
from typing import Union

ShipId = str


@dataclasses.dataclass
class Cell:
    """_summary_"""

    ship_id: Union[str, None] = None
    has_ship: bool = False
    has_shot: bool = False


Coordinate = tuple[int, int]
Board = list[list[Cell]]


class Direction(enum.Enum):
    """_summary_

    Args:
        enum (_type_): _description_
    """

    HORIZONTAL = 0
    VERTICAL = 1


@dataclasses.dataclass
class Ship:
    """_summary_"""

    ship_id: ShipId
    ship_size: int
    direction: Direction = Direction.HORIZONTAL


class ShipType(enum.Enum):
    """_summary_

    Args:
        enum (_type_): _description_
    """

    PatrolBoat = 0
    Submarine = 1
    Destroyer = 2
    Battleship = 3
    Carrier = 4


@dataclasses.dataclass(unsafe_hash=True)
class ShipConfig:
    """_summary_"""

    ship_type: ShipType
    ship_size: int
    ship_amount: int
