"""_summary_

    Raises:
        ex.IsEmptyStringException: _description_
        ex.IsNotValidCoordinateException: _description_

    Returns:
        _type_: _description_
"""
import battleflask.app.exceptions as ex


def validate_is_not_empty_string(
    value: str | None, var_name: str | None = None
) -> None:
    """_summary_

    Args:
        value (str | None): _description_

    Raises:
        ex.IsEmptyStringException: _description_
    """
    if is_empty_string(value):
        raise ex.IsEmptyStringException(
            f'Passed value {var_name}-> "{value}" is not valid'
        )


def validate_is_session_in_cookies_the_same(
    session_id: str, cookies_session_id: str
) -> None:
    if session_id != cookies_session_id:
        raise ex.IsNotTheSameSessionIdException(
            f"Session IDs are different. id1: {session_id}, id2: {cookies_session_id}"
        )


def validate_is_correct_coordinate(
    value: int | None, var_name: str | None = None
) -> None:
    """_summary_

    Args:
        value (int | None): _description_

    Raises:
        ex.IsNotValidCoordinateException: _description_
    """
    if not is_correct_coordinate(value):
        raise ex.IsNotValidCoordinateException(
            f'Passed value {var_name}->"{value}" is not valid coordinate'
        )


def is_empty_string(value: str | None) -> bool:
    """_summary_

    Args:
        value (str | None): _description_

    Returns:
        bool: _description_
    """
    return value is None or not isinstance(value, str) or len(value.strip()) == 0


def is_correct_coordinate(value: int | None) -> bool:
    """_summary_

    Args:
        value (int | None): _description_

    Returns:
        bool: _description_
    """
    return value is not None and 0 <= value < 10
