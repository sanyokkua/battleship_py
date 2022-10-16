"""Implementation of the game logic"""

import logging

import battleapi.abstract as abstract
import battleapi.logic.board as board
import battleapi.logic.configs as config
import battleapi.logic.exceptions as ex
import battleapi.logic.models as models
import battleapi.logic.player as pl
import battleapi.logic.utils as utils

log: logging.Logger = logging.getLogger(__name__)


class Game:
    """Game process implementation.

    Raises:
        ex.ToManyPlayersException: Raised when there was a try to add more than 2
            players.
        ex.PlayerExistException: Raised when there was a try to add second time existing
            player.
        ex.ShipAlreadyOnTheBoardException: Raised when there was a try to add same ship
            to the board.
        ex.GameNotFinishedException: Raised when there was a try to get winner when game
            is not finished.
        ex.PlayerNotFoundException: Raised when player is not found.

    Returns:
        _type_: Game
    """

    _id_generator: abstract.IdGenerator
    _game_config: config.GameConfiguration
    _players: dict[str, pl.Player]
    _active_player_id: str

    def __init__(
        self,
        id_generator: abstract.IdGenerator,
        game_config: config.GameConfiguration,
        players: dict[str, pl.Player] | None = None,
        active_player_id: str | None = None,
    ) -> None:
        """Initialization of the game.

        Args:
            id_generator (abstract.IdGenerator): generator of ids.
            game_config (config.GameConfiguration): game config (classic, custom, etc).
            players (dict[str, pl.Player] | None, optional): list of players.
                Defaults to None.
            active_player_id (str | None, optional): id if the active player
                (who should do the turn). Defaults to None.
        """
        utils.validate_is_not_none(id_generator, "id_generator")
        utils.validate_is_not_none(game_config, "game_config")
        self._id_generator = id_generator
        self._game_config = game_config
        self._players = {} if players is None else players
        self._active_player_id = "" if active_player_id is None else active_player_id
        log.debug(
            "id_gen: %s, config: %s, players: %s, active: %s",
            id_generator,
            game_config,
            self._players,
            self._active_player_id,
        )

    def add_player(self, player_id: str, player_name: str) -> None:
        """Add player to the game session.

        Args:
            player_id (str): player id.
            player_name (str): player name.

        Raises:
            ex.ToManyPlayersException: raised on the number of players > 2.
            ex.PlayerExistException: Raised when a try to add existing player again.
        """
        utils.validate_player_id(player_id)
        utils.validate_not_empty_string(player_name)
        log.debug("player id: %s, name: %s", player_id, player_name)
        if len(self._players) >= 2:
            log.warning("players: %d", len(self._players))
            raise ex.ToManyPlayersException("In the session already exist 2 player")
        if player_id in self._players.keys():
            log.warning("players ids: %s", self._players.keys())
            raise ex.PlayerExistException(f"Player {player_id} already exist")
        ships_not_on_board = {}
        all_ships = {}
        for config in self._game_config.get_ship_configs():
            size = config.ship_size
            amount = config.ship_amount
            for _ in range(amount):
                ship_id = self._id_generator.generate_id()
                ship = models.Ship(ship_id, size)
                ships_not_on_board[ship_id] = ship
                all_ships[ship_id] = ship
        log.debug("ships not on board: %s", ships_not_on_board)
        log.debug("all ships: %s", all_ships)
        player = pl.Player(
            player_id, player_name, board.Board(), ships_not_on_board, all_ships
        )
        log.debug("player: %s", player)
        self._players[player.player_id] = player

    def is_game_initialized(self) -> bool:
        """Check if the game initialized.

        Initialized game means it has 2 players and ready to go to the next game stages.

        Returns:
            bool: True if initialized.
        """
        is_initialized: bool = len(self._players) == 2
        log.debug("is initialized: %s", is_initialized)
        return is_initialized

    def get_available_ships(self, player_id) -> list[models.Ship]:
        """Return ships available to use for preparation stage.

        Args:
            player_id (_type_): player id.

        Returns:
            list[models.Ship]: list of ships.
        """
        ships: dict[str, models.Ship] = self._players[player_id].ships_not_on_board
        available: list[models.Ship] = [] if len(ships) == 0 else list(ships.values())
        log.debug("Available ships: %s", available)
        return available

    def add_ship(
        self, player_id: str, coordinate: models.Coordinate, ship: models.Ship
    ) -> bool:
        """Add ship to the board.

        Args:
            player_id (str): player id.
            coordinate (models.Coordinate): base coordinate.
            ship (models.Ship): ship.

        Raises:
            ex.ShipAlreadyOnTheBoardException: raised when ship is already added to
                the board.

        Returns:
            bool: True if ship added.
        """
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)
        utils.validate_is_not_none(ship)
        log.debug("player id: %s, coord: %s, ship: %s", player_id, coordinate, ship)
        player: pl.Player = self._players[player_id]
        if ship.ship_id not in player.ships_not_on_board.keys():
            raise ex.ShipAlreadyOnTheBoardException(f"{ship.ship_id} can't be added")
        game_board: board.Board = player.board
        game_board.add_ship(coordinate, ship)
        del player.ships_not_on_board[ship.ship_id]
        return True

    def remove_ship(self, player_id: str, coordinate: models.Coordinate) -> bool:
        """Remove ship from the board.

        Args:
            player_id (str): player id.
            coordinate (models.Coordinate): any coordinate of the ship.

        Returns:
            bool: True if deleted.
        """
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)
        player: pl.Player = self._players[player_id]
        ship_id: str | None = player.board.remove_ship(coordinate)
        log.debug("player id: %s, coord: %s, ship: %s", player_id, coordinate, ship_id)
        if ship_id is None:
            return False
        ship: models.Ship = player.all_ships[ship_id]
        player.ships_not_on_board[ship_id] = ship
        return True

    def make_player_ready(self, player_id: str) -> bool:
        """Change player status to ready.

        Change player status only if it added all the ships to the board on the
        preparation stage.

        Args:
            player_id (str): player id.

        Returns:
            bool: True if player is ready.
        """
        utils.validate_player_id(player_id)
        player: pl.Player = self._players[player_id]
        if len(player.ships_not_on_board) == 0:
            player.is_ready = True
        self._select_active_player(player)
        return player.is_ready

    def _select_active_player(self, player: pl.Player) -> None:
        """Find active player.

        Active player will be chosen based on the preparation results (who finished
        preparation stage first).

        Args:
            player (pl.Player): current Player
        """
        opponent: pl.Player = self.get_opponent(player.player_id)
        if player.is_ready and not opponent.is_ready:
            self._active_player_id = player.player_id
        else:
            self._active_player_id = opponent.player_id

    def is_game_ready(self) -> bool:
        """Check if game is ready for gameplay stage.

        Returns:
            bool: True if ready.
        """
        for player in self._players.values():
            amount: int = len(player.ships_not_on_board)
            if not player.is_ready or amount > 0:
                return False
        return True

    def get_player_board(
        self, current_player_id: str, is_hidden: bool = False
    ) -> models.Board:
        """Return game board (field) for player.

        Args:
            current_player_id (str): player id.
            is_hidden (bool, optional): flag to sho ships if requested for opponent.
                Defaults to False.

        Returns:
            models.Board: game board (field).
        """
        utils.validate_player_id(current_player_id)
        player: pl.Player = self._players[current_player_id]
        return player.board.get_board(is_hidden)

    def get_opponent_board(self, current_player_id: str) -> models.Board:
        """Return opponent board with hidden ships.

        Args:
            current_player_id (str): player id of current player.

        Returns:
            models.Board: Game Board (Field).
        """
        utils.validate_player_id(current_player_id)
        player: pl.Player = self.get_opponent(current_player_id)
        return player.board.get_board(is_hidden=True)

    def make_shot(self, player_id: str, coordinate: models.Coordinate) -> bool:
        """Make shot by opponent field.

        Args:
            player_id (str): current player id.
            coordinate (models.Coordinate): coordinate of the shot.

        Returns:
            bool: True if shot was made by ship.
        """
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)
        enemy: pl.Player = self.get_opponent(player_id)
        success: bool = enemy.board.make_shot(coordinate)
        if success:
            self._active_player_id = player_id
        else:
            self._active_player_id = enemy.player_id
        return success

    def is_game_finished(self) -> bool:
        """Check if the game was finished. Game Over check.

        Returns:
            bool: True if game is over.
        """
        for player in self._players.values():
            alive_ships: int = player.board.get_amount_of_alive_ships()
            if alive_ships == 0:
                return True
        return False

    def get_winner(self) -> pl.Player | None:
        """Get winner of the game.

        Raises:
            ex.GameNotFinishedException: Raised when game still in progress.

        Returns:
            pl.Player | None: Winner Player or None.
        """
        if not self.is_game_finished():
            return None
        for player in self._players.values():
            if not player.is_ready:
                return None
        for player in self._players.values():
            alive_ships: int = player.board.get_amount_of_alive_ships()
            if alive_ships != 0:
                return player
        raise ex.GameNotFinishedException("Game is not finished yet")

    def get_opponent(self, current_player_id: str) -> pl.Player:
        """Get opponent.

        Args:
            current_player_id (str): player id.

        Raises:
            ex.PlayerNotFoundException: raised if opponent not found. (Probably when
                opponent is not joined yet).

        Returns:
            pl.Player: Player.
        """
        utils.validate_player_id(current_player_id)
        for player_id, player in self._players.items():
            if (
                current_player_id != player_id
                and current_player_id in self._players.keys()
            ):
                return player
        raise ex.PlayerNotFoundException(
            f"Opponent is not found. {self.players.keys()}"
        )

    @property
    def game_config(self) -> config.GameConfiguration:
        """Return current game configuration.

        Returns:
            config.GameConfiguration: GameConfiguration.
        """
        return self._game_config

    @property
    def players(self) -> dict[str, pl.Player]:
        """Return current players dict.

        Returns:
            dict[str, pl.Player]: Players dictionary.
        """
        return self._players

    @property
    def active_player_id(self) -> str:
        """Return current active player id.

        Returns:
            str: Player id.
        """
        return self._active_player_id
