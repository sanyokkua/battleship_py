"""
Module contains abstract classes (interfaces) that should be implemented and used for
application usage.
"""
import abc

import battleapi.dto as dto
import battleapi.logic.models as models


class IdGenerator(abc.ABC):
    """Interface for the ID generation classes.

    Args:
        abc (_type_): Inherits abstract metaclass.
    """

    @abc.abstractmethod
    def generate_id(self) -> str:
        """Generate string that can be used as an identifier.

        Returns:
            str: generated id-like string.
        """


class DbClient(abc.ABC):
    """Interface for the DB client required for the game.

    Args:
        abc (_type_): Inherits abstract metaclass.
    """

    @abc.abstractmethod
    def save(self, session_id: str, session: dto.SessionState) -> bool:
        """Save SessionState object to the DB with passed session_id.

        Args:
            session_id (str): unique identifier of the session. Primary Key.
            session (dto.SessionState): Game Session Object.

        Returns:
            bool: success of the operation. True - OK, False - Failure.
        """

    @abc.abstractmethod
    def load(self, session_id: str) -> dto.SessionState:
        """Load SessionState object from the DB with passed session_id.

        Args:
            session_id (str): unique identifier of the session. Primary Key.

        Returns:
            dto.SessionState: Game Session Object.
        """

    @abc.abstractmethod
    def remove(self, session_id: str) -> bool:
        """Remove SessionState object from the DB with passed session_id.

        Args:
            session_id (str): unique identifier of the session. Primary Key.

        Returns:
            bool: success of the operation. True - OK, session deleted, False - Failure
                or session was already deleted or even never exist in the DB
        """


class GamePersistence(abc.ABC):
    """Interface for the Persistence API required for game controller.

    Args:
        abc (_type_): Inherits abstract metaclass.
    """

    db_client: DbClient

    @abc.abstractmethod
    def save_session(self, session_id: str, session_state: dto.SessionState) -> bool:
        """Save game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.
            session_state (dto.SessionState): current game session state.

        Returns:
            bool: result of the save method.
        """

    @abc.abstractmethod
    def load_session(self, session_id: str) -> dto.SessionState | None:
        """Load game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.

        Returns:
            dto.SessionState: saved earlier game session state.
        """

    @abc.abstractmethod
    def remove_session(self, session_id: str) -> bool:
        """Remove game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.

        Returns:
            bool: result of deletion. False if error or absence of the session.
        """


class GameController(abc.ABC):
    """Interface for the game controller which responsible to manage all the actions
    related to the game process.

    Args:
        abc (_type_): Inherits abstract metaclass.
    """

    persistence: GamePersistence
    id_generator: IdGenerator

    @abc.abstractmethod
    def init_game_session(self) -> str:
        """Init new game session.

        In the scope of this method will be created new ID for session,
        session will be saved to the DB, session id will be returned.

        Returns:
            str: created session id value.
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def get_opponent_prepare_status(
        self, session_id: str, current_player_id: str
    ) -> dto.PlayerInfo | None:
        """Return opponent to the passed player_id.

        Args:
            session_id (str): session id of the existing session.
            current_player_id (str): player_id of the player who needs to get information
                of the opponent

        Returns:
            dto.PlayerInfo: opponent player information object.
        """

    @abc.abstractmethod
    def get_prepare_ships_list(
        self, session_id: str, player_id: str
    ) -> list[models.Ship]:
        """Get list of the available ships for the player on preparation stage.

        Args:
            session_id (str): id of the current game session.
            player_id (str): id of the player who requested information.

        Returns:
            list: list of the available ships.
        """

    @abc.abstractmethod
    def get_prepare_player_field(
        self, session_id: str, player_id: str
    ) -> list[list[models.Cell]]:
        """Return field for the player on the preparation stage.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id of the current game session.

        Returns:
            list[list]: field representation.
        """

    @abc.abstractmethod
    def get_opponent(self, session_id: str, player_id: str) -> dto.PlayerInfo | None:
        """Return opponent information to the current player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id of the current game session.

        Returns:
            dto.PlayerInfo: player information.
        """

    @abc.abstractmethod
    def get_active_player(self, session_id: str) -> dto.PlayerInfo | None:
        """Return player information who now should have to make a move.

        Args:
            session_id (str): session id of the current game session.

        Returns:
            dto.PlayerInfo: player information.
        """

    @abc.abstractmethod
    def get_player_by_id(
        self, session_id: str, player_id: str
    ) -> dto.PlayerInfo | None:
        """Return player for session by its id.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id to be returned.

        Returns:
            dto.PlayerInfo: player information.
        """

    @abc.abstractmethod
    def get_number_of_cells_left(self, session_id: str, player_id: str) -> int:
        """Return number of available (not touched) cells to the player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id who requested information.

        Returns:
            int: number of available cells.
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def get_winner(self, session_id: str) -> dto.PlayerInfo:
        """Return winner of the game.

        Args:
            session_id (str): current game session id.

        Returns:
            dto.PlayerInfo: player information.
        """

    @abc.abstractmethod
    def add_ship_to_field(
        self,
        session_id: str,
        player_id: str,
        ship_id: str,
        coordinate: models.Coordinate,
        ship_direction: str,
    ) -> None:
        """Add ship to the field in preparation stage.

        Args:
            session_id (str): current game session id.
            player_id (str): player id who adds ship.
            ship_id (str): ship type.
            coordinate (models.Coordinate): coordinate of the cell.
            ship_direction (str): direction of the ship.
        """

    @abc.abstractmethod
    def remove_ship_from_field(
        self, session_id: str, player_id: str, coordinate: models.Coordinate
    ) -> None:
        """Remove ship from the field in preparation stage.

        Args:
            session_id (str): current game session id.
            player_id (str): player id who removes ship.
            coordinate (models.Coordinate): coordinate of the cell.
        """

    @abc.abstractmethod
    def start_game(self, session_id: str, player_id: str) -> None:
        """Start game.

        Change state of the player to ready to flag the game that next stage can be
        switched to gameplay stage.

        Args:
            session_id (str): current game session id.
            player_id (str): current player id.
        """

    @abc.abstractmethod
    def make_shot(
        self, session_id: str, player_id: str, coordinate: models.Coordinate
    ) -> dto.ShotResult:
        """Make a shot by the opponent field.

        Args:
            session_id (str): current game session id.
            player_id (str): player who makes a shot.
            coordinate (models.Coordinate): coordinate of the cell in opponent field.

        Returns:
            dto.ShotResult: Result of the made shot.
        """
