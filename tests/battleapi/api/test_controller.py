from unittest.mock import MagicMock

import pytest

import battleapi.api.controller as c
import battleapi.api.dto as dto
import battleapi.api.persistence as p
import battleapi.logic.configs as cfg
import battleapi.logic.exceptions as ex
import battleapi.logic.models as models
import battleapi.utils.id_generator as gen
import db.in_memory_db_client as memory


def create_real_controller():
    generator = gen.Uuid4IdGenerator()
    db_client = memory.InMemoryDbClient()
    persistence = p.GamePersistenceApi(db_client)
    cotroller = c.GameControllerApi(persistence=persistence, id_generator=generator)
    return cotroller


class TestControllerApi:
    def test_init_game_session_success(self) -> None:
        generated_id = "generated_id"
        db_client = memory.InMemoryDbClient()
        persistence = p.GamePersistenceApi(db_client)
        id_generator = gen.Uuid4IdGenerator()
        controller = c.GameControllerApi(
            id_generator=id_generator, persistence=persistence
        )

        persistence.save_session = MagicMock(return_value=True)
        id_generator.generate_id = MagicMock(return_value=generated_id)
        res = controller.init_game_session()

        assert res == generated_id
        id_generator.generate_id.assert_called()

    def test_init_game_session_fail(self) -> None:
        generated_id = "generated_id"
        db_client = memory.InMemoryDbClient()
        persistence = p.GamePersistenceApi(db_client)
        id_generator = gen.Uuid4IdGenerator()
        controller = c.GameControllerApi(
            id_generator=id_generator, persistence=persistence
        )

        persistence.save_session = MagicMock(return_value=False)
        id_generator.generate_id = MagicMock(return_value=generated_id)

        with pytest.raises(ex.SessionIsNotCreatedException):
            controller.init_game_session()
        id_generator.generate_id.assert_called()

    def test_create_player_in_session(self) -> None:
        session_id = "generated_id"
        player_id = "test_player_id"
        player_name = "test_player"
        db_client = memory.InMemoryDbClient()
        persistence = p.GamePersistenceApi(db_client)
        id_generator = gen.Uuid4IdGenerator()
        controller = c.GameControllerApi(
            id_generator=id_generator, persistence=persistence
        )
        config = cfg.CustomGameConfiguration()
        active_player = "active_player_id"
        session = dto.SessionStateDto(
            session_id=session_id,
            game_config=config,
            players={},
            active_player_id=active_player,
        )

        db_client.load = MagicMock(return_value=session)
        id_generator.generate_id = MagicMock(return_value=session_id)

        created_id = controller.init_game_session()
        id_generator.generate_id.assert_called()

        id_generator.generate_id = MagicMock(return_value=player_id)
        db_client.save = MagicMock(return_value=True)
        player_info = controller.create_player_in_session(created_id, player_name)

        id_generator.generate_id.assert_called()
        db_client.load.assert_called_once_with(session_id)
        db_client.save.assert_called()
        assert player_info is not None
        assert player_info.player_id == player_id
        assert player_info.player_name == player_name
        assert player_info.session_id == session_id

    def test_get_opponent_prepare_status(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )

        player_2_not_found = controller.get_opponent_prepare_status(
            session_id, created_player_1.player_id
        )
        assert player_2_not_found is None

        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
        player_found = controller.get_opponent_prepare_status(
            session_id, created_player_1.player_id
        )
        assert player_found is not None
        assert player_found.session_id == session_id
        assert player_found.player_name == created_player_2.player_name
        assert player_found.player_id == created_player_2.player_id

    def test_get_prepare_ships_list(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )

        player_ships_list = controller.get_prepare_ships_list(
            session_id, created_player_1.player_id
        )
        assert len(player_ships_list) == 10

        ship = player_ships_list.pop()
        controller.add_ship_to_field(
            session_id,
            created_player_1.player_id,
            ship.ship_id,
            (0, 0),
            models.Direction.VERTICAL.name,
        )
        assert len(player_ships_list) == 9

    def test_get_prepare_player_field(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        player_ships_list = controller.get_prepare_ships_list(
            session_id, created_player_1.player_id
        )
        ship = player_ships_list.pop()
        controller.add_ship_to_field(
            session_id,
            created_player_1.player_id,
            ship.ship_id,
            (0, 0),
            models.Direction.VERTICAL.name,
        )
        field = controller.get_prepare_player_field(
            session_id, created_player_1.player_id
        )
        for row in range(10):
            if field[row][0].ship_id == ship.ship_id:
                assert field[row][0].has_ship
                assert not field[row][0].has_shot
            else:
                assert not field[row][0].has_ship
                assert not field[row][0].has_shot

    def test_get_opponent(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )

        opponent = controller.get_opponent(session_id, created_player_1.player_id)
        assert opponent is None

        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
        opponent = controller.get_opponent(session_id, created_player_1.player_id)
        assert opponent.player_id == created_player_2.player_id
        assert opponent.player_name == created_player_2.player_name

    def test_get_active_player(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        assert controller.get_active_player(session_id) is None
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
        assert controller.get_active_player(session_id) is None

        player_1 = controller.persistence.db_client.load(session_id).players[
            created_player_1.player_id
        ]
        player_2 = controller.persistence.db_client.load(session_id).players[
            created_player_2.player_id
        ]
        controller.persistence.load_session = MagicMock(
            return_value=dto.SessionStateDto(
                session_id=session_id,
                game_config=cfg.CustomGameConfiguration(),
                players={
                    created_player_1.player_id: player_1,
                    created_player_2.player_id: player_2,
                },
                active_player_id=created_player_2.player_id,
            )
        )
        player = controller.get_active_player(session_id)
        assert player is not None
        assert player.player_id == created_player_2.player_id

    def test_get_player_by_id(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        assert controller.get_active_player(session_id) is None
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
        found_1 = controller.get_player_by_id(session_id, created_player_1.player_id)
        found_2 = controller.get_player_by_id(session_id, created_player_2.player_id)

        assert found_1 is not None
        assert found_2 is not None
        assert found_1.player_id == created_player_1.player_id
        assert found_2.player_id == created_player_2.player_id

    def test_get_number_of_cells_left(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        assert controller.get_active_player(session_id) is None
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
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
            pl_1_ships = controller.get_prepare_ships_list(
                session_id, created_player_1.player_id
            )
            pl_2_ships = controller.get_prepare_ships_list(
                session_id, created_player_2.player_id
            )
            controller.add_ship_to_field(
                session_id,
                created_player_1.player_id,
                pl_1_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
            controller.add_ship_to_field(
                session_id,
                created_player_2.player_id,
                pl_2_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
        controller.start_game(session_id, created_player_1.player_id)
        controller.start_game(session_id, created_player_2.player_id)

        pl_1_cells_1 = controller.get_number_of_cells_left(
            session_id, created_player_1.player_id
        )
        pl_2_cells_1 = controller.get_number_of_cells_left(
            session_id, created_player_2.player_id
        )

        assert pl_1_cells_1 == 100
        assert pl_2_cells_1 == 100

        controller.make_shot(session_id, created_player_1.player_id, (1, 0))
        controller.make_shot(session_id, created_player_1.player_id, (3, 1))
        controller.make_shot(session_id, created_player_1.player_id, (5, 0))

        pl_1_cells_2 = controller.get_number_of_cells_left(
            session_id, created_player_1.player_id
        )
        pl_2_cells_2 = controller.get_number_of_cells_left(
            session_id, created_player_2.player_id
        )

        assert pl_1_cells_2 == 100
        assert pl_2_cells_2 == 97

    def test_get_field(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        assert controller.get_active_player(session_id) is None
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
        coordinates = [
            (2, 0),
            (4, 0),
            (1, 5),
            (5, 5),
            (9, 5),
        ]
        for coordinate in coordinates:
            pl_1_ships = controller.get_prepare_ships_list(
                session_id, created_player_1.player_id
            )
            pl_2_ships = controller.get_prepare_ships_list(
                session_id, created_player_2.player_id
            )
            controller.add_ship_to_field(
                session_id,
                created_player_1.player_id,
                pl_1_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
            controller.add_ship_to_field(
                session_id,
                created_player_2.player_id,
                pl_2_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
        controller.start_game(session_id, created_player_1.player_id)
        controller.start_game(session_id, created_player_2.player_id)
        controller.make_shot(session_id, created_player_1.player_id, (2, 0))
        controller.make_shot(session_id, created_player_1.player_id, (5, 5))

        field_self = controller.get_field(session_id, created_player_2.player_id, False)
        assert field_self[2][0].has_ship
        assert field_self[2][0].has_shot
        assert field_self[5][5].has_ship
        assert field_self[5][5].has_shot
        assert field_self[9][5].has_ship
        assert not field_self[9][5].has_shot
        assert not field_self[0][0].has_ship
        assert not field_self[0][0].has_shot

        field_opponent = controller.get_field(
            session_id, created_player_2.player_id, True
        )
        assert field_opponent[2][0].has_ship
        assert field_opponent[2][0].has_shot
        assert field_opponent[5][5].has_ship
        assert field_opponent[5][5].has_shot
        assert not field_opponent[9][5].has_ship
        assert not field_opponent[9][5].has_shot
        assert not field_opponent[0][0].has_ship
        assert not field_opponent[0][0].has_shot

    def test_get_winner(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
        coordinates = [
            (2, 0),
            (4, 0),
            (1, 5),
            (5, 5),
            (9, 5),
        ]
        for coordinate in coordinates:
            pl_1_ships = controller.get_prepare_ships_list(
                session_id, created_player_1.player_id
            )
            pl_2_ships = controller.get_prepare_ships_list(
                session_id, created_player_2.player_id
            )
            controller.add_ship_to_field(
                session_id,
                created_player_1.player_id,
                pl_1_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
            controller.add_ship_to_field(
                session_id,
                created_player_2.player_id,
                pl_2_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )

        winner = controller.get_winner(session_id)
        assert winner is None

        player_1 = controller.persistence.db_client.load(session_id).players[
            created_player_1.player_id
        ]
        for row in player_1.board._board:
            for cell in row:
                cell.has_shot = True
        player_2 = controller.persistence.db_client.load(session_id).players[
            created_player_2.player_id
        ]
        player_1.is_ready = True
        player_2.is_ready = True

        controller.persistence.load_session = MagicMock(
            return_value=dto.SessionStateDto(
                session_id=session_id,
                game_config=cfg.CustomGameConfiguration(),
                players={
                    created_player_1.player_id: player_1,
                    created_player_2.player_id: player_2,
                },
                active_player_id=created_player_2.player_id,
            )
        )
        winner = controller.get_winner(session_id)
        assert winner is not None
        assert winner.player_id == created_player_2.player_id

    def test_add_ship_to_field(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        coordinates = [
            (2, 0),
            (4, 0),
            (1, 5),
            (5, 5),
            (9, 5),
        ]
        for coordinate in coordinates:
            pl_1_ships = controller.get_prepare_ships_list(
                session_id, created_player_1.player_id
            )
            controller.add_ship_to_field(
                session_id,
                created_player_1.player_id,
                pl_1_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
        field = controller.get_field(session_id, created_player_1.player_id)
        assert field[2][0].has_ship
        assert field[4][0].has_ship
        assert field[1][5].has_ship
        assert field[5][5].has_ship
        assert field[9][5].has_ship

    def test_remove_ship_from_field(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        coordinates = [
            (2, 0),
            (4, 0),
            (1, 5),
            (5, 5),
            (9, 5),
        ]
        for coordinate in coordinates:
            pl_1_ships = controller.get_prepare_ships_list(
                session_id, created_player_1.player_id
            )
            controller.add_ship_to_field(
                session_id,
                created_player_1.player_id,
                pl_1_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
        field = controller.get_field(session_id, created_player_1.player_id)
        assert field[2][0].has_ship
        assert field[4][0].has_ship
        assert field[1][5].has_ship
        assert field[5][5].has_ship
        assert field[9][5].has_ship

        controller.remove_ship_from_field(
            session_id, created_player_1.player_id, (2, 0)
        )
        controller.remove_ship_from_field(
            session_id, created_player_1.player_id, (4, 0)
        )
        controller.remove_ship_from_field(
            session_id, created_player_1.player_id, (1, 5)
        )
        controller.remove_ship_from_field(
            session_id, created_player_1.player_id, (5, 5)
        )
        controller.remove_ship_from_field(
            session_id, created_player_1.player_id, (9, 5)
        )

        field = controller.get_field(session_id, created_player_1.player_id)
        assert not field[2][0].has_ship
        assert not field[4][0].has_ship
        assert not field[1][5].has_ship
        assert not field[5][5].has_ship
        assert not field[9][5].has_ship

    def test_start_game(self) -> None:
        controller = create_real_controller()
        session_id = controller.init_game_session()
        assert controller.get_active_player(session_id) is None
        created_player_1 = controller.create_player_in_session(
            session_id, "test_player_1"
        )
        created_player_2 = controller.create_player_in_session(
            session_id, "test_player_2"
        )
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
            pl_1_ships = controller.get_prepare_ships_list(
                session_id, created_player_1.player_id
            )
            pl_2_ships = controller.get_prepare_ships_list(
                session_id, created_player_2.player_id
            )
            controller.add_ship_to_field(
                session_id,
                created_player_1.player_id,
                pl_1_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
            controller.add_ship_to_field(
                session_id,
                created_player_2.player_id,
                pl_2_ships.pop().ship_id,
                coordinate,
                models.Direction.HORIZONTAL.name,
            )
        controller.start_game(session_id, created_player_1.player_id)
        controller.start_game(session_id, created_player_2.player_id)
        session = controller.persistence.load_session(session_id)
        for player in session.players.values():
            assert player.is_ready
