class IsEmptyStringException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class IsNotValidCoordinateException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class IsNotTheSameSessionIdException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class ActivePlayerIsNotSetException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class GameIsNotFinishedException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)
