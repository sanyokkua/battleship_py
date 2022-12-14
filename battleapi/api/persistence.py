"""Implementation of the Game Persistence functionality."""
import logging

import battleapi.abstract as abstract
import battleapi.api.dto as dto

log: logging.Logger = logging.getLogger(__name__)


class GamePersistenceApi(abstract.GamePersistence):
    """Implementation for the Persistence API required for game controller.

    Args:
        abstract.GamePersistence (_type_): Inherits interface.
    """

    def __init__(self, db_client: abstract.DbClient) -> None:
        """Initialize Persistence."""
        self.db_client = db_client
        log.debug("Inited: %s", db_client)

    def save_session(self, session_id: str, session_state: dto.SessionStateDto) -> bool:
        """Save game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.
            session_state (dto.SessionState): current game session state.

        Returns:
            bool: result of the save method.
        """
        try:
            log.debug("Save session: %s, state: %s", session_id, session_state)
            return self.db_client.save(session_id, session_state)
        except Exception:
            log.debug("Save session: %s, Failed", session_id)
            return False

    def load_session(self, session_id: str) -> dto.SessionStateDto | None:
        """Load game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.

        Returns:
            dto.SessionState: saved earlier game session state.
        """
        try:
            log.debug("Load session: %s", session_id)
            return self.db_client.load(session_id)
        except Exception:
            log.debug("load session: %s, Failed", session_id)
            return None

    def remove_session(self, session_id: str) -> bool:
        """Remove game session via db_client object.

        Args:
            session_id (str): identifier of the session to be saved. Primary Key.

        Returns:
            bool: result of deletion. False if error or absence of the session.
        """
        try:
            log.debug("Delete session: %s", session_id)
            return self.db_client.remove(session_id)
        except Exception:
            log.debug("Delete session: %s, Failed", session_id)
            return False
