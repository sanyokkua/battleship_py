from unittest.mock import MagicMock

import battleapi.api.persistance_api as papi
import battleapi.dto as dto
import battleapi.implementations.in_memory_db_client as memory
import battleapi.logic.configuration.custom_config as cfg


class TestPersistenceApi:
    def test_save_functionality_success(self):
        db_client_with_mocks = memory.InMemoryDbClient()
        db_client_with_mocks.save = MagicMock(return_value=True)

        persistence = papi.PersistenceApi(db_client=db_client_with_mocks)

        session_id = "id_to_check"
        config = cfg.CustomGameConfiguration()
        active_player = "active_player_id"
        session = dto.SessionState(
            session_id=session_id,
            game_config=config,
            players={},
            active_player_id=active_player,
        )

        assert persistence.save_session(session_id, session)

        db_client_with_mocks.save.assert_called_once_with(session_id, session)

    def test_save_functionality_fail(self):
        db_client_with_mocks = memory.InMemoryDbClient()
        db_client_with_mocks.save = MagicMock(side_effect=AttributeError())

        persistence = papi.PersistenceApi(db_client=db_client_with_mocks)
        session_id = "id_to_check"
        config = cfg.CustomGameConfiguration()
        active_player = "active_player_id"
        session = dto.SessionState(
            session_id=session_id,
            game_config=config,
            players={},
            active_player_id=active_player,
        )

        assert not persistence.save_session(session_id, session)
        db_client_with_mocks.save.assert_called_once_with(session_id, session)

    def test_load_functionality_success(self):
        db_client_with_mocks = memory.InMemoryDbClient()
        persistence = papi.PersistenceApi(db_client=db_client_with_mocks)

        session_id = "id_to_check"
        config = cfg.CustomGameConfiguration()
        active_player = "active_player_id"
        session = dto.SessionState(
            session_id=session_id,
            game_config=config,
            players={},
            active_player_id=active_player,
        )
        db_client_with_mocks.load = MagicMock(return_value=session)
        res = persistence.load_session(session_id)

        assert res == session
        db_client_with_mocks.load.assert_called_once_with(session_id)

    def test_load_functionality_fail(self):
        db_client_with_mocks = memory.InMemoryDbClient()
        db_client_with_mocks.load = MagicMock(side_effect=AttributeError())
        persistence = papi.PersistenceApi(db_client=db_client_with_mocks)

        session_id = "error_session_id"
        res = persistence.load_session(session_id)

        assert res == None
        db_client_with_mocks.load.assert_called_once_with(session_id)

    def test_remove_functionality_success(self):
        db_client_with_mocks = memory.InMemoryDbClient()
        db_client_with_mocks.remove = MagicMock(return_value=True)

        persistence = papi.PersistenceApi(db_client=db_client_with_mocks)
        session_id = "session_to_delete"

        assert persistence.remove_session(session_id)
        db_client_with_mocks.remove.assert_called_once_with(session_id)

    def test_remove_functionality_fail(self):
        db_client_with_mocks = memory.InMemoryDbClient()
        db_client_with_mocks.remove = MagicMock(side_effect=AttributeError())

        persistence = papi.PersistenceApi(db_client=db_client_with_mocks)
        session_id = "session_to_delete"

        assert not persistence.remove_session(session_id)
        db_client_with_mocks.remove.assert_called_once_with(session_id)
