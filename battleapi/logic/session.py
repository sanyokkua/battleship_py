"""Implementation of the game logic"""
from typing import Union

import dto

import battleapi.interfaces as interfaces
import battleapi.logic.board as board
import battleapi.logic.configuration.game_config as gc
import battleapi.logic.exceptions as ex
import battleapi.logic.models as models
import battleapi.logic.utils as utils


class GameSession:
    """_summary_

    Raises:
        ex.ToManyPlayersException: _description_
        ex.PlayerExistException: _description_
        ex.ShipAlreadyOnTheBoardException: _description_
        ex.GameNotFinishedException: _description_
        ex.PlayerNotFoundException: _description_

    Returns:
        _type_: _description_
    """

    _id_generator: interfaces.IdGenerator
    _game_config: gc.GameConfiguration
    _players: dict[str, dto.Player]
    _active_player_id: str

    def __init__(
        self,
        id_generator: interfaces.IdGenerator,
        game_config: gc.GameConfiguration,
        players: Union[dict[str, dto.Player], None] = None,
        active_player_id: Union[str, None] = None,
    ) -> None:
        """_summary_

        Args:
            id_generator (interfaces.IdGenerator): _description_
            game_config (gc.GameConfiguration): _description_
            players (Union[dict[str, pl.Player], None], optional): _description_. Defaults to None.
            active_player_id (Union[str, None], optional): _description_. Defaults to None.
        """
        utils.validate_is_not_none(id_generator, "id_generator")
        utils.validate_is_not_none(game_config, "game_config")

        self._id_generator = id_generator
        self._game_config = game_config
        self._players = {} if players is None else players
        self._active_player_id = "" if active_player_id is None else active_player_id

    def add_player(self, player_id: str, player_name: str) -> None:
        """_summary_

        Args:
            player_id (str): _description_
            player_name (str): _description_

        Raises:
            ex.ToManyPlayersException: _description_
            ex.PlayerExistException: _description_
        """
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
        player = dto.Player(
            player_id, player_name, board.GameBoard(), ships_not_on_board, all_ships
        )
        self._players[player.player_id] = player

    def is_game_initialized(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return len(self._players) == 2

    def get_available_ships(self, player_id) -> list[models.Ship]:
        """_summary_

        Args:
            player_id (_type_): _description_

        Returns:
            list[models.Ship]: _description_
        """
        ships: dict[str, models.Ship] = self._players[player_id].ships_not_on_board
        return [] if len(ships) == 0 else list(ships.values())

    def add_ship(
        self, player_id: str, coordinate: models.Coordinate, ship: models.Ship
    ) -> bool:
        """_summary_

        Args:
            player_id (str): _description_
            coordinate (models.Coordinate): _description_
            ship (models.Ship): _description_

        Raises:
            ex.ShipAlreadyOnTheBoardException: _description_

        Returns:
            bool: _description_
        """
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)
        utils.validate_is_not_none(ship)

        player: dto.Player = self._players[player_id]
        if ship.ship_id not in player.ships_not_on_board.keys():
            raise ex.ShipAlreadyOnTheBoardException(f"{ship.ship_id} can't be added")

        game_board: board.GameBoard = player.board
        game_board.add_ship(coordinate, ship)
        del player.ships_not_on_board[ship.ship_id]
        return True

    def remove_ship(self, player_id: str, coordinate: models.Coordinate) -> bool:
        """_summary_

        Args:
            player_id (str): _description_
            coordinate (models.Coordinate): _description_

        Returns:
            bool: _description_
        """
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)

        player: dto.Player = self._players[player_id]
        ship_id: Union[str, None] = player.board.remove_ship(coordinate)
        if ship_id is None:
            return False
        ship: models.Ship = player.all_ships[ship_id]
        player.ships_not_on_board[ship_id] = ship
        return True

    def make_player_ready(self, player_id: str) -> bool:
        """_summary_

        Args:
            player_id (str): _description_

        Returns:
            bool: _description_
        """
        utils.validate_player_id(player_id)

        player: dto.Player = self._players[player_id]
        if len(player.ships_not_on_board) == 0:
            player.is_ready = True

        self._select_active_player(player)
        return player.is_ready

    def _select_active_player(self, player: dto.Player) -> None:
        """_summary_

        Args:
            player (dto.Player): _description_
        """
        opponent: dto.Player = self.get_opponent(player.player_id)
        if player.is_ready and not opponent.is_ready:
            self._active_player_id = player.player_id
        else:
            self._active_player_id = opponent.player_id

    def is_game_ready(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        for player in self._players.values():
            amount: int = len(player.ships_not_on_board)
            if not player.is_ready or amount > 0:
                return False
        return True

    def get_player_board(
        self, current_player_id: str, is_hidden: bool = False
    ) -> models.Board:
        """_summary_

        Args:
            current_player_id (str): _description_
            is_hidden (bool): _description_

        Returns:
            models.Board: _description_
        """
        utils.validate_player_id(current_player_id)

        player: dto.Player = self._players[current_player_id]
        return player.board.get_board(is_hidden)

    def get_opponent_board(self, current_player_id: str) -> models.Board:
        """_summary_

        Args:
            current_player_id (str): _description_

        Returns:
            models.Board: _description_
        """
        utils.validate_player_id(current_player_id)

        player: dto.Player = self.get_opponent(current_player_id)
        return player.board.get_board(is_hidden=True)

    def make_shot(self, player_id: str, coordinate: models.Coordinate) -> bool:
        """_summary_

        Args:
            player_id (str): _description_
            coordinate (models.Coordinate): _description_

        Returns:
            bool: _description_
        """
        utils.validate_player_id(player_id)
        utils.validate_coordinate(coordinate)

        enemy: dto.Player = self.get_opponent(player_id)
        success: bool = enemy.board.make_shot(coordinate)
        if success:
            self._active_player_id = player_id
        else:
            self._active_player_id = enemy.player_id
        return success

    def is_game_finished(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        for player in self._players.values():
            alive_ships: int = player.board.get_amount_of_alive_ships()
            if alive_ships == 0:
                return True
        return False

    def get_winner(self) -> Union[dto.Player, None]:
        """_summary_

        Raises:
            ex.GameNotFinishedException: _description_

        Returns:
            Union[dto.Player, None]: _description_
        """
        if not self.is_game_finished():
            return None
        for player in self._players.values():
            alive_ships: int = player.board.get_amount_of_alive_ships()
            if alive_ships != 0:
                return player
        raise ex.GameNotFinishedException("Game is not finished yet")

    def get_opponent(self, current_player_id: str) -> dto.Player:
        """_summary_

        Args:
            current_player_id (str): _description_

        Raises:
            ex.PlayerNotFoundException: _description_

        Returns:
            dto.Player: _description_
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
    def game_config(self) -> gc.GameConfiguration:
        """_summary_

        Returns:
            gc.GameConfiguration: _description_
        """
        return self._game_config

    @property
    def players(self) -> dict[str, dto.Player]:
        """_summary_

        Returns:
            dict[str, dto.Player]: _description_
        """
        return self._players

    @property
    def active_player_id(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self._active_player_id
