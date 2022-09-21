"""Implementation of the Game Persistence functionality."""
import battleapi.dto as dto
import battleapi.interfaces as types
import battleapi.exceptions as ex


class PersistenceApi(types.GamePersistence):
    """Implementation for the Persistence API required for game controller.

    Args:
        types.GamePersistence (_type_): Inherits interface.
    """

    def __init__(self, db_client: types.DbClient) -> None:
        """Initialize Persistence."""
        self.db_client = db_client

    def save_session(self, session_id: str, session_state: dto.SessionState) -> bool:
        """Save game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.
            session_state (dto.SessionState): current game session state.

        Returns:
            bool: result of the save method.
        """
        return self.db_client.save(session_id, session_state)

    def load_session(self, session_id: str) -> dto.SessionState:
        """Load game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.

        Returns:
            dto.SessionState: saved earlier game session state.
        """
        return self.db_client.load(session_id)

    def remove_session(self, session_id: str) -> bool:
        """Remove game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.

        Returns:
            bool: result of deletion. False if error or absence of the session.
        """
        return self.db_client.remove(session_id)

    def save_player(
        self, session_id: str, player_id: str, player: dto.PlayerInfo
    ) -> bool:
        """Save player to the game session.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.
            player_id (str): identifier of the player to be saved.
            player (dto.PlayerInfo): player information object.

        Returns:
            bool: _description_
        """
        session = self.load_session(session_id)
        players = session.players
        if len(players) >= 2:
            raise ex.ToManyPlayersException(
                f"Currently game already has 2 players. {players}"
            )
        if player_id not in players.keys():
            players[player_id] = player
            return True
        return False

    def load_player(self, session_id: str, player_id: str) -> dto.PlayerInfo:
        """Load player from the game session.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.
            player_id (str): identifier of the player to be saved.

        Returns:
            dto.PlayerInfo: player information object.
        """
        session = self.load_session(session_id)
        players = session.players
        if player_id in players:
            return players[player_id]
        raise ex.PlayerNotFoundException(
            f"Player with id: {player_id} is not found in session: {session_id}"
        )
