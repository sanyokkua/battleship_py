"""Definition of the abstract configuration."""
import abc
import enum
import logging

import battleapi.logic.models as models

log: logging.Logger = logging.getLogger(__name__)

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
        log.debug("amount_mapping: %s", amount_mapping)
        log.debug("size_mapping: %s", size_mapping)
        return list_of_ships


class ClassicGameConfiguration(GameConfiguration):
    """_summary_

    Args:
        config (_type_): _description_
    """

    def get_size_mapping(self) -> dict[models.ShipType, Size]:
        """_summary_

        Returns:
            dict[models.ShipType, int]: _description_
        """
        return {
            models.ShipType.PatrolBoat: 1,
            models.ShipType.Submarine: 2,
            models.ShipType.Destroyer: 3,
            models.ShipType.Battleship: 4,
        }

    def get_amount_mapping(self) -> dict[models.ShipType, Amount]:
        """_summary_

        Returns:
            dict[models.ShipType, int]: _description_
        """
        return {
            models.ShipType.PatrolBoat: 4,
            models.ShipType.Submarine: 3,
            models.ShipType.Destroyer: 2,
            models.ShipType.Battleship: 1,
        }


class CustomGameConfiguration(GameConfiguration):
    """_summary_

    Args:
        config (_type_): _description_
    """

    def get_size_mapping(self) -> dict[models.ShipType, Size]:
        """_summary_

        Returns:
            dict[models.ShipType, int]: _description_
        """
        return {
            models.ShipType.Submarine: 2,
            models.ShipType.Destroyer: 3,
            models.ShipType.Battleship: 4,
            models.ShipType.Carrier: 5,
        }

    def get_amount_mapping(self) -> dict[models.ShipType, Amount]:
        """_summary_

        Returns:
            dict[models.ShipType, int]: _description_
        """
        return {
            models.ShipType.Submarine: 4,
            models.ShipType.Destroyer: 3,
            models.ShipType.Battleship: 2,
            models.ShipType.Carrier: 1,
        }
