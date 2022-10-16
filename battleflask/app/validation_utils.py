"""Validation utils used in the controllers.

Raises:
    ex.IsEmptyStringException: raised when string is empty.
    ex.IsNotTheSameSessionIdException: raised when game ids are different.
    ex.IsNotValidCoordinateException: raised when coordinate is not correct.
"""
import battleflask.app.exceptions as ex


def validate_is_not_empty_string(
    value: str | None, var_name: str | None = None
) -> None:
    """Validate string value.

    Args:
        value (str | None): string value.
        var_name (str | None, optional): variable name for debug. Defaults to None.

    Raises:
        ex.IsEmptyStringException: raised if the string is empty.
    """
    if is_empty_string(value):
        raise ex.IsEmptyStringException(
            f'Passed value {var_name}-> "{value}" is not valid'
        )


def validate_is_session_in_cookies_the_same(
    session_id: str, cookies_session_id: str
) -> None:
    """Validate that both session id are equal.

    Args:
        session_id (str): path session id.
        cookies_session_id (str): cookies session id.

    Raises:
        ex.IsNotTheSameSessionIdException: raised if the ids are different.
    """
    if session_id != cookies_session_id:
        raise ex.IsNotTheSameSessionIdException(
            f"Session IDs are different. id1: {session_id}, id2: {cookies_session_id}"
        )


def validate_is_correct_coordinate(
    value: int | None, var_name: str | None = None
) -> None:
    """Validate coordinate.

    Args:
        value (int | None): coordinate.
        var_name (str | None, optional): name of the variable. Defaults to None.

    Raises:
        ex.IsNotValidCoordinateException: raised if the coordinate is not correct.
    """
    if not is_correct_coordinate(value):
        raise ex.IsNotValidCoordinateException(
            f'Passed value {var_name}->"{value}" is not valid coordinate'
        )


def is_empty_string(value: str | None) -> bool:
    """Check if the string is empty.

    Args:
        value (str | None): value to check.

    Returns:
        bool: True if is empty.
    """
    return value is None or not isinstance(value, str) or len(value.strip()) == 0


def is_correct_coordinate(value: int | None) -> bool:
    """Check if the coordinate is correct.

    Args:
        value (int | None): value to check.

    Returns:
        bool: True if there is no problems with coordinate.
    """
    return value is not None and 0 <= value < 10
