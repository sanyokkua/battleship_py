"""Utility functions used to help with validation etc.

Raises:
    ex.IncorrectPlayerIdException: raised if the player is not correct.
    ex.IncorrectStringException: raised if the string is empty.
    ex.CoordinateException: raised if the coordinate out of bounds.
    ex.ObjectIsNoneException: raised if the passed object is None.

Returns:
    _type_: module
"""
import logging
from typing import Union

import battleapi.logic.exceptions as ex

log: logging.Logger = logging.getLogger(__name__)

SIZE_HORIZONTAL: int = 10
SIZE_VERTICAL: int = 10


def validate_player_id(player_id: str) -> None:
    """Check if player id is valid.

    Args:
        player_id (str): player id.

    Raises:
        ex.IncorrectPlayerIdException: raised if player id is not correct.
    """
    log.debug("Player id: %s", player_id)
    if (
        player_id is None
        or not isinstance(player_id, str)
        or len(player_id.strip()) == 0
    ):
        raise ex.IncorrectPlayerIdException(f"Value {player_id} is not valid!")


def validate_not_empty_string(value: str) -> None:
    """Check if the value is not empty string.

    Args:
        value (str): passed string.

    Raises:
        ex.IncorrectStringException: raised if the string is not valid.
    """
    log.debug("Player id: %s", value)
    if value is None or not isinstance(value, str) or len(value.strip()) == 0:
        raise ex.IncorrectStringException(f"Value {value} is not valid!")


def validate_coordinate(coordinate: tuple[int, int]) -> None:
    """Check if coordinate has row and column in the field 10x10.

    Args:
        coordinate (models.Coordinate): Coordinate to check.

    Raises:
        ex.CoordinateException: raised if the coordinate out of bounds.
    """
    log.debug("coordinate: %s", coordinate)
    row, column = coordinate
    if row < 0 or row >= SIZE_VERTICAL:
        raise ex.CoordinateException(f"Row coordinate is out of bounds: {row}")
    if column < 0 or column >= SIZE_HORIZONTAL:
        raise ex.CoordinateException(f"Row coordinate is out of bounds: {column}")


def validate_is_not_none(obj: Union[object, None], obj_name: str = "") -> None:
    """Check if the project is not None.

    Args:
        obj (Union[object, None]): object to check.
        obj_name (str, optional): Name of the object that is validated. Defaults to "".

    Raises:
        ex.ObjectIsNoneException: raised if the object is None.
    """
    log.debug("obj: %s", obj)
    if obj is None:
        raise ex.ObjectIsNoneException(f"Object is None. {obj_name}")


def get_neighbour_coordinates(
    current_coordinate: tuple[int, int],
) -> set[tuple[int, int]]:
    """Find neighbour coordinates for the passed coordinate.

    Args:
        current_coordinate (models.Coordinate): initial coordinate.

    Returns:
        set[models.Coordinate]: coordinates around the current coordinate.
    """
    row, column = current_coordinate
    coordinate_modifiers: set[tuple[int, int]] = {
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    }
    result_set: set[tuple[int, int]] = set()
    for row_modifier, column_modifier in coordinate_modifiers:
        neighbour_row: int = row + row_modifier
        neighbour_col: int = column + column_modifier
        is_not_valid_row: bool = (neighbour_row < 0) or (neighbour_row >= SIZE_VERTICAL)
        is_not_valid_col: bool = (neighbour_col < 0) or (
            neighbour_col >= SIZE_HORIZONTAL
        )
        is_current_cell: bool = neighbour_row == row and neighbour_col == column
        if is_not_valid_row or is_not_valid_col or is_current_cell:
            log.debug("Filter coordinates that are not valid")
            continue
        result_set.add((neighbour_row, neighbour_col))
    log.debug("get_neighbour_coordinates. result num: %d", len(result_set))
    return result_set
