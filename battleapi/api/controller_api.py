"""Implementation of the Game Controller functionality."""
import battleapi.dto as dto
import battleapi.interfaces as types


class ControllerApi(types.GameController):
    """Implementation for the game controller which responsible to manage all the actions
    related to the game process.

    Args:
        types.GameController (_type_): Inherits interface.
    """

    def __init__(
        self, persistence: types.GamePersistence, id_generator: types.IdGenerator
    ):
        self.persistence: types.GamePersistence = persistence
        self.id_generator: types.IdGenerator = id_generator

    def init_game_session(self) -> str:
        """Init new game session.

        In the scope of this method will be created new ID for session,
        session will be saved to the DB, session id will be returned.

        Returns:
            str: created session id value.
        """

    def create_player_in_session(
        self, session_id: str, player_name: str
    ) -> dto.PlayerInfo:
        """Create player by passed player_name.

        Created player will be added to the session by passed session_id.

        Args:
            session_id (str): session id of the created session.
            player_name (str): player name that will be created.

        Returns:
            dto.PlayerInfo: player information object of the created player.
        """

    def get_opponent_prepare_status(
        self, session_id: str, current_player_id: str
    ) -> dto.PlayerInfo:
        """Return opponent to the passed player_id.

        Args:
            session_id (str): session id of the existing session.
            current_player_id (str): player_id of the player who needs to get information
                of the opponent

        Returns:
            dto.PlayerInfo: opponent player information object.
        """

    def get_prepare_ships_list(self, session_id: str, player_id: str) -> list:
        """Get list of the available ships for the player on preparation stage.

        Args:
            session_id (str): id of the current game session.
            player_id (str): id of the player who requested information.

        Returns:
            list: list of the available ships.
        """

    def get_prepare_player_field(self, session_id: str, player_id: str) -> list[list]:
        """Return field for the player on the preparation stage.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id of the current game session.

        Returns:
            list[list]: field representation.
        """

    def get_opponent(self, session_id: str, player_id: str) -> dto.PlayerInfo:
        """Return opponent information to the current player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id of the current game session.

        Returns:
            dto.PlayerInfo: player information.
        """

    def get_active_player(self, session_id: str) -> dto.PlayerInfo:
        """Return player information who now should have to make a move.

        Args:
            session_id (str): session id of the current game session.

        Returns:
            dto.PlayerInfo: player information.
        """

    def get_player_by_id(self, session_id: str, player_id: str) -> dto.PlayerInfo:
        """Return player for session by its id.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id to be returned.

        Returns:
            dto.PlayerInfo: player information.
        """

    def get_number_of_cells_left(self, session_id: str, player_id: str) -> int:
        """Return number of available (not touched) cells to the player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id who requested information.

        Returns:
            int: number of available cells.
        """

    def get_field(
        self, session_id: str, player_id: str, is_for_opponent: bool = False
    ) -> list[list]:
        """Return field representation for player.

        Args:
            session_id (str): id of the current game session.
            player_id (str): player id whose field should be returned.
            is_for_opponent (bool, optional): Flag to let game know if the ships should
                be showed or not. True means ships should be hidden. Defaults to False.

        Returns:
            list[list]: field representation.
        """

    def get_winner(self, session_id: str) -> dto.PlayerInfo:
        """Return winner of the game.

        Args:
            session_id (str): current game session id.

        Returns:
            dto.PlayerInfo: player information.
        """

    def add_ship_to_field(
        self,
        session_id: str,
        player_id: str,
        ship_type: str,
        coordinate: tuple[int, int],
        ship_direction: str,
    ) -> None:
        """Add ship to the field in preparation stage.

        Args:
            session_id (str): current game session id.
            player_id (str): player id who adds ship.
            ship_type (str): ship type.
            coordinate (tuple[int, int]): coordinate of the cell.
            ship_direction (str): direction of the ship.
        """

    def remove_ship_from_field(
        self, session_id: str, player_id: str, coordinate: tuple[int, int]
    ) -> None:
        """Remove ship from the field in preparation stage.

        Args:
            session_id (str): current game session id.
            player_id (str): player id who removes ship.
            coordinate (tuple[int, int]): coordinate of the cell.
        """

    def start_game(self, session_id: str, player_id: str) -> None:
        """Start game.

        Change state of the player to ready to flag the game that next stage can be
        switched to gameplay stage.

        Args:
            session_id (str): current game session id.
            player_id (str): current player id.
        """

    def make_shot(
        self, session_id: str, player_id: str, coordinate: tuple[int, int]
    ) -> dto.ShotResult:
        """Make a shot by the opponent field.

        Args:
            session_id (str): current game session id.
            player_id (str): player who makes a shot.
            coordinate (tuple[int, int]): coordinate of the cell in opponent field.

        Returns:
            dto.ShotResult: Result of the made shot.
        """
