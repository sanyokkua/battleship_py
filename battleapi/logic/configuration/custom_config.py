"""_summary_

Returns:
    _type_: _description_
"""
import battleapi.logic.configuration.game_config as gc
import battleapi.logic.models as models


class CustomGameConfiguration(gc.GameConfiguration):
    """_summary_

    Args:
        gc (_type_): _description_
    """

    def get_size_mapping(self) -> dict[models.ShipType, int]:
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

    def get_amount_mapping(self) -> dict[models.ShipType, int]:
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
