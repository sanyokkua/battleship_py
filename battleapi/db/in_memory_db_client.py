"""Implementation of DB client for in memory keeping Game Session Data."""
import battleapi.abstract as types
import battleapi.api.dto as dto


class InMemoryDbClient(types.DbClient):
    """Implementation for the DB client required for the game.

    Args:
        abstract.DbClient (_type_): Inherited interface.
    """

    data_source: dict[str, dto.SessionStateDto]

    def __init__(self) -> None:
        self.data_source = {}

    def save(self, session_id: str, session: dto.SessionStateDto) -> bool:
        """Save SessionStateDto object to the DB with passed session_id.

        Args:
            session_id (str): unique identifier of the session. Primary Key.
            session (dto.SessionState): Game Session Object.

        Returns:
            bool: success of the operation. True - OK, False - Failure.
        """
        self.data_source[session_id] = session
        return True

    def load(self, session_id: str) -> dto.SessionStateDto:
        """Load SessionStateDto object from the DB with passed session_id.

        Args:
            session_id (str): unique identifier of the session. Primary Key.

        Returns:
            dto.SessionState: Game Session Object.
        """
        return self.data_source[session_id]

    def remove(self, session_id: str) -> bool:
        """Remove SessionStateDto object from the DB with passed session_id.

        Args:
            session_id (str): unique identifier of the session. Primary Key.

        Returns:
            bool: success of the operation. True - OK, session deleted, False - Failure
                or session was already deleted or even never exist in the DB
        """
        try:
            del self.data_source[session_id]
        except KeyError as err:
            return False
        return True
