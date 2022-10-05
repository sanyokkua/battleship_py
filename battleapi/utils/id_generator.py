"""Implementation of the ID generator functionality."""
import logging
import uuid

import battleapi.abstract as types

log: logging.Logger = logging.getLogger(__name__)


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
        gen_id = str(uuid.uuid4())
        log.debug("Generated id: %s", gen_id)
        return gen_id
