import battleflask.app.exceptions as ex


def validate_is_not_empty_string(
    value: str | None, var_name: str | None = None
) -> None:
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
    if not is_correct_coordinate(value):
        raise ex.IsNotValidCoordinateException(
            f'Passed value {var_name}->"{value}" is not valid coordinate'
        )


def is_empty_string(value: str | None) -> bool:
    return value is None or not isinstance(value, str) or len(value.strip()) == 0


def is_correct_coordinate(value: int | None) -> bool:
    return value is not None and 0 <= value < 10
