"""Implementation of the Game Controller functionality."""
import logging

import battleapi.abstract as abstract
import battleapi.api.dto as dto
import battleapi.logic.configs as config
import battleapi.logic.exceptions as ex
import battleapi.logic.game as game
import battleapi.logic.models as models
import battleapi.logic.player as pl

log: logging.Logger = logging.getLogger(__name__)


def index_board(board_dto: list[list[dto.CellDto]]) -> list[list[dto.CellDto]]:
    indexed_board: list[list[dto.CellDto]] = []
    for row_index, row in enumerate(board_dto):
        indexed_row: list[dto.CellDto] = []
        for col_index, cell in enumerate(row):
            cell.row = row_index
            cell.col = col_index
            indexed_row.append(cell)
        indexed_board.append(indexed_row)
    return indexed_board


class GameControllerApi(abstract.GameController):
    """Implementation for the game controller which responsible to manage all the actions
    related to the game process.

    Args:
        abstract.GameController (_type_): Inherits interface.
    """

    def __init__(
        self, persistence: abstract.GamePersistence, id_generator: abstract.IdGenerator
    ) -> None:
        self.persistence: abstract.GamePersistence = persistence
        self.id_generator: abstract.IdGenerator = id_generator
        log.debug("Inited: pers: s%, gen: %s", persistence, id_generator)

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
            dto.SessionStateDto(
                session_id=session_id,
                game_config=config.ClassicGameConfiguration(),
                players={},
                active_player_id="",
            ),
        )
        if not res:
            log.error("Session is not saved")
            raise ex.SessionIsNotCreatedException("Save session returned false.")
        log.info("Inited session")
        log.debug("SessionId: %s", session_id)
        return session_id

    def create_player_in_session(
        self, session_id: str, player_name: str
    ) -> dto.PlayerDto:
        """Create player by passed player_name.

        Created player will be added to the session by passed session_id.

        Args:
            session_id (str): session id of the created session.
            player_name (str): player name that will be created.

        Returns:
            dto.PlayerDto: player information object of the created player.
        """
        game_session: game.Game = self._load_game_session(session_id)
        player_id: str = self.id_generator.generate_id()
        game_session.add_player(player_id, player_name)
        player: pl.Player = game_session.players[player_id]
        log.debug("SessionId: %s, Player: %s", session_id, player)
        self._save_game_session(game_session, session_id)
        log.info("Player is created")
        self._save_game_session(game_session, session_id)
        return dto.PlayerDto(
            player_name=player.player_name,
            player_id=player.player_id,
            session_id=session_id,
            is_ready=player.is_ready,
        )

    def _save_game_session(self, game_session, session_id) -> None:
        self.persistence.save_session(
            session_id,
            dto.SessionStateDto(
                session_id=session_id,
                game_config=game_session.game_config,
                players=game_session.players,
                active_player_id=game_session.active_player_id,
            ),
        )
        log.debug("Game Session is Saved")

    def _load_game_session(self, session_id: str) -> game.Game:
        session: dto.SessionStateDto | None = self.persistence.load_session(session_id)
        if session is None:
            log.debug("Game Session is not found: %s", session_id)
            raise ex.SessionIsNotCreatedException("Can't load session.")
        game_session: game.Game = game.Game(
            id_generator=self.id_generator,
            game_config=session.game_config,
            players=session.players,
            active_player_id=session.active_player_id,
        )
        log.debug("Game Session is loaded: %s", game_session)
        return game_session

    def get_opponent_prepare_status(
        self, session_id: str, current_player_id: str
    ) -> dto.PlayerDto | None:
        """Return opponent to the passed value.

        Args:
            session_id (str): session id of the existing session.
            current_player_id (str): value of the player who needs to get information
                of the opponent

        Returns:
            dto.PlayerDto: opponent player information object.
        """
        session: game.Game = self._load_game_session(session_id)
        try:
            player: pl.Player = session.get_opponent(current_player_id)
            log.debug("Opponent info: session: %s, opponent: %s", session_id, player)
            return dto.PlayerDto(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
                is_ready=player.is_ready,
            )
        except ex.PlayerNotFoundException:
            log.warning("Opponent is not found for player: %s", current_player_id)
            log.debug("Session: %s", session)
            return None

    def get_prepare_ships_list(
        self, session_id: str, player_id: str
    ) -> list[dto.ShipDto]:
        """Get list of the available ships for the player on preparation stage.

        Args:
            session_id (str): id of the current game session.
            player_id (str): id of the player who requested information.

        Returns:
            list: list of the available ships.
        """
        log.debug("session_id: %s, value: %s", session_id, player_id)
        game_session: game.Game = self._load_game_session(session_id)
        ships: list[models.Ship] = game_session.get_available_ships(player_id)
        ships_dto: list[dto.ShipDto] = list(map(dto.from_model_ship, ships))
        ships_dto.sort(key=lambda ship: ship.ship_size)
        log.debug("ships: %s", ships_dto)
        return ships_dto

    def get_prepare_player_field(
        self, session_id: str, player_id: str
    ) -> list[list[dto.CellDto]]:
        """Return field for the player on the preparation stage.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id of the current game session.

        Returns:
            list[list]: field representation.
        """
        log.debug("session_id: %s, value: %s", session_id, player_id)
        game_session: game.Game = self._load_game_session(session_id)
        board: list[list[models.Cell]] = game_session.get_player_board(player_id)
        board_dto: list[list[dto.CellDto]] = []
        for row in board:
            line: list[dto.CellDto] = list(map(dto.from_model_cell, row))
            board_dto.append(line)
        log.debug("Field: %s", board_dto)
        return index_board(board_dto)

    def get_opponent(self, session_id: str, player_id: str) -> dto.PlayerDto | None:
        """Return opponent information to the current player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id of the current game session.

        Returns:
            dto.PlayerDto: player information.
        """
        log.debug("session_id: %s, value: %s", session_id, player_id)
        game_session: game.Game = self._load_game_session(session_id)
        try:
            player: pl.Player = game_session.get_opponent(player_id)
            log.debug("Opponent: %s", player)
            return dto.PlayerDto(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
                is_ready=player.is_ready,
            )
        except ex.PlayerNotFoundException:
            log.debug("Opponent not found for current_player: %", player_id)
            return None

    def get_active_player(self, session_id: str) -> dto.PlayerDto | None:
        """Return player information who now should have to make a move.

        Args:
            session_id (str): session id of the current game session.

        Returns:
            dto.PlayerDto: player information.
        """
        log.debug("session_id: %s", session_id)
        session: game.Game = self._load_game_session(session_id)
        player_id: str = session.active_player_id
        if player_id is None or player_id == "":
            log.debug("Active player not found (or not yet set)")
            return None
        log.debug("Found active player id: %s", player_id)
        try:
            player: pl.Player = session.players[player_id]
            log.debug("Player: %s", player)
            return dto.PlayerDto(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
                is_ready=player.is_ready,
            )
        except KeyError:
            log.debug("Player not found in the session")
            return None

    def get_player_by_id(self, session_id: str, player_id: str) -> dto.PlayerDto | None:
        """Return player for session by its id.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id to be returned.

        Returns:
            dto.PlayerDto: player information.
        """
        log.debug("session_id: %s, value: %s", session_id, player_id)
        session: game.Game = self._load_game_session(session_id)
        try:
            player: pl.Player = session.players[player_id]
            log.debug("Player: %s", player)
            return dto.PlayerDto(
                player_name=player.player_name,
                player_id=player.player_id,
                session_id=session_id,
                is_ready=player.is_ready,
            )
        except KeyError:
            log.debug("Player not found in the session")
            return None

    def get_number_of_cells_left(self, session_id: str, player_id: str) -> int:
        """Return number of available (not touched) cells to the player.

        Args:
            session_id (str): session id of the current game session.
            player_id (str): player id who requested information.

        Returns:
            int: number of available cells.
        """
        log.debug("session_id: %s, value: %s", session_id, player_id)
        session: game.Game = self._load_game_session(session_id)
        if session.is_game_ready():
            player: pl.Player = session.players[player_id]
            number_of_cells_left = player.board.get_amount_of_not_shot_cells()
            log.debug("Number of cells left: %d", number_of_cells_left)
            return number_of_cells_left
        log.debug("Game is not ready. 0 cells left")
        return 0

    def get_field(
        self, session_id: str, player_id: str, is_for_opponent: bool = False
    ) -> list[list[dto.CellDto]]:
        """Return field representation for player.

        Args:
            session_id (str): id of the current game session.
            player_id (str): player id whose field should be returned.
            is_for_opponent (bool, optional): Flag to let game know if the ships should
                be showed or not. True means ships should be hidden. Defaults to False.

        Returns:
            list[list]: field representation.
        """
        log.debug("session_id: %s, value: %s", session_id, player_id)
        session: game.Game = self._load_game_session(session_id)

        board: list[list[models.Cell]]
        if is_for_opponent:
            log.debug("Loading board for opponent")
            board = session.get_player_board(player_id, is_hidden=True)
        else:
            log.debug("Loading board for current player")
            board = session.get_player_board(player_id)
        board_dto: list[list[dto.CellDto]] = []
        for row in board:
            line: list[dto.CellDto] = list(map(dto.from_model_cell, row))
            board_dto.append(line)
        log.debug("Board: %s", board_dto)
        return index_board(board_dto)

    def get_winner(self, session_id: str) -> dto.PlayerDto | None:
        """Return winner of the game.

        Args:
            session_id (str): current game session id.

        Returns:
            dto.PlayerDto: player information.
        """
        log.debug("session_id: %s", session_id)
        session: game.Game = self._load_game_session(session_id)
        winner: pl.Player | None = session.get_winner()
        if winner is None:
            log.debug("Winner is None")
            return None
        log.debug("Winner: %s", winner)
        return dto.PlayerDto(
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
        log.debug("session_id: %s, value: %s", session_id, player_id)
        log.debug(
            "ship_id: %s, coordinate: %s, ship_direction: %s",
            ship_id,
            coordinate,
            ship_direction,
        )
        session: game.Game = self._load_game_session(session_id)
        ships: dict[str, models.Ship] = session.players[player_id].ships_not_on_board
        ship: models.Ship = ships[ship_id]
        ship.direction = models.Direction[ship_direction]
        session.add_ship(player_id, coordinate, ship)
        self._save_game_session(session, session_id)

    def remove_ship_from_field(
        self, session_id: str, player_id: str, coordinate: models.Coordinate
    ) -> None:
        """Remove ship from the field in preparation stage.

        Args:
            session_id (str): current game session id.
            player_id (str): player id who removes ship.
            coordinate (models.Coordinate): coordinate of the cell.
        """
        log.debug(
            "session_id: %s, value: %s, coordinate: %s",
            session_id,
            player_id,
            coordinate,
        )
        session: game.Game = self._load_game_session(session_id)
        removed = session.remove_ship(player_id, coordinate)
        log.debug("Ships is removed: %s", removed)
        self._save_game_session(session, session_id)

    def start_game(self, session_id: str, player_id: str) -> None:
        """Start game.

        Change state of the player to ready to flag the game that next stage can be
        switched to gameplay stage.

        Args:
            session_id (str): current game session id.
            player_id (str): current player id.
        """
        log.debug("session_id: %s, value: %s", session_id, player_id)
        session: game.Game = self._load_game_session(session_id)
        readiness = session.make_player_ready(player_id)
        log.debug("Player is ready: %s", readiness)
        self._save_game_session(session, session_id)

    def make_shot(
        self, session_id: str, player_id: str, coordinate: models.Coordinate
    ) -> dto.ShotResultDto:
        """Make a shot by the opponent field.

        Args:
            session_id (str): current game session id.
            player_id (str): player who makes a shot.
            coordinate (models.Coordinate): coordinate of the cell in opponent field.

        Returns:
            dto.ShotResultDto: Result of the made shot.
        """
        log.debug(
            "session_id: %s, value: %s, coordinate: %s",
            session_id,
            player_id,
            coordinate,
        )
        session: game.Game = self._load_game_session(session_id)
        is_hit = session.make_shot(player_id, coordinate)
        is_finished: bool = session.is_game_finished()
        log.debug(
            "Is_hit: %s, is_finished: %s, next_pl: %s",
            is_hit,
            is_finished,
            session.active_player_id,
        )
        self._save_game_session(session, session_id)
        return dto.ShotResultDto(
            is_finished=is_finished, next_player=session.active_player_id
        )
