"""Definition of the Game Core Exceptions."""


class SessionIsNotCreatedException(Exception):
    """Exception is raised when there was a problem with session creation."""

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)
