"""Module contains logic of the game board.

Raises:
    ex.CellIsNotEmptyException: raised on the tries to use occupied cell.
"""
import logging
from typing import Callable

import battleapi.logic.exceptions as ex
import battleapi.logic.models as models
import battleapi.logic.utils as utils

log: logging.Logger = logging.getLogger(__name__)

CoordinateSet = set[tuple[int, int]]
CoordinateList = list[tuple[int, int]]
CoordinateCollection = CoordinateList | CoordinateSet
BoardOrNone = models.Board | None
ShipId = str
Filter = Callable[[models.Cell], bool]


class Board:
    """Implementation of the game board logic.

    Raises:
        ex.CellIsNotEmptyException: Raised on the tries to use occupied cell.

    Returns:
        _type_: Board
    """

    _board: models.Board
    _ships_on_board: dict[ShipId, CoordinateSet]

    def __init__(self, board: BoardOrNone = None) -> None:
        """Initialization of the game board (field).

        Args:
            board (BoardOrNone, optional): If the game is loaded, new board will not be
                created and passed board will be used. Defaults to None.
        """
        self._ships_on_board = {}
        if board is None:
            self._board = [
                [models.Cell() for _ in range(utils.SIZE_HORIZONTAL)]
                for _ in range(utils.SIZE_VERTICAL)
            ]
        else:
            self._board = board
        log.debug(
            "Inited. board: %s, ships_on_board: %s", self._board, self._ships_on_board
        )

    @staticmethod
    def _create_ship_coordinates(
        coordinate: models.Coordinate, ship: models.Ship
    ) -> CoordinateSet:
        """Creates ship coordinates for all cells based on the ship direction.

        Args:
            coordinate (models.Coordinate): base (or first) coordinate.
            ship (models.Ship): ship that requires coordinates to be created.

        Returns:
            CoordinateSet: set of coordinates from 1 to 5.
        """
        coordinates: CoordinateSet = set()
        row, col = coordinate
        for diff in range(ship.ship_size):
            if ship.direction == models.Direction.HORIZONTAL:
                coordinates.add((row, col + diff))
            else:
                coordinates.add((row + diff, col))
        log.debug(
            "Ship: %s, Orig coord: %s, created: %s", ship, coordinate, coordinates
        )
        return coordinates

    @staticmethod
    def _create_neighbour_coordinates(
        ship_coordinates: CoordinateCollection,
    ) -> CoordinateSet:
        """Creates neighbour coordinates for the passed ship coordinates.

        Args:
            ship_coordinates (CoordinateCollection): ship coordinates.

        Returns:
            set: set of coordinates of neighbours around the ship coordinates.
        """
        coordinates: CoordinateSet = set()
        for coordinate in ship_coordinates:
            neighbours = utils.get_neighbour_coordinates(coordinate)
            for neighbour in neighbours:
                coordinates.add(neighbour)
        log.debug("orig: %s, neighbours: %s", ship_coordinates, coordinates)
        return coordinates

    def _validate_coordinates(self, coordinates: CoordinateCollection) -> None:
        """Validation of the all coordinates.

        Validates that coordinate in the field (10x10).
        Validates that coordinate doesn't have a ship already.

        Args:
            coordinates (CoordinateCollection): coordinates.

        Raises:
            ex.CellIsNotEmptyException: raised if coordinate already has ship.
        """
        for coordinate in coordinates:
            utils.validate_coordinate(coordinate)
            row, col = coordinate
            if self._board[row][col].has_ship:
                raise ex.CellIsNotEmptyException(
                    f"Coordinate isn't correct {coordinate}"
                )
        log.debug("origin: %s", coordinates)

    def add_ship(self, coordinate: models.Coordinate, ship: models.Ship) -> None:
        """Add ship to the board.

        Args:
            coordinate (models.Coordinate): Ship base coordinate.
            ship (models.Ship): Ship.
        """
        ship_coordinates: CoordinateSet = self._create_ship_coordinates(
            coordinate, ship
        )
        self._validate_coordinates(ship_coordinates)

        neighbour_coordinates: CoordinateSet = self._create_neighbour_coordinates(
            ship_coordinates
        )
        self._validate_coordinates(neighbour_coordinates)

        log.debug(
            "ship: %s, coord: %s, coordinates: %s, neighbours: %s",
            ship,
            coordinate,
            ship_coordinates,
            neighbour_coordinates,
        )
        for ship_coordinate in ship_coordinates:
            row, col = ship_coordinate
            cell: models.Cell = self._board[row][col]
            cell.has_ship = True
            cell.ship_id = ship.ship_id
        self._ships_on_board[ship.ship_id] = ship_coordinates

    def remove_ship(self, coordinate: models.Coordinate) -> ShipId | None:
        """Remove ship from the board (field).

        Args:
            coordinate (models.Coordinate): Any of the ship coordinates (if many)

        Returns:
            Union[ShipId, None]: ship_id if coordinate had ship or None
        """
        utils.validate_coordinate(coordinate)
        row, col = coordinate
        cell: models.Cell = self._board[row][col]
        log.debug("coord: %s, cell: %s", coordinate, cell)
        if cell.has_ship:
            ship_id: ShipId | None = cell.ship_id
            if ship_id is None:
                raise ex.ShipWithoutIdException("Ship doesn't have id")
            log.debug("ship id: %s", ship_id)
            coordinates: CoordinateSet = self._ships_on_board[ship_id]
            for current_coordinate in coordinates:
                row, col = current_coordinate
                self._board[row][col].has_ship = False
                self._board[row][col].ship_id = None
            del self._ships_on_board[ship_id]
            log.debug("removed coordinates: %s", coordinates)
            return ship_id
        return None

    def make_shot(self, coordinate: models.Coordinate) -> bool:
        """Make shot.

        Args:
            coordinate (models.Coordinate): coordinate where shot should be done.

        Returns:
            bool: True if the was hit.
        """
        utils.validate_coordinate(coordinate)
        row, col = coordinate
        cell: models.Cell = self._board[row][col]
        log.debug("coord: %s, cell: %s", coordinate, cell)
        cell.has_shot = True
        if cell.has_ship:
            self._process_cells_after_shot(coordinate)
        return cell.has_ship

    def get_board(self, is_hidden: bool = False) -> models.Board:
        """Return game board.

        Args:
            is_hidden (bool, optional): If board requested for by opponent
            (display on UI) - this parameter will hide not hit ships.
            Defaults to False.

        Returns:
            models.Board: Game Board.
        """
        log.debug("is_hidden: %s", is_hidden)
        field_to_return: models.Board = []
        for row in self._board:
            new_row: list[models.Cell] = []
            for cell in row:
                has_ship: bool = cell.has_ship
                has_shot: bool = cell.has_shot
                show_ship: bool = (not is_hidden and has_ship) or (
                    is_hidden and has_ship and has_shot
                )
                log.debug("show_ship: %s", show_ship)
                ship_id = None if is_hidden else cell.ship_id
                new_cell = models.Cell(
                    ship_id=ship_id, has_ship=show_ship, has_shot=has_shot
                )
                new_row.append(new_cell)
            field_to_return.append(new_row)
        log.debug("field_to_return: %s", field_to_return)
        return field_to_return

    def get_amount_of_not_shot_cells(self) -> int:
        """Return amount of the cells without shot.

        Returns:
            int: number of cells.
        """
        return self._count_amount(lambda cell: not cell.has_shot)

    def get_amount_of_alive_ships(self) -> int:
        """Returns number of cells with ships without hit.

        Returns:
            int: amount of cells.
        """
        return self._count_amount(lambda cell: not cell.has_shot and cell.has_ship)

    def _count_amount(self, cell_filter: Filter) -> int:
        """Utility method to count cells by criteria filter.

        Args:
            cell_filter (Callable[[models.Cell], bool]): filter.

        Returns:
            int: amount of cells.
        """
        count: int = 0
        for row in self._board:
            for cell in row:
                if cell_filter(cell):
                    count += 1
        log.debug("count_amount: %d", count)
        return count

    # noinspection Assert
    def _process_cells_after_shot(self, coordinate: models.Coordinate) -> None:
        """Recalculate board state when shot was made.

        Add shots to the empty cell around destroyed ship.

        Args:
            coordinate (models.Coordinate): coordinate of shot.
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
