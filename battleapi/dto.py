"""Game API Data Transfer Objects."""
import dataclasses

from logic import board as gb
from logic import models as models

import battleapi.logic.configuration.game_config as gc


@dataclasses.dataclass
class PlayerInfo:
    """Representation of the player."""

    player_name: str
    player_id: str
    session_id: str


@dataclasses.dataclass
class ShotResult:
    """Representation of the shot results."""

    is_finished: bool
    next_player: str


@dataclasses.dataclass
class Player:
    """_summary_"""

    player_id: str
    player_name: str
    board: gb.GameBoard
    ships_not_on_board: dict[models.ShipId, models.Ship]
    all_ships: dict[models.ShipId, models.Ship]
    is_ready: bool = False


@dataclasses.dataclass
class SessionState:
    """Representation of the current game session."""

    session_id: str
    game_config: gc.GameConfiguration
    players: dict[str, Player]
    active_player_id: str = ""
