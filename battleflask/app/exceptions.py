class IsEmptyStringException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class IsNotValidCoordinateException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class IsNotTheSameSessionIdException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class ActivePlayerIsNotSetException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class GameIsNotFinishedException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)
