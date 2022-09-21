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
