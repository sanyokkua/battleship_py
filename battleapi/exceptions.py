"""Definition of the Game Core Exceptions."""


class ToManyPlayersException(Exception):
    """Exception is raised when there was a try to add more than 2 players to session."""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class SessionNotFoundException(Exception):
    """Exception is raised when there was a try to get not existing session."""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class PlayerNotFoundException(Exception):
    """Exception is raised when there was a try to get not existing player."""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)
