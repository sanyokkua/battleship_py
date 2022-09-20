from battleapi.logic.models.cell import Cell
from battleapi.logic.models.ships import BaseShip
from battleapi.logic.utils import get_neighbour_coordinates


class CoordinateException(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


class Field:
    number_of_rows: int = 10
    number_of_columns: int = 10

    def __init__(self) -> None:
        self._cells: dict[tuple[int, int], Cell] = {}
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                cell: Cell = Cell(row, column)
                self._cells[(row, column)] = cell

    def put_ship(self, coordinate: tuple[int, int], ship: BaseShip) -> None:
        ship.main_coordinate = coordinate
        self._validate_coordinates(ship)
        for coordinate in ship.coordinates:
            cell: Cell = self._cells[coordinate]
            cell.has_ship = True
            cell.is_free = False
            neighbours = get_neighbour_coordinates(
                coordinate, self.number_of_rows, self.number_of_columns
            )
            for neighbour in neighbours:
                neighbour_cell: Cell = self._cells[neighbour]
                neighbour_cell.is_free = False

    def _validate_coordinates(self, ship: BaseShip) -> None:
        for coordinate in ship.coordinates:
            row, column = coordinate
            if row < 0 or row >= self.number_of_rows:
                raise CoordinateException(f"Row coordinate is out of bounds: {row}")
            if column < 0 or column >= self.number_of_columns:
                raise CoordinateException(f"Row coordinate is out of bounds: {column}")
            if not self._cells[coordinate].is_free:
                raise CoordinateException(
                    f"Row coordinate is not free(empty) {coordinate}"
                )
