"""Definition of the abstract configuration."""
import abc
import enum
import logging

import battleapi.logic.models as models

log: logging.Logger = logging.getLogger(__name__)

Amount = int
Size = int


class GameType(enum.Enum):
    """Type of the game.

    Based on the type of rules there are 2 types of game.
    """

    CLASSIC = 0
    CUSTOM = 1


class GameConfiguration(abc.ABC):
    """Abstract configuration representation.

    Args:
        abc (_type_): Inherited class.

    Returns:
        _type_: GameConfiguration
    """

    @abc.abstractmethod
    def get_size_mapping(self) -> dict[models.ShipType, int]:
        """Return mapping of the ShipType to its Size in cells amount.

        Returns:
            dict[models.ShipType, int]: ship_type to size map.
        """

    @abc.abstractmethod
    def get_amount_mapping(self) -> dict[models.ShipType, int]:
        """Return mapping of the ShipType to its amount available for player.

        Returns:
            dict[models.ShipType, int]: ship_type to amount map.
        """

    def get_ship_configs(self) -> set[models.ShipConfig]:
        """Return configuration collected on the ship sizes and ship amounts.

        Returns:
            set[models.ShipConfig]: set of the ships.
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
    """Classic Game Configuration.

    Ship sizes starts from 1 and ends with 4.

    Args:
        config (_type_): GameConfiguration
    """

    def get_size_mapping(self) -> dict[models.ShipType, Size]:
        """Return mapping of the ShipType to its Size in cells amount.

        Returns:
            dict[models.ShipType, int]: ship_type to size map.
        """
        return {
            models.ShipType.PatrolBoat: 1,
            models.ShipType.Submarine: 2,
            models.ShipType.Destroyer: 3,
            models.ShipType.Battleship: 4,
        }

    def get_amount_mapping(self) -> dict[models.ShipType, Amount]:
        """Return mapping of the ShipType to its amount available for player.

        Returns:
            dict[models.ShipType, int]: ship_type to amount map.
        """
        return {
            models.ShipType.PatrolBoat: 4,
            models.ShipType.Submarine: 3,
            models.ShipType.Destroyer: 2,
            models.ShipType.Battleship: 1,
        }


class CustomGameConfiguration(GameConfiguration):
    """Custom Game Configuration.

    Ship sizes starts from 2 and ends with 5.

    Args:
        config (_type_): GameConfiguration
    """

    def get_size_mapping(self) -> dict[models.ShipType, Size]:
        """Return mapping of the ShipType to its Size in cells amount.

        Returns:
            dict[models.ShipType, int]: ship_type to size map.
        """
        return {
            models.ShipType.Submarine: 2,
            models.ShipType.Destroyer: 3,
            models.ShipType.Battleship: 4,
            models.ShipType.Carrier: 5,
        }

    def get_amount_mapping(self) -> dict[models.ShipType, Amount]:
        """Return mapping of the ShipType to its amount available for player.

        Returns:
            dict[models.ShipType, int]: ship_type to amount map.
        """
        return {
            models.ShipType.Submarine: 4,
            models.ShipType.Destroyer: 3,
            models.ShipType.Battleship: 2,
            models.ShipType.Carrier: 1,
        }
