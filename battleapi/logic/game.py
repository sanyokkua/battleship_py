"""Implementation of the game logic"""

import battleapi.abstract as abstract
import battleapi.logic.board as board
import battleapi.logic.configs as config
import battleapi.logic.exceptions as ex
import battleapi.logic.models as models
import battleapi.logic.player as pl
import battleapi.logic.utils as utils


class Game:
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
        utils.validate_is_not_none(id_generator, "id_generator")
        utils.validate_is_not_none(game_config, "game_config")
        self._id_generator = id_generator
        self._game_config = game_config
        self._players = {} if players is None else players
        self._active_player_id = "" if active_player_id is None else active_player_id

    def add_player(self, player_id: str, player_name: str) -> None:
        utils.validate_player_id(player_id)
        utils.validate_not_empty_string(player_name)
        if len(self._players) >= 2:
            raise ex.ToManyPlayersException("In the session already exist 2 player")
        if player_id in self._players.keys():
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
        player = pl.Player(
            player_id, player_name, board.Board(), ships_not_on_board, all_ships
        )
        self._players[player.player_id] = player

    def is_game_initialized(self) -> bool:
        return len(self._players) == 2

    def get_available_ships(self, player_id) -> list[models.Ship]:
        ships: dict[str, models.Ship] = self._players[player_id].ships_not_on_board
        return [] if len(ships) == 0 else list(ships.values())

    def add_ship(
        self, player_id: str, coordinate: models.Coordinate, ship: models.Ship
    ) -> bool:
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)
        utils.validate_is_not_none(ship)
        player: pl.Player = self._players[player_id]
        if ship.ship_id not in player.ships_not_on_board.keys():
            raise ex.ShipAlreadyOnTheBoardException(f"{ship.ship_id} can't be added")
        game_board: board.Board = player.board
        game_board.add_ship(coordinate, ship)
        del player.ships_not_on_board[ship.ship_id]
        return True

    def remove_ship(self, player_id: str, coordinate: models.Coordinate) -> bool:
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)
        player: pl.Player = self._players[player_id]
        ship_id: str | None = player.board.remove_ship(coordinate)
        if ship_id is None:
            return False
        ship: models.Ship = player.all_ships[ship_id]
        player.ships_not_on_board[ship_id] = ship
        return True

    def make_player_ready(self, player_id: str) -> bool:
        utils.validate_player_id(player_id)
        player: pl.Player = self._players[player_id]
        if len(player.ships_not_on_board) == 0:
            player.is_ready = True
        self._select_active_player(player)
        return player.is_ready

    def _select_active_player(self, player: pl.Player) -> None:
        opponent: pl.Player = self.get_opponent(player.player_id)
        if player.is_ready and not opponent.is_ready:
            self._active_player_id = player.player_id
        else:
            self._active_player_id = opponent.player_id

    def is_game_ready(self) -> bool:
        for player in self._players.values():
            amount: int = len(player.ships_not_on_board)
            if not player.is_ready or amount > 0:
                return False
        return True

    def get_player_board(
        self, current_player_id: str, is_hidden: bool = False
    ) -> models.Board:
        utils.validate_player_id(current_player_id)
        player: pl.Player = self._players[current_player_id]
        return player.board.get_board(is_hidden)

    def get_opponent_board(self, current_player_id: str) -> models.Board:
        utils.validate_player_id(current_player_id)
        player: pl.Player = self.get_opponent(current_player_id)
        return player.board.get_board(is_hidden=True)

    def make_shot(self, player_id: str, coordinate: models.Coordinate) -> bool:
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
        for player in self._players.values():
            alive_ships: int = player.board.get_amount_of_alive_ships()
            if alive_ships == 0:
                return True
        return False

    def get_winner(self) -> pl.Player | None:
        if not self.is_game_finished():
            return None
        for player in self._players.values():
            alive_ships: int = player.board.get_amount_of_alive_ships()
            if alive_ships != 0:
                return player
        raise ex.GameNotFinishedException("Game is not finished yet")

    def get_opponent(self, current_player_id: str) -> pl.Player:
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
        return self._game_config

    @property
    def players(self) -> dict[str, pl.Player]:
        return self._players

    @property
    def active_player_id(self) -> str:
        return self._active_player_id
