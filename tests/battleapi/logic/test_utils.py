import pytest

import battleapi.logic.exceptions as ex
import battleapi.logic.utils as utils


class TestUtilFunctions:
    def test_validate_player_id(self) -> None:
        with pytest.raises(ex.IncorrectPlayerIdException):
            utils.validate_player_id(None)
        with pytest.raises(ex.IncorrectPlayerIdException):
            utils.validate_player_id("")
        with pytest.raises(ex.IncorrectPlayerIdException):
            utils.validate_player_id("     ")
        with pytest.raises(ex.IncorrectPlayerIdException):
            utils.validate_player_id(999)

        utils.validate_player_id("Correct_player_id")

    def test_validate_not_empty_string(self) -> None:
        with pytest.raises(ex.IncorrectStringException):
            utils.validate_not_empty_string(None)
        with pytest.raises(ex.IncorrectStringException):
            utils.validate_not_empty_string("")
        with pytest.raises(ex.IncorrectStringException):
            utils.validate_not_empty_string("     ")
        with pytest.raises(ex.IncorrectStringException):
            utils.validate_not_empty_string(999)

        utils.validate_not_empty_string("Any non Empty string")

    def test_validate_coordinate(self) -> None:
        with pytest.raises(ex.CoordinateException):
            utils.validate_coordinate((0, -1))
        with pytest.raises(ex.CoordinateException):
            utils.validate_coordinate((-1, 0))
        with pytest.raises(ex.CoordinateException):
            utils.validate_coordinate((-1, -1))
        with pytest.raises(ex.CoordinateException):
            utils.validate_coordinate((10, 0))
        with pytest.raises(ex.CoordinateException):
            utils.validate_coordinate((0, 10))
        with pytest.raises(ex.CoordinateException):
            utils.validate_coordinate((10, 10))

        utils.validate_coordinate((2, 3))
        utils.validate_coordinate((0, 0))
        utils.validate_coordinate((9, 9))
        utils.validate_coordinate((5, 5))

    def test_validate_is_not_none(self) -> None:
        with pytest.raises(ex.ObjectIsNoneException):
            utils.validate_is_not_none(None)
        utils.validate_is_not_none("")
        utils.validate_is_not_none(0)
        utils.validate_is_not_none((1, 300))

    def test_get_neighbour_coordinates_0_0_4_4_eq_3(self) -> None:
        neighbours_0_0 = utils.get_neighbour_coordinates((0, 0))
        assert len(neighbours_0_0) == 3

    def test_get_neighbour_coordinates_0_3_4_4_eq_3(self) -> None:
        neighbours_0_9 = utils.get_neighbour_coordinates((0, 9))
        assert len(neighbours_0_9) == 3

    def test_get_neighbour_coordinates_3_0_4_4_eq_3(self) -> None:
        neighbours_9_0 = utils.get_neighbour_coordinates((9, 0))
        assert len(neighbours_9_0) == 3

    def test_get_neighbour_coordinates_3_3_4_4_eq_3(self) -> None:
        neighbours_9_9 = utils.get_neighbour_coordinates((9, 9))
        assert len(neighbours_9_9) == 3

    def test_get_neighbour_coordinates_1_0_4_4_eq_5(self) -> None:
        neighbours_1_0 = utils.get_neighbour_coordinates((1, 0))
        assert len(neighbours_1_0) == 5

    def test_get_neighbour_coordinates_1_1_4_4_eq_8(self) -> None:
        neighbours_5_5 = utils.get_neighbour_coordinates((5, 5))
        assert len(neighbours_5_5) == 8
