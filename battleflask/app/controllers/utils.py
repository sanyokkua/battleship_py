"""Utility functions."""
import battleapi.api.dto as dto


def get_ship_id(ships: list[dto.ShipDto] | None) -> str:
    """Get ship id.

    Args:
        ships (list[dto.ShipDto] | None): ships list.

    Returns:
        str: ship id.
    """
    return ships[0].ship_id if ships is not None and len(ships) > 0 else ""


def get_ship_direction(ships: list[dto.ShipDto] | None) -> str:
    """Get ship direction.

    Args:
        ships (list[dto.ShipDto] | None): ships list.

    Returns:
        str: ship direction.
    """
    return ships[0].direction if ships is not None and len(ships) > 0 else ""
