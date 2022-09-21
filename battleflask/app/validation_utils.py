"""_summary_

    Raises:
        ex.IsEmptyStringException: _description_
        ex.IsNotValidCoordinateException: _description_

    Returns:
        _type_: _description_
"""
import battleflask.app.exceptions as ex


def validate_is_not_empty_string(value: str | None) -> None:
    """_summary_

    Args:
        value (str | None): _description_

    Raises:
        ex.IsEmptyStringException: _description_
    """
    if is_empty_string(value):
        raise ex.IsEmptyStringException(f'Passed value "{value}" is not valid')


def validate_is_correct_coordinate(value: int | None) -> None:
    """_summary_

    Args:
        value (int | None): _description_

    Raises:
        ex.IsNotValidCoordinateException: _description_
    """
    if is_correct_coordinate(value):
        raise ex.IsNotValidCoordinateException(
            f'Passed value "{value}" is not valid coordinate'
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
