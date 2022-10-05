"""Implementation of the ID generator functionality."""
import uuid

import battleapi.abstract as types


class Uuid4IdGenerator(types.IdGenerator):
    """Implementation for the ID generation.

    Args:
        abstract.IdGenerator (_type_): Inherited interface.
    """

    def generate_id(self) -> str:
        """Generate string that can be used as an identifier.

        Returns:
            str: generated id-like string.
        """
        return str(uuid.uuid4())