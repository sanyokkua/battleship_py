"""Logic exceptions."""


class ToManyPlayersException(Exception):
    """Exception is raised when there was a try to add more than 2 players to game."""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class PlayerExistException(Exception):
    """Exception is raised when there was a try to create again player with existing id"""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class IncorrectPlayerIdException(Exception):
    """Exception is raised when player id is empty or not a string"""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class IncorrectStringException(Exception):
    """Exception is raised when string is empty or not a string"""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class GameStateReCreatedException(Exception):
    """Exception is raised when game state was created again and deleted previous one."""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class GameNotFinishedException(Exception):
    """Exception is raised when game finish results was requested before the end."""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class PlayerDoesNotExistException(Exception):
    """Exception is raised when game state doesn't have player with passed player_id."""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class CoordinateException(Exception):
    """Exception is raised when there was a problem with coordinates of the cell."""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class CellIsNotEmptyException(Exception):
    """Exception is raised when there was a try to add ship to occupied cell."""

    def __init__(self, message: str = "") -> None:
        Exception.__init__(self, message)


class PlayerNotFoundException(Exception):
    """Exception is raised when there was a try to get not existing player."""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class ObjectIsNoneException(Exception):
    """Exception is raised when object is None"""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class ShipAlreadyOnTheBoardException(Exception):
    """Exception is raised when there was a try to add ship that already was added before"""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class ShipWithoutIdException(Exception):
    """Exception is raised when ship doesn't have ship_id value"""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)
