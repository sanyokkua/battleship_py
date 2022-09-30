from battleapi.logic.configuration.custom_config import CustomGameConfiguration
from battleapi.logic.models import ShipType


class TestClassicConfig:
    def test_custom_config_values(self) -> None:
        config = CustomGameConfiguration()
        ship_configs = config.get_ship_configs()
        assert len(ship_configs) == 4
        for ship in ship_configs:
            if ship.ship_type == ShipType.PatrolBoat:
                assert False  # Shouldn't be for classic config
            elif ship.ship_type == ShipType.Submarine:
                assert ship.ship_size == 2
                assert ship.ship_amount == 4
            elif ship.ship_type == ShipType.Destroyer:
                assert ship.ship_size == 3
                assert ship.ship_amount == 3
            elif ship.ship_type == ShipType.Battleship:
                assert ship.ship_size == 4
                assert ship.ship_amount == 2
            elif ship.ship_type == ShipType.Carrier:
                assert ship.ship_size == 5
                assert ship.ship_amount == 1
