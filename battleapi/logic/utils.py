def get_neighbour_coordinates(
    current_coordinate: tuple[int, int], number_of_rows: int, number_of_columns: int
) -> set[tuple[int, int]]:
    """Find coordinates of the neighbours to the passed coordinate.
    Builds a set (list) of the coordinates that should be in the cells
    around passed cell (current_coordinate).
    The logic to build and validate coordinates that will cover cells
    around and filter coordinates that can be out of the field measures.
    ( 0 0 ) ( 0 1 ) ( 0 2 )    ( -1 -1 ) ( -1 +0 ) ( -1 +1 )
    ( 1 0 ) ( 1 1 ) ( 1 2 ) -> ( +0 -1 ) (  1  1 ) ( +0 +1 )
    ( 2 0 ) ( 2 1 ) ( 2 2 )    ( +1 -1 ) ( +1 +0 ) ( +1 +1 )
    Args:
        current_coordinate (tuple[int, int]): cell coordinates.
        number_of_rows (int): field number of rows.
        number_of_columns (int): field number of columns.
    Returns:
        set[tuple[int, int]]: set of the built coordinates.
    """
    # log.debug('get_neighbour_coordinates. current: %s', current_coordinate)
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
        is_not_valid_row: bool = (neighbour_row < 0) or (
            neighbour_row >= number_of_rows
        )
        is_not_valid_col: bool = (neighbour_col < 0) or (
            neighbour_col >= number_of_columns
        )
        is_current_cell: bool = neighbour_row == row and neighbour_col == column
        if is_not_valid_row or is_not_valid_col or is_current_cell:
            # log.debug('Filter coordinates that are not valid')
            continue
        result_set.add((neighbour_row, neighbour_col))
    # log.debug('get_neighbour_coordinates. result num: %d', len(result_set))
    return result_set
