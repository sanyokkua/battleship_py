"""_summary_

Returns:
    _type_: _description_
"""
import battleapi.logic.configuration.game_config as gc
import battleapi.logic.models as models


class ClassicGameConfiguration(gc.GameConfiguration):
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
            models.ShipType.PatrolBoat: 1,
            models.ShipType.Submarine: 2,
            models.ShipType.Destroyer: 3,
            models.ShipType.Battleship: 4,
        }

    def get_amount_mapping(self) -> dict[models.ShipType, int]:
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
