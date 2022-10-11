import battleapi.api.dto as dto


def get_ship_id(ships: list[dto.ShipDto] | None) -> str:
    return ships[0].ship_id if ships is not None and len(ships) > 0 else ""


def get_ship_direction(ships: list[dto.ShipDto] | None) -> str:
    return ships[0].direction if ships is not None and len(ships) > 0 else ""
