"""Player info module."""
import dataclasses

import battleapi.logic.board as board
import battleapi.logic.models as models


@dataclasses.dataclass
class Player:
    """Representation of the player in the game."""

    player_id: str
    player_name: str
    board: board.Board
    ships_not_on_board: dict[models.ShipId, models.Ship]
    all_ships: dict[models.ShipId, models.Ship]
    is_ready: bool = False
