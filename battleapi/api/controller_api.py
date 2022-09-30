"""Implementation of the Game Controller functionality."""
import battleapi.dto as dto
import battleapi.exceptions as ex
import battleapi.interfaces as types
import battleapi.logic.configuration.classic_config as config
import battleapi.logic.exceptions as l_ex
import battleapi.logic.models as models
import battleapi.logic.session as engine


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
        session_id: str = self.id_generator.generate_id()
        res: bool = self.persistence.save_session(
            session_id,
            dto.SessionState(
                session_id=session_id,
                game_config=config.ClassicGameConfiguration(),
                players={},
                active_player_id="",
            ),
        )
        if not res:
            raise ex.SessionIsNotCreatedException("Save session returned false.")
        return session_id

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
        game_session: engine.GameSession = self._load_game_session(session_id)

        player_id: str = self.id_generator.generate_id()
        game_session.add_player(player_id, player_name)
        player: dto.Player = game_session.players[player_id]

        self._save_game_session(game_session, session_id)
        return dto.PlayerInfo(
            player_name=player.player_name,
            player_id=player.player_id,
            session_id=session_id,
        )

    def _save_game_session(self, game_session, session_id) -> None:
        self.persistence.save_session(
            session_id,
            dto.SessionState(
                session_id=session_id,
                game_config=game_session.game_config,
                players=game_session.players,
                active_player_id=game_session.active_player_id,
            ),
        )

    def _load_game_session(self, session_id: str) -> engine.GameSession:
        session: dto.SessionState | None = self.persistence.load_session(session_id)
        if session is None:
            raise ex.SessionIsNotCreatedException("Can't load session.")
        game_session: engine.GameSession = engine.GameSession(
            id_generator=self.id_generator,
            game_config=session.game_config,
            players=session.players,
            active_player_id=session.active_player_id,
        )
        return game_session

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
        session: engine.GameSession = self._load_game_session(session_id)
        try:
            player: dto.Player = session.get_opponent(current_player_id)
            return dto.PlayerInfo(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
            )
        except l_ex.PlayerNotFoundException:
            return None

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
        game_session: engine.GameSession = self._load_game_session(session_id)
        ships: list[models.Ship] = game_session.get_available_ships(player_id)
        return ships

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
        game_session: engine.GameSession = self._load_game_session(session_id)
        ships: list[list[models.Cell]] = game_session.get_player_board(player_id)
        return list(ships)

    def get_opponent(self, session_id: str, player_id: str) -> dto.PlayerInfo | None:
        """Return opponent information to the current player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id of the current game session.

        Returns:
            dto.PlayerInfo: player information.
        """
        game_session: engine.GameSession = self._load_game_session(session_id)
        try:
            player: dto.Player = game_session.get_opponent(player_id)
            return dto.PlayerInfo(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
            )
        except l_ex.PlayerNotFoundException:
            return None

    def get_active_player(self, session_id: str) -> dto.PlayerInfo | None:
        """Return player information who now should have to make a move.

        Args:
            session_id (str): session id of the current game session.

        Returns:
            dto.PlayerInfo: player information.
        """
        session: engine.GameSession = self._load_game_session(session_id)
        player_id: str = session.active_player_id
        if player_id is None or player_id == "":
            return None
        try:
            player: dto.Player = session.players[player_id]
            return dto.PlayerInfo(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
            )
        except KeyError:
            return None

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
        session = self._load_game_session(session_id)
        try:
            player: dto.Player = session.players[player_id]
            return dto.PlayerInfo(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
            )
        except KeyError:
            return None

    def get_number_of_cells_left(self, session_id: str, player_id: str) -> int:
        """Return number of available (not touched) cells to the player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id who requested information.

        Returns:
            int: number of available cells.
        """
        session: engine.GameSession = self._load_game_session(session_id)
        if session.is_game_ready():
            player: dto.Player = session.players[player_id]
            return player.board.get_amount_of_not_shot_cells()
        return 0

    def get_field(
        self, session_id: str, player_id: str, is_for_opponent: bool = False
    ) -> list[list[models.Cell]]:
        """Return field representation for player.

        Args:
            session_id (str): id of the current game session.
            player_id (str): player id whose field should be returned.
            is_for_opponent (bool, optional): Flag to let game know if the ships should
                be showed or not. True means ships should be hidden. Defaults to False.

        Returns:
            list[list]: field representation.
        """
        session: engine.GameSession = self._load_game_session(session_id)
        if is_for_opponent:
            return session.get_player_board(player_id, is_hidden=True)
        return session.get_player_board(player_id)

    def get_winner(self, session_id: str) -> dto.PlayerInfo | None:
        """Return winner of the game.

        Args:
            session_id (str): current game session id.

        Returns:
            dto.PlayerInfo: player information.
        """
        session: engine.GameSession = self._load_game_session(session_id)
        winner: dto.Player | None = session.get_winner()
        if winner is None:
            return None
        return dto.PlayerInfo(
            player_name=winner.player_name,
            player_id=winner.player_id,
            session_id=session_id,
        )

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
        session: engine.GameSession = self._load_game_session(session_id)
        ships: dict[str, models.Ship] = session.players[player_id].ships_not_on_board
        ship: models.Ship = ships[ship_id]
        ship.direction = models.Direction[ship_direction]
        session.add_ship(player_id, coordinate, ship)

    def remove_ship_from_field(
        self, session_id: str, player_id: str, coordinate: models.Coordinate
    ) -> None:
        """Remove ship from the field in preparation stage.

        Args:
            session_id (str): current game session id.
            player_id (str): player id who removes ship.
            coordinate (models.Coordinate): coordinate of the cell.
        """
        session: engine.GameSession = self._load_game_session(session_id)
        session.remove_ship(player_id, coordinate)

    def start_game(self, session_id: str, player_id: str) -> None:
        """Start game.

        Change state of the player to ready to flag the game that next stage can be
        switched to gameplay stage.

        Args:
            session_id (str): current game session id.
            player_id (str): current player id.
        """
        session: engine.GameSession = self._load_game_session(session_id)
        session.make_player_ready(player_id)

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
        session: engine.GameSession = self._load_game_session(session_id)
        session.make_shot(player_id, coordinate)
        is_finished: bool = session.is_game_finished()
        return dto.ShotResult(
            is_finished=is_finished, next_player=session.active_player_id
        )
