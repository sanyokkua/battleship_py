import battleapi.logic.configs as cc
import db.in_memory_db_client as client
from battleapi.api.dto import SessionStateDto


def prepare_session(session_id_1, session_id_2):
    game_config = cc.ClassicGameConfiguration()
    active_player_id = "player_1"
    active_player_id_2 = "player_2"
    session = SessionStateDto(
        session_id=session_id_1,
        game_config=game_config,
        players={},
        active_player_id=active_player_id,
    )
    session2 = SessionStateDto(
        session_id=session_id_2,
        game_config=game_config,
        players={},
        active_player_id=active_player_id_2,
    )
    in_memory_client = client.InMemoryDbClient()
    in_memory_client.save(session_id_1, session)
    in_memory_client.save(session_id_2, session2)
    return in_memory_client


class TestUuid4IdGenerator:
    def test_db_client_creation(self) -> None:
        in_memory_client = client.InMemoryDbClient()
        assert isinstance(in_memory_client.data_source, dict)
        assert len(in_memory_client.data_source) == 0

    def test_client_save(self) -> None:
        in_memory_client = client.InMemoryDbClient()
        session_id = "session_id_1"
        session_id_2 = "session_id_2"
        game_config = cc.ClassicGameConfiguration()
        players = {}
        active_player_id = ""
        active_player_id_2 = "player_2"
        session = SessionStateDto(
            session_id=session_id,
            game_config=game_config,
            players=players,
            active_player_id=active_player_id,
        )
        session2 = SessionStateDto(
            session_id=session_id_2,
            game_config=game_config,
            players=players,
            active_player_id=active_player_id_2,
        )

        in_memory_client.save("session_id_1", session)
        assert len(in_memory_client.data_source) == 1

        in_memory_client.save("session_id_2", session2)
        assert len(in_memory_client.data_source) == 2

        in_memory_client.save("session_id_2", session2)
        assert len(in_memory_client.data_source) == 2

        assert in_memory_client.data_source["session_id_1"].session_id == "session_id_1"
        assert in_memory_client.data_source["session_id_1"].players == {}
        assert in_memory_client.data_source["session_id_1"].active_player_id == ""
        assert in_memory_client.data_source["session_id_2"].session_id == "session_id_2"
        assert in_memory_client.data_source["session_id_2"].players == {}
        assert (
            in_memory_client.data_source["session_id_2"].active_player_id == "player_2"
        )

    def test_client_load(self) -> None:
        session_id_1 = "session_id_1"
        session_id_2 = "session_id_2"
        in_memory_client = prepare_session(session_id_1, session_id_2)
        assert in_memory_client.load(session_id_1).session_id == session_id_1
        assert in_memory_client.load(session_id_1).players == {}
        assert in_memory_client.load(session_id_1).active_player_id == "player_1"

        assert in_memory_client.load(session_id_2).session_id == session_id_2
        assert in_memory_client.load(session_id_2).players == {}
        assert in_memory_client.load(session_id_2).active_player_id == "player_2"

    def test_client_remove(self) -> None:
        session_id_1 = "session_id_1"
        session_id_2 = "session_id_2"
        in_memory_client = prepare_session(session_id_1, session_id_2)
        assert len(in_memory_client.data_source) == 2
        assert in_memory_client.remove(session_id_1)
        assert len(in_memory_client.data_source) == 1
        assert in_memory_client.remove(session_id_2)
        assert len(in_memory_client.data_source) == 0
        assert not in_memory_client.remove("non-existing")
