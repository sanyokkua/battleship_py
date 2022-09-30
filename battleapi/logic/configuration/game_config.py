"""Definition of the abstract configuration."""
import abc
import enum

import battleapi.logic.models as models

Amount = int
Size = int


class GameType(enum.Enum):
    """_summary_

    Args:
        enum (_type_): _description_
    """

    CLASSIC = 0
    CUSTOM = 1


class GameConfiguration(abc.ABC):
    """_summary_

    Args:
        abc (_type_): _description_

    Returns:
        _type_: _description_
    """

    @abc.abstractmethod
    def get_size_mapping(self) -> dict[models.ShipType, int]:
        """_summary_

        Returns:
            dict[models.ShipType, int]: _description_
        """

    @abc.abstractmethod
    def get_amount_mapping(self) -> dict[models.ShipType, int]:
        """_summary_

        Returns:
            dict[models.ShipType, int]: _description_
        """

    def get_ship_configs(self) -> set[models.ShipConfig]:
        """_summary_

        Returns:
            set[models.ShipConfig]: _description_
        """
        list_of_ships: set[models.ShipConfig] = set()
        amount_mapping: dict[models.ShipType, Amount] = self.get_amount_mapping()
        size_mapping: dict[models.ShipType, Size] = self.get_size_mapping()
        for (ship_type, ship_size) in size_mapping.items():
            ship_amount: int = amount_mapping[ship_type]
            ship: models.ShipConfig = models.ShipConfig(
                ship_type=ship_type,
                ship_size=ship_size,
                ship_amount=ship_amount,
            )
            list_of_ships.add(ship)
        return list_of_ships
