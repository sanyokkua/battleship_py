import dataclasses

@dataclasses.dataclass
class PlayerInfo:
    player_name:str
    player_id: str
    session_id: str


@dataclasses.dataclass
class Information:
    player_id: str
    session_id: str
    player_name: str


@dataclasses.dataclass
class PlayersState:
    players: [PlayerInfo]
    is_opponent_ready: bool


@dataclasses.dataclass
class Cell:
    row: int
    column: int
    has_shot: bool = False
    has_ship: bool = False


@dataclasses.dataclass
class Field:
    number_of_rows: int
    number_of_columns: int
    cells: list[list[Cell]]


@dataclasses.dataclass
class PlayersInfo:
    player_1_name: str
    player_1_id: str
    player_2_name: str
    player_2_id: str
    active_player_id: str


@dataclasses.dataclass
class State:
    player_field: Field
    opponent_field: Field
    players_info: PlayersInfo
