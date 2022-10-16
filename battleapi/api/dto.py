"""Game API Data Transfer Objects."""
import dataclasses

import battleapi.logic.configs as config
import battleapi.logic.models as model
import battleapi.logic.player as player

Coordinate = tuple[int, int]
ShipId = str


@dataclasses.dataclass
class CellDto:
    """Representation of the Field Cell.

    ship_id - Unique ship identifier.
    has_ship - True if the cell has ship.
    has_shot - Tru if the cell has shot.
    row - int value, represent number of row (from 0 to 9).
    col - int value, represent number of column (from 0 to 9).
    is_not_available - True if the cell has ship or if in the neighbour cell - is ship.
    """

    ship_id: str | None = None
    has_ship: bool = False
    has_shot: bool = False
    row: int = 0
    col: int = 0
    is_not_available: bool = False


@dataclasses.dataclass
class ShipDto:
    """Represent ship.

    ship_id - Unique ship identifier.
    ship_size - Number of cells in the ship (1-5).
    direction - Direction of the ship. Can be VERTICAL or HORIZONTAL.
    """

    ship_id: str
    ship_size: int
    direction: str = f"{model.Direction.HORIZONTAL.name}"


@dataclasses.dataclass
class PlayerDto:
    """Representation of the player.

    player_name - name that player used during creating/joining to the game.
    player_id - unique identifier that was given by app to user to work with player.
    session_id - unique identifier of the game session.
    is_ready - True if the player finished with preparation stage.
    """

    player_name: str
    player_id: str
    session_id: str
    is_ready: bool = False


@dataclasses.dataclass
class ShotResultDto:
    """Representation of the shot results."""

    is_finished: bool
    next_player: str


@dataclasses.dataclass
class SessionStateDto:
    """Representation of the current game session."""

    session_id: str
    game_config: config.GameConfiguration
    players: dict[str, player.Player]
    active_player_id: str = ""


def from_model_cell(cell: model.Cell) -> CellDto:
    """Utility to map model.Cell object to CellDto object.

    Args:
        cell (model.Cell): original model object.

    Returns:
        CellDto: mapped CellDto.
    """
    return CellDto(ship_id=cell.ship_id, has_ship=cell.has_ship, has_shot=cell.has_shot)


def from_model_ship(ship: model.Ship) -> ShipDto:
    """Utility to map model.Ship object to ShipDto object.

    Args:
        ship (model.Ship): original model object.

    Returns:
        ShipDto: mapped ShipDto.
    """
    return ShipDto(
        ship_id=ship.ship_id, ship_size=ship.ship_size, direction=ship.direction.name
    )
