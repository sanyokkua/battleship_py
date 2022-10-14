import pytest

import battleapi.logic.board as b
import battleapi.logic.configs as classic_cfg
import battleapi.logic.exceptions as ex
import battleapi.logic.game as s
import battleapi.logic.player as pl
import battleapi.utils.id_generator as id_gen


def create_session():
    id_generator = id_gen.Uuid4IdGenerator()
    config = classic_cfg.ClassicGameConfiguration()
    session = s.Game(id_generator=id_generator, game_config=config)
    return session


class TestGameSession:
    def test_creation_of_the_game_session_default_params(self) -> None:
        session = create_session()
        assert session.active_player_id == ""
        assert len(session.players) == 0

    def test_creation_of_the_game_session_custom_params(self) -> None:
        id_generator = id_gen.Uuid4IdGenerator()
        config = classic_cfg.ClassicGameConfiguration()
        session = s.Game(
            id_generator=id_generator,
            game_config=config,
            players={"id": pl.Player("id", "player", b.Board(), {}, {})},
            active_player_id="test_id",
        )
        assert session.active_player_id == "test_id"
        assert len(session.players) == 1

    def test_add_player(self) -> None:
        session = create_session()
        session.add_player("test_player_id", "test_name")
        assert len(session.players) == 1
        assert session.players["test_player_id"].player_name == "test_name"
        assert session.players["test_player_id"].board is not None
        assert not session.players["test_player_id"].is_ready
        assert len(session.players["test_player_id"].ships_not_on_board) == 10
        with pytest.raises(ex.PlayerExistException):
            session.add_player("test_player_id", "test_name")

        session.add_player("test_player_id_new", "test_name_new")
        assert len(session.players) == 2
        assert session.players["test_player_id_new"].player_name == "test_name_new"
        assert session.players["test_player_id_new"].board is not None
        assert not session.players["test_player_id_new"].is_ready
        assert len(session.players["test_player_id_new"].ships_not_on_board) == 10

        with pytest.raises(ex.ToManyPlayersException):
            session.add_player("test_player_id_error", "test_name_error")

    def test_is_game_initialized(self) -> None:
        session = create_session()
        assert not session.is_game_initialized()

        session.add_player("test_player_id", "test_name")
        session.add_player("test_player_id_new", "test_name_new")
        assert session.is_game_initialized()

    def test_get_available_ships(self) -> None:
        session = create_session()
        session.add_player("test_player_id", "test_name")
        ships = session.get_available_ships("test_player_id")
        assert len(ships) == 10

        for index in range(0, 10, 2):
            coordinate = (index, 0)
            ship = ships.pop()
            session.add_ship("test_player_id", coordinate, ship)
        new_ships_list = session.get_available_ships("test_player_id")
        assert len(new_ships_list) == 5

        session.players["test_player_id"].ships_not_on_board.clear()
        assert len(session.get_available_ships("test_player_id")) == 0

    def test_add_ship(self) -> None:
        session = create_session()
        session.add_player("test_player_id", "test_name")
        ships = session.get_available_ships("test_player_id")
        ship = ships.pop()
        assert session.add_ship("test_player_id", (0, 0), ship)
        assert not session.players["test_player_id"].is_ready
        assert not ship.ship_id in session.players["test_player_id"].ships_not_on_board
        with pytest.raises(ex.IncorrectPlayerIdException):
            session.add_ship("", (0, 0), ship)
        with pytest.raises(ex.CoordinateException):
            session.add_ship("test_player_id", (-1, 10), ship)
        with pytest.raises(ex.ObjectIsNoneException):
            session.add_ship("test_player_id", (0, 0), None)
        with pytest.raises(ex.ShipAlreadyOnTheBoardException):
            session.add_ship("test_player_id", (0, 0), ship)
        assert session.add_ship("test_player_id", (2, 0), ships.pop())
        assert session.add_ship("test_player_id", (4, 0), ships.pop())
        assert session.add_ship("test_player_id", (6, 0), ships.pop())
        assert session.add_ship("test_player_id", (8, 0), ships.pop())
        assert session.add_ship("test_player_id", (1, 5), ships.pop())
        assert session.add_ship("test_player_id", (3, 5), ships.pop())
        assert session.add_ship("test_player_id", (5, 5), ships.pop())
        assert session.add_ship("test_player_id", (7, 5), ships.pop())
        assert session.add_ship("test_player_id", (9, 5), ships.pop())
        assert len(session.get_available_ships("test_player_id")) == 0

    def test_remove_ship(self) -> None:
        session = create_session()
        session.add_player("test_player_id", "test_name")
        ships = session.get_available_ships("test_player_id")
        ship_1 = ships.pop()
        ship_2 = ships.pop()
        ship_3 = ships.pop()
        assert session.add_ship("test_player_id", (0, 0), ship_1)
        assert session.add_ship("test_player_id", (2, 0), ship_2)
        assert session.add_ship("test_player_id", (4, 0), ship_3)
        assert not session.remove_ship("test_player_id", (1, 1))
        assert session.remove_ship("test_player_id", (2, 0))
        assert ship_2.ship_id in session.players["test_player_id"].ships_not_on_board
        with pytest.raises(ex.IncorrectPlayerIdException):
            session.remove_ship("", (0, 0))
        with pytest.raises(ex.CoordinateException):
            session.remove_ship("test_player_id", (-1, 10))

    def test_make_player_ready(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "test_name_2")
        assert not session.make_player_ready("test_player_id_1")
        ships = session.get_available_ships("test_player_id_1")
        assert session.add_ship("test_player_id_1", (0, 0), ships.pop())
        assert session.add_ship("test_player_id_1", (2, 0), ships.pop())
        assert session.add_ship("test_player_id_1", (4, 0), ships.pop())
        assert session.add_ship("test_player_id_1", (6, 0), ships.pop())
        assert session.add_ship("test_player_id_1", (8, 0), ships.pop())
        assert session.add_ship("test_player_id_1", (1, 5), ships.pop())
        assert session.add_ship("test_player_id_1", (3, 5), ships.pop())
        assert session.add_ship("test_player_id_1", (5, 5), ships.pop())
        assert session.add_ship("test_player_id_1", (7, 5), ships.pop())
        assert session.add_ship("test_player_id_1", (9, 5), ships.pop())
        assert session.make_player_ready("test_player_id_1")

    def test__select_active_player(self) -> None:
        pass

    def test_is_game_ready(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "test_name_2")
        assert not session.is_game_ready()
        coordinates = [
            (0, 0),
            (2, 0),
            (4, 0),
            (6, 0),
            (8, 0),
            (1, 5),
            (3, 5),
            (5, 5),
            (7, 5),
            (9, 5),
        ]
        for coordinate in coordinates:
            pl_1_ships = session.get_available_ships("test_player_id_1")
            pl_2_ships = session.get_available_ships("test_player_id_2")
            session.add_ship("test_player_id_1", coordinate, pl_1_ships.pop())
            session.add_ship("test_player_id_2", coordinate, pl_2_ships.pop())
        assert not session.is_game_ready()
        session.make_player_ready("test_player_id_1")
        session.make_player_ready("test_player_id_2")
        assert session.is_game_ready()
        session.remove_ship("test_player_id_2", (9, 5))
        assert not session.is_game_ready()

    def test_get_player_board(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        coordinates = [(0, 0), (2, 0)]
        for coordinate in coordinates:
            pl_1_ships = session.get_available_ships("test_player_id_1")
            session.add_ship("test_player_id_1", coordinate, pl_1_ships.pop())
        board = session.get_player_board("test_player_id_1")
        assert board[0][0].has_ship
        assert not board[1][0].has_ship
        assert board[2][0].has_ship
        assert not board[3][0].has_ship

    def test_get_opponent_board(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "test_name_2")
        coordinates = [(0, 0), (2, 0)]
        for coordinate in coordinates:
            pl_1_ships = session.get_available_ships("test_player_id_1")
            session.add_ship("test_player_id_1", coordinate, pl_1_ships.pop())
        board = session.get_opponent_board("test_player_id_2")
        assert not board[0][0].has_ship
        assert not board[1][0].has_ship

    def test_make_shot(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "test_name_2")
        coordinates = [(0, 0), (2, 0)]
        for coordinate in coordinates:
            pl_1_ships = session.get_available_ships("test_player_id_1")
            session.add_ship("test_player_id_1", coordinate, pl_1_ships.pop())
        board = session.get_opponent_board("test_player_id_2")
        assert not board[0][0].has_ship
        assert not board[1][0].has_ship
        assert not board[2][0].has_ship
        assert not board[3][0].has_ship
        session.make_shot("test_player_id_2", (0, 0))
        board = session.get_opponent_board("test_player_id_2")
        assert board[0][0].has_ship
        assert board[0][0].has_shot

    def test_is_game_finished(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "test_name_2")
        coordinates = [(0, 0), (2, 0)]
        for coordinate in coordinates:
            pl_1_ships = session.get_available_ships("test_player_id_1")
            pl_2_ships = session.get_available_ships("test_player_id_2")
            session.add_ship("test_player_id_1", coordinate, pl_1_ships.pop())
            session.add_ship("test_player_id_2", coordinate, pl_2_ships.pop())
        board = session.players["test_player_id_1"].board
        assert not session.is_game_finished()
        for row in board._board:
            for cell in row:
                if cell.has_ship:
                    cell.has_shot = True
        assert session.is_game_finished()

    def test_get_winner(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "winner")
        coordinates = [(0, 0), (2, 0), (4, 0)]
        for coordinate in coordinates:
            pl_1_ships = session.get_available_ships("test_player_id_1")
            pl_2_ships = session.get_available_ships("test_player_id_2")
            session.add_ship("test_player_id_1", coordinate, pl_1_ships.pop())
            session.add_ship("test_player_id_2", coordinate, pl_2_ships.pop())
        winner = session.get_winner()
        assert winner is None
        for player in session.players.values():
            player.is_ready = True
        for row in range(5):
            for col in range(10):
                session.make_shot("test_player_id_2", (row, col))
        winner = session.get_winner()
        assert winner is not None
        assert winner.player_id == "test_player_id_2"
        assert winner.player_name == "winner"

    def test_get_opponent(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "test_name_2")
        test_val_1 = session.get_opponent("test_player_id_1")
        test_val_2 = session.get_opponent("test_player_id_2")
        assert test_val_1 is not None
        assert test_val_1.player_id == "test_player_id_2"
        assert test_val_2 is not None
        assert test_val_2.player_id == "test_player_id_1"
        with pytest.raises(ex.IncorrectPlayerIdException):
            session.get_opponent("")
        with pytest.raises(ex.PlayerNotFoundException):
            session.get_opponent("not-existing-id")

    def test_game_config(self) -> None:
        session = create_session()
        with pytest.raises(AttributeError):
            session.game_config = None

    def test_players(self) -> None:
        session = create_session()
        assert len(session.players) == 0
        session.add_player("test_player_id_1", "test_name_1")
        assert len(session.players) == 1
        session.add_player("test_player_id_2", "test_name_2")
        assert len(session.players) == 2
        with pytest.raises(AttributeError):
            session.players = {}

    def test_active_player_id(self) -> None:
        session = create_session()
        session.add_player("test_player_id_1", "test_name_1")
        session.add_player("test_player_id_2", "test_name_2")
        assert session.active_player_id == ""
        session._active_player_id = "test_player_id_1"
        assert session.active_player_id == "test_player_id_1"
        with pytest.raises(AttributeError):
            session.active_player_id = "new_value"
