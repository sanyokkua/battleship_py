"""_summary_

Raises:
    ex.CellIsNotEmptyException: _description_

Returns:
    _type_: _description_
"""
from typing import Callable, Union

import battleapi.logic.exceptions as ex
import battleapi.logic.models as models
import battleapi.logic.utils as utils

CoordinateSet = set[tuple[int, int]]
CoordinateList = list[tuple[int, int]]
CoordinateCollection = Union[CoordinateList, CoordinateSet]
BoardOrNone = Union[models.Board, None]
ShipId = str


class GameBoard:
    """_summary_

    Raises:
        ex.CellIsNotEmptyException: _description_

    Returns:
        _type_: _description_
    """

    _board: models.Board
    _ships_on_board: dict[ShipId, set[models.Coordinate]]

    def __init__(self, board: BoardOrNone = None) -> None:
        """_summary_

        Args:
            board (BoardOrNone, optional): _description_. Defaults to None.
        """
        self._ships_on_board = {}
        if board is None:
            self._board = [
                [models.Cell() for _ in range(utils.SIZE_HORIZONTAL)]
                for _ in range(utils.SIZE_VERTICAL)
            ]
        else:
            self._board = board

    @staticmethod
    def _create_ship_coordinates(
        coordinate: models.Coordinate, ship: models.Ship
    ) -> CoordinateSet:
        """_summary_

        Args:
            coordinate (models.Coordinate): _description_
            ship (models.Ship): _description_

        Returns:
            CoordinateSet: _description_
        """
        coordinates: CoordinateSet = set()
        row, col = coordinate
        for diff in range(ship.ship_size):
            if ship.direction == models.Direction.HORIZONTAL:
                coordinates.add((row, col + diff))
            else:
                coordinates.add((row + diff, col))
        return coordinates

    @staticmethod
    def _create_neighbour_coordinates(
        ship_coordinates: CoordinateCollection,
    ) -> CoordinateSet:
        """_summary_

        Args:
            ship_coordinates (CoordinateCollection): _description_

        Returns:
            _type_: _description_
        """
        coordinates: CoordinateSet = set()
        for coordinate in ship_coordinates:
            neighbours = utils.get_neighbour_coordinates(coordinate)
            for neighbour in neighbours:
                coordinates.add(neighbour)
        return coordinates

    def _validate_coordinates(self, coordinates: CoordinateCollection) -> None:
        """_summary_

        Args:
            coordinates (CoordinateCollection): _description_

        Raises:
            ex.CellIsNotEmptyException: _description_
        """
        for coordinate in coordinates:
            utils.validate_coordinate(coordinate)
            row, col = coordinate
            if self._board[row][col].has_ship:
                raise ex.CellIsNotEmptyException(
                    f"Coordinate isn't correct {coordinate}"
                )

    def add_ship(self, coordinate: models.Coordinate, ship: models.Ship) -> None:
        """_summary_

        Args:
            coordinate (models.Coordinate): _description_
            ship (models.Ship): _description_
        """
        ship_coordinates: CoordinateSet = self._create_ship_coordinates(
            coordinate, ship
        )
        self._validate_coordinates(ship_coordinates)

        neighbour_coordinates: CoordinateSet = self._create_neighbour_coordinates(
            ship_coordinates
        )
        self._validate_coordinates(neighbour_coordinates)

        for ship_coordinate in ship_coordinates:
            row, col = ship_coordinate
            cell: models.Cell = self._board[row][col]
            cell.has_ship = True
            cell.ship_id = ship.ship_id
        self._ships_on_board[ship.ship_id] = ship_coordinates

    def remove_ship(self, coordinate: models.Coordinate) -> Union[ShipId, None]:
        """_summary_

        Args:
            coordinate (models.Coordinate): _description_

        Returns:
            Union[ShipId, None]: _description_
        """
        utils.validate_coordinate(coordinate)
        row, col = coordinate
        cell: models.Cell = self._board[row][col]
        if cell.has_ship:
            ship_id: Union[str, None] = cell.ship_id
            if ship_id is None:
                raise ex.ShipWithoutIdException("Ship doesn't have id")
            coordinates: CoordinateSet = self._ships_on_board[ship_id]
            for current_coordinate in coordinates:
                row, col = current_coordinate
                self._board[row][col].has_ship = False
                self._board[row][col].ship_id = None
            del self._ships_on_board[ship_id]
            return ship_id
        return None

    def make_shot(self, coordinate: models.Coordinate) -> bool:
        """_summary_

        Args:
            coordinate (models.Coordinate): _description_

        Returns:
            bool: _description_
        """
        utils.validate_coordinate(coordinate)
        row, col = coordinate
        cell: models.Cell = self._board[row][col]
        cell.has_shot = True
        if cell.has_ship:
            self._process_cells_after_shot(coordinate)
        return cell.has_ship

    def get_board(self, is_hidden: bool = False) -> models.Board:
        """_summary_

        Args:
            is_hidden (bool, optional): _description_. Defaults to False.

        Returns:
            models.Board: _description_
        """
        field_to_return: models.Board = []
        for row in self._board:
            new_row: list[models.Cell] = []
            for cell in row:
                has_ship: bool = cell.has_ship
                has_shot: bool = cell.has_shot
                show_ship: bool = (not is_hidden and has_ship) or (
                    is_hidden and has_ship and has_shot
                )
                ship_id = None if is_hidden else cell.ship_id
                new_cell = models.Cell(
                    ship_id=ship_id, has_ship=show_ship, has_shot=has_shot
                )
                new_row.append(new_cell)
            field_to_return.append(new_row)
        return field_to_return

    def get_amount_of_not_shot_cells(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._count_amount(lambda cell: not cell.has_shot)

    def get_amount_of_alive_ships(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._count_amount(lambda cell: not cell.has_shot and cell.has_ship)

    def _count_amount(self, cell_filter: Callable[[models.Cell], bool]) -> int:
        """_summary_

        Args:
            cell_filter (Callable[[models.Cell], bool]): _description_

        Returns:
            int: _description_
        """
        count: int = 0
        for row in self._board:
            for cell in row:
                if cell_filter(cell):
                    count += 1
        return count

    # noinspection Assert
    def _process_cells_after_shot(self, coordinate: models.Coordinate) -> None:
        """_summary_

        Args:
            coordinate (models.Coordinate): _description_
        """
        row, col = coordinate
        cell = self._board[row][col]
        assert cell.has_ship
        assert cell.ship_id is not None
        ship_coordinates: CoordinateSet = self._ships_on_board[cell.ship_id]
        ship_size: int = len(ship_coordinates)
        ship_destroyed_cells: int = 0
        for ship_coordinate in ship_coordinates:
            ship_row, ship_col = ship_coordinate
            ship_cell: models.Cell = self._board[ship_row][ship_col]
            if ship_cell.has_ship and ship_cell.has_shot:
                ship_destroyed_cells += 1
        is_destroyed: bool = ship_destroyed_cells == ship_size
        if is_destroyed:
            for process_coordinate in ship_coordinates:
                neighbours: CoordinateSet = utils.get_neighbour_coordinates(
                    process_coordinate
                )
                for neighbour in neighbours:
                    n_row, n_col = neighbour
                    n_cell: models.Cell = self._board[n_row][n_col]
                    n_cell.has_shot = True
