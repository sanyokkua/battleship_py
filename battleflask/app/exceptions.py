class IsEmptyStringException(Exception):
    def __init__(self, message: str):
        Exception.__init__(self, message)


class IsNotValidCoordinateException(Exception):
    def __init__(self, message: str):
        Exception.__init__(self, message)
