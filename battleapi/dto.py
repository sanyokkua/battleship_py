"""Game API Data Transfer Objects."""
import dataclasses


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
class PlayerState:
    """Representation of the current player state."""

    has_turn: bool
    field: list[list]
    is_winner: bool = False


@dataclasses.dataclass
class SessionState:
    """Representation of the current game session."""

    session_id: str
    players: dict[str, PlayerInfo]
    states: dict[str, PlayerState]
    active_player_id: str
    active_player_name: str
    is_finished_session: bool
