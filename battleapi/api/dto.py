"""Game API Data Transfer Objects."""
import dataclasses

import battleapi.logic.configs as config
import battleapi.logic.models as model
import battleapi.logic.player as player

Coordinate = tuple[int, int]
ShipId = str


@dataclasses.dataclass
class CellDto:
    """_summary_"""

    ship_id: str | None = None
    has_ship: bool = False
    has_shot: bool = False
    row: int = 0
    col: int = 0
    is_not_available: bool = False


@dataclasses.dataclass
class ShipDto:
    """_summary_"""

    ship_id: str
    ship_size: int
    direction: str = f"{model.Direction.HORIZONTAL.name}"


@dataclasses.dataclass
class PlayerDto:
    """Representation of the player."""

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
    return CellDto(ship_id=cell.ship_id, has_ship=cell.has_ship, has_shot=cell.has_shot)


def from_model_ship(ship: model.Ship) -> ShipDto:
    return ShipDto(
        ship_id=ship.ship_id, ship_size=ship.ship_size, direction=ship.direction.name
    )
