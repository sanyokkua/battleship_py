import enum


class ShipType(enum.Enum):
    PatrolBoat = 0
    Submarine = 1
    Destroyer = 2
    Battleship = 3
    Carrier = 4


class State(enum.Enum):
    DESTROYED = 0
    WOUNDED = 1
    INTACT = 2


class Direction(enum.Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class BaseShip:
    def __init__(
        self,
        length: int,
        main_coordinate: tuple[int, int],
        direction: Direction = Direction.HORIZONTAL,
    ) -> None:
        self._length: int = length
        self._main_coordinate: tuple[int, int] = main_coordinate
        self._direction: Direction = direction
        self._state: State = State.INTACT
        self._coordinates: list[tuple[int, int]] = []
        self._update_coordinates()

    @property
    def lenght(self) -> int:
        return self._length

    @property
    def main_coordinate(self) -> tuple[int, int]:
        return self._main_coordinate

    @main_coordinate.setter
    def main_coordinate(self, value: tuple[int, int]) -> None:
        self._main_coordinate = value
        self._update_coordinates()

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        self._state = value

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, value: Direction) -> None:
        self._direction = value

    @property
    def coordinates(self) -> list[tuple[int, int]]:
        return self._coordinates

    def _update_coordinates(self) -> None:
        self._coordinates.clear()
        row, column = self._main_coordinate
        if self.direction == Direction.VERTICAL:
            for diff in range(self.lenght):
                self._coordinates.append((row + diff, column))
        else:
            for diff in range(self.lenght):
                self._coordinates.append((row, column + diff))
