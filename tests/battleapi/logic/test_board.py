import pytest

import battleapi.logic.board as b
import battleapi.logic.exceptions as ex
import battleapi.logic.models as m


def create_cells(has_ship=True, has_shot=False):
    cells: list[list[m.Cell]] = []
    for row in range(10):
        line: list[m.Cell] = []
        for col in range(10):
            cell = m.Cell(f"{row},{col}", has_ship=has_ship, has_shot=has_shot)
            line.append(cell)
        cells.append(line)
    return cells


class TestGameBoard:
    def test_game_board_creation_without_params(self) -> None:
        board = b.Board()

        assert board._board is not None
        assert len(board._board) == 10
        assert len(board._board[0]) == 10
        assert len(board._board[9]) == 10
        assert board._ships_on_board is not None
        assert len(board._ships_on_board) == 0
        for row in board._board:
            for cell in row:
                assert not cell.has_ship
                assert not cell.has_shot
                assert cell.ship_id is None

    def test_game_board_creation_with_params(self) -> None:
        cells = create_cells()
        board = b.Board(cells)

        assert board._board is not None
        assert len(board._board) == 10
        assert len(board._board[0]) == 10
        assert len(board._board[9]) == 10
        assert board._ships_on_board is not None
        assert len(board._ships_on_board) == 0
        for row in board._board:
            for cell in row:
                assert cell.has_ship
                assert not cell.has_shot
                assert cell.ship_id is not None
                assert len(cell.ship_id) >= 3

    def test_static__create_ship_coordinates_size_2_horizontal(self) -> None:
        ship = m.Ship("id", 2, m.Direction.HORIZONTAL)
        coordinates = list(b.Board._create_ship_coordinates((2, 3), ship))
        coordinates.sort()
        assert len(coordinates) == 2
        assert coordinates[0] == (2, 3)
        assert coordinates[1] == (2, 4)

    def test_static__create_ship_coordinates_size_1_horizontal(self) -> None:
        ship = m.Ship("id", 1, m.Direction.HORIZONTAL)
        coordinates = list(b.Board._create_ship_coordinates((2, 3), ship))
        coordinates.sort()
        assert len(coordinates) == 1
        assert coordinates[0] == (2, 3)

    def test_static__create_ship_coordinates_size_1_vertical(self) -> None:
        ship = m.Ship("id", 1, m.Direction.VERTICAL)
        coordinates = list(b.Board._create_ship_coordinates((2, 3), ship))
        coordinates.sort()
        assert len(coordinates) == 1
        assert coordinates[0] == (2, 3)

    def test_static__create_ship_coordinates_size_2_vertical(self) -> None:
        ship = m.Ship("id", 2, m.Direction.VERTICAL)
        coordinates = list(b.Board._create_ship_coordinates((2, 3), ship))
        coordinates.sort()
        assert len(coordinates) == 2
        assert coordinates[0] == (2, 3)
        assert coordinates[1] == (3, 3)

    def test_static__create_ship_coordinates_size_5_horizontal(self) -> None:
        ship = m.Ship("id", 5, m.Direction.HORIZONTAL)
        coordinates = list(b.Board._create_ship_coordinates((4, 0), ship))
        coordinates.sort()
        assert len(coordinates) == 5
        assert coordinates[0] == (4, 0)
        assert coordinates[1] == (4, 1)
        assert coordinates[2] == (4, 2)
        assert coordinates[3] == (4, 3)
        assert coordinates[4] == (4, 4)

    def test_static__create_ship_coordinates_size_5_vertical(self) -> None:
        ship = m.Ship("id", 5, m.Direction.VERTICAL)
        coordinates = list(b.Board._create_ship_coordinates((3, 7), ship))
        coordinates.sort()
        assert len(coordinates) == 5
        assert coordinates[0] == (3, 7)
        assert coordinates[1] == (4, 7)
        assert coordinates[2] == (5, 7)
        assert coordinates[3] == (6, 7)
        assert coordinates[4] == (7, 7)

    def test_static__create_neighbour_coordinates_size_3_vertical(self) -> None:
        ship = m.Ship("id", 3, m.Direction.VERTICAL)
        coordinates = list(b.Board._create_ship_coordinates((6, 6), ship))
        coordinates.sort()
        assert coordinates[0] == (6, 6)
        assert coordinates[1] == (7, 6)
        assert coordinates[2] == (8, 6)
        neighbours = list(b.Board._create_neighbour_coordinates(coordinates))
        neighbours.sort()
        for coordinate in coordinates:
            row, col = coordinate
            neighbour_1 = (row + 1, col)
            neighbour_2 = (row - 1, col)
            neighbour_3 = (row, col - 1)
            neighbour_4 = (row, col + 1)
            neighbour_5 = (row + 1, col + 1)
            neighbour_6 = (row + 1, col - 1)
            neighbour_7 = (row - 1, col + 1)
            neighbour_8 = (row - 1, col - 1)
            assert neighbour_1 in neighbours
            assert neighbour_2 in neighbours
            assert neighbour_3 in neighbours
            assert neighbour_4 in neighbours
            assert neighbour_5 in neighbours
            assert neighbour_6 in neighbours
            assert neighbour_7 in neighbours
            assert neighbour_8 in neighbours

    def test__validate_coordinates_out_of_bounds_1(self) -> None:
        board = b.Board()
        ship = m.Ship("id", 3, m.Direction.VERTICAL)
        coordinates = b.Board._create_ship_coordinates((8, 6), ship)
        with pytest.raises(ex.CoordinateException):
            board._validate_coordinates(coordinates)

    def test__validate_coordinates_out_of_bounds_2(self) -> None:
        board = b.Board()
        ship = m.Ship("id", 3, m.Direction.HORIZONTAL)
        coordinates = b.Board._create_ship_coordinates((9, 9), ship)
        with pytest.raises(ex.CoordinateException):
            board._validate_coordinates(coordinates)

    def test__validate_coordinates_out_of_bounds_not_raised_for_neighbours(
        self,
    ) -> None:
        board = b.Board()
        ship = m.Ship("id", 3, m.Direction.HORIZONTAL)
        coordinates = b.Board._create_ship_coordinates((0, 1), ship)
        neighbours = b.Board._create_neighbour_coordinates(coordinates)
        board._validate_coordinates(neighbours)

    def test__validate_coordinates_cell_has_ship_1(self) -> None:
        board = b.Board()
        ship = m.Ship("id", 3, m.Direction.HORIZONTAL)
        coordinates = b.Board._create_ship_coordinates((5, 5), ship)
        board._board[5][5].has_ship = True
        with pytest.raises(ex.CellIsNotEmptyException):
            board._validate_coordinates(coordinates)

    def test__validate_coordinates_cell_has_ship_2(self) -> None:
        board = b.Board()
        ship = m.Ship("id", 3, m.Direction.HORIZONTAL)
        coordinates = b.Board._create_ship_coordinates((5, 5), ship)
        board._board[5][6].has_ship = True
        with pytest.raises(ex.CellIsNotEmptyException):
            board._validate_coordinates(coordinates)

    def test__validate_coordinates_cell_has_ship_3(self) -> None:
        board = b.Board()
        ship = m.Ship("id", 3, m.Direction.HORIZONTAL)
        coordinates = b.Board._create_ship_coordinates((5, 5), ship)
        board._board[5][7].has_ship = True
        with pytest.raises(ex.CellIsNotEmptyException):
            board._validate_coordinates(coordinates)

    def test_add_ship_size_3_coordinate_0_0_horizontal(self) -> None:
        board = b.Board()
        ship = m.Ship("ship_main_coordinate_0_0", 3, m.Direction.HORIZONTAL)
        board.add_ship((0, 0), ship)
        expected_ship_coordinates = [
            (0, 0),
            (0, 1),
            (0, 2),
        ]
        for coordinate in expected_ship_coordinates:
            row, col = coordinate
            assert board._board[row][col].ship_id == "ship_main_coordinate_0_0"
            assert board._board[row][col].has_ship
            assert not board._board[row][col].has_shot

    def test_add_ship_size_5_coordinate_5_5_vertical(self) -> None:
        board = b.Board()
        ship = m.Ship("ship_main_coordinate_5_5", 5, m.Direction.VERTICAL)
        board.add_ship((5, 5), ship)

        expected_ship_coordinates = [
            (5, 5),
            (6, 5),
            (7, 5),
            (8, 5),
            (9, 5),
        ]
        for coordinate in expected_ship_coordinates:
            row, col = coordinate
            assert board._board[row][col].ship_id == "ship_main_coordinate_5_5"
            assert board._board[row][col].has_ship
            assert not board._board[row][col].has_shot

    def test_add_ship_size_1_coordinate_9_9_vertical(self) -> None:
        board = b.Board()
        ship = m.Ship("ship_main_coordinate_9_9", 1, m.Direction.VERTICAL)
        board.add_ship((9, 9), ship)

        expected_ship_coordinates = [(9, 9)]
        for coordinate in expected_ship_coordinates:
            row, col = coordinate
            assert board._board[row][col].ship_id == "ship_main_coordinate_9_9"
            assert board._board[row][col].has_ship
            assert not board._board[row][col].has_shot

    def test_add_ship_size_3_coordinate_0_9_horizontal_out_of_bounds(self) -> None:
        board = b.Board()
        ship = m.Ship("ship_main_coordinate_0_9", 3, m.Direction.HORIZONTAL)

        with pytest.raises(ex.CoordinateException):
            board.add_ship((0, 9), ship)

    def test_add_ship_size_3_coordinate_9_0_vertical_out_of_bounds(self) -> None:
        board = b.Board()
        ship = m.Ship("ship_main_coordinate_9_0", 3, m.Direction.VERTICAL)

        with pytest.raises(ex.CoordinateException):
            board.add_ship((8, 0), ship)

    def test_add_ship_size_3_coordinate_0_0_horizontal_neighbour_vertical(self) -> None:
        board = b.Board()
        neighbour_ship = m.Ship("ship_main_coordinate_1_0", 3, m.Direction.VERTICAL)
        board.add_ship((1, 0), neighbour_ship)

        ship = m.Ship("ship_main_coordinate_0_0", 3, m.Direction.HORIZONTAL)
        with pytest.raises(ex.CellIsNotEmptyException):
            board.add_ship((0, 0), ship)

    def test_add_ship_size_3_coordinate_0_0_horizontal_neighbour_horizontal(
        self,
    ) -> None:
        board = b.Board()
        neighbour_ship = m.Ship("ship_main_coordinate_0_3", 3, m.Direction.HORIZONTAL)
        board.add_ship((0, 3), neighbour_ship)

        ship = m.Ship("ship_main_coordinate_0_0", 3, m.Direction.HORIZONTAL)
        with pytest.raises(ex.CellIsNotEmptyException):
            board.add_ship((0, 0), ship)

    def test_add_ship_size_4_coordinate_5_5_vertical_neighbour_horizontal(self) -> None:
        board = b.Board()
        neighbour_ship_1 = m.Ship("ship_main_coordinate_3_3", 4, m.Direction.VERTICAL)
        neighbour_ship_2 = m.Ship("ship_main_coordinate_5_6", 4, m.Direction.HORIZONTAL)
        board.add_ship((3, 3), neighbour_ship_1)  # 3-3 4-3 5-3 6-3
        board.add_ship((5, 6), neighbour_ship_2)  # 5-6 6-6 7-6 8-6

        ship = m.Ship("ship_main_coordinate_5_5", 4, m.Direction.VERTICAL)
        with pytest.raises(ex.CellIsNotEmptyException):
            board.add_ship((5, 5), ship)

    def test_remove_ship(self) -> None:
        board = b.Board()
        neighbour_ship_1 = m.Ship("ship_main_coordinate_4_3", 4, m.Direction.VERTICAL)
        board.add_ship((4, 3), neighbour_ship_1)
        neighbour_ship_2 = m.Ship("ship_main_coordinate_5_6", 2, m.Direction.HORIZONTAL)
        board.add_ship((5, 6), neighbour_ship_2)

        del_ship_id_1 = board.remove_ship((4, 3))
        assert "ship_main_coordinate_4_3" == del_ship_id_1
        expected_free_cells = [
            (4, 3),
            (5, 3),
            (6, 3),
            (7, 3),
        ]
        for coordinate in expected_free_cells:
            row, col = coordinate
            assert board._board[row][col].ship_id is None
            assert not board._board[row][col].has_ship
        coordinates_not_touched = [(5, 6), (5, 7)]
        for not_touched in coordinates_not_touched:
            row, col = not_touched
            assert board._board[row][col].ship_id == "ship_main_coordinate_5_6"
            assert board._board[row][col].has_ship

    def test_remove_ship_when_coordinate_does_not_have_ship(self) -> None:
        board = b.Board()
        neighbour_ship_1 = m.Ship("ship_main_coordinate_4_3", 4, m.Direction.VERTICAL)
        board.add_ship((4, 3), neighbour_ship_1)
        neighbour_ship_2 = m.Ship("ship_main_coordinate_5_6", 2, m.Direction.HORIZONTAL)
        board.add_ship((5, 6), neighbour_ship_2)

        del_ship_id_1 = board.remove_ship((5, 5))
        assert del_ship_id_1 is None
        coordinates_not_touched = [
            (5, 6),
            (5, 7),
            (4, 3),
            (5, 3),
            (6, 3),
            (7, 3),
        ]
        for not_touched in coordinates_not_touched:
            row, col = not_touched
            assert board._board[row][col].has_ship

    def test_make_shot(self) -> None:
        board = b.Board()
        neighbour_ship_1 = m.Ship("ship_main_coordinate_0_0", 5, m.Direction.VERTICAL)
        board.add_ship((0, 0), neighbour_ship_1)
        neighbour_ship_2 = m.Ship("ship_main_coordinate_5_5", 3, m.Direction.HORIZONTAL)
        board.add_ship((5, 5), neighbour_ship_2)
        initial_amount_of_cells_without_shot = board.get_amount_of_not_shot_cells()
        initial_amount_of_alive_ships = board.get_amount_of_alive_ships()
        coordinates_with_ships = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 5),
            (5, 6),
            (5, 7),
        ]
        for ship_coordinate in coordinates_with_ships:
            board.make_shot(ship_coordinate)
            row, col = ship_coordinate
            assert board._board[row][col].has_ship
            assert board._board[row][col].has_shot
        coordinates_without_ships = [
            (3, 3),
            (1, 1),
            (4, 3),
            (5, 8),
            (6, 0),
            (7, 1),
        ]
        for not_ship_coordinate in coordinates_without_ships:
            board.make_shot(not_ship_coordinate)
            row, col = not_ship_coordinate
            assert not board._board[row][col].has_ship
            assert board._board[row][col].has_shot

        final_amount_of_cells_without_shot = board.get_amount_of_not_shot_cells()
        final_amount_of_alive_ships = board.get_amount_of_alive_ships()

        assert (
            initial_amount_of_cells_without_shot != final_amount_of_cells_without_shot
        )
        assert initial_amount_of_alive_ships != final_amount_of_alive_ships
        assert final_amount_of_alive_ships == 0

    def test_get_board_should_not_change_board_values(self):
        board = b.Board()
        ship = m.Ship("ship_main_coordinate_0_0", 5, m.Direction.VERTICAL)
        board.add_ship((0, 0), ship)

        returned_board = board.get_board()
        returned_board[0][0].has_ship = False
        returned_board[0][0].ship_id = "Diff_id"
        returned_board[0][0].has_shot = True

        assert not returned_board[0][0].has_ship
        assert returned_board[0][0].ship_id == "Diff_id"
        assert returned_board[0][0].has_shot

        assert board._board[0][0].has_ship
        assert board._board[0][0].ship_id == "ship_main_coordinate_0_0"
        assert not board._board[0][0].has_shot

    def test_get_board_should_not_sho_ship_without_shot(self):
        board = b.Board()
        ship = m.Ship("ship_main_coordinate_0_0", 5, m.Direction.VERTICAL)
        board.add_ship((0, 0), ship)
        board.make_shot((1, 0))
        returned_board = board.get_board(is_hidden=True)

        assert not returned_board[0][0].has_ship
        assert not returned_board[0][0].has_shot

        assert returned_board[1][0].has_ship
        assert returned_board[1][0].has_shot

        assert not returned_board[0][2].has_ship
        assert not returned_board[0][2].has_shot
