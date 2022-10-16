"""Exceptions used in the controllers."""


class IsEmptyStringException(Exception):
    """Represent exception that is raised for empty string values.

    Args:
        Exception (_type_): Inherited base exception.
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class IsNotValidCoordinateException(Exception):
    """Represent exception that is raised for incorrect coordinates.

    Args:
        Exception (_type_): Inherited base exception.
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class IsNotTheSameSessionIdException(Exception):
    """Represent exception that is raised for incorrect session id path and cookies.

    Args:
        Exception (_type_): Inherited base exception.
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class ActivePlayerIsNotSetException(Exception):
    """Represent exception that is raised for empty value of the active player.

    Args:
        Exception (_type_): Inherited base exception.
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class GameIsNotFinishedException(Exception):
    """Represent exception that is raised when requested data is not available for not
     finished games.

    Args:
        Exception (_type_): Inherited base exception.
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)
