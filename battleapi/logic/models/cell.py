class Cell:
    def __init__(
        self,
        row: int,
        column: int,
        has_ship: bool = False,
        has_shot: bool = False,
        is_free: bool = True,
    ) -> None:
        self._row: int
        self._column: int
        self._has_ship: bool = has_ship
        self._has_shot: bool = has_ship
        self._is_free: bool = is_free

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def has_ship(self) -> bool:
        return self._has_ship

    @has_ship.setter
    def has_ship(self, value: bool) -> None:
        self._has_ship = value

    @property
    def has_shot(self) -> bool:
        return self._has_shot

    @has_shot.setter
    def has_shot(self, value: bool) -> None:
        self._has_shot = value

    @property
    def is_free(self) -> bool:
        return self._is_free

    @is_free.setter
    def is_free(self, value: bool) -> None:
        self._is_free = value
