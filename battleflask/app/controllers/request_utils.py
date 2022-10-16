"""Utility functions for requests."""
import logging

import flask

log: logging.Logger = logging.getLogger(__name__)


def get_form_string(key: str, default_value: str = "") -> str:
    """Retrieve string value from the form in request.

    Args:
        key (str): form input name.
        default_value (str, optional): Default value if not found. Defaults to "".

    Returns:
        str: string value for form key.
    """
    log.debug("key: %s, default: %s", key, default_value)
    # noinspection PyBroadException
    try:
        value: str = flask.request.form[key]
        if value and len(value.strip()) > 0:
            return value.strip()
        return default_value
    except Exception:
        return default_value


def get_form_int(key: str, default_value: int = -1) -> int:
    """Retrieve integer value from the form in request.

    Args:
        key (str): form input name.
        default_value (int, optional): Default value if not found. Defaults to -1.

    Returns:
        int: integer value for form key.
    """
    log.debug("key: %s, default: %d", key, default_value)
    # noinspection PyBroadException
    try:
        value: str = flask.request.form[key]
        if value and len(value.strip()) > 0:
            return int(value.strip())
        return default_value
    except Exception:
        return default_value


def get_cookies_string(key: str, default_value: str = "") -> str:
    """Retrieve string value from the user cookies in request.

    Args:
        key (str): cookie key
        default_value (str, optional): Default value if not found. Defaults to "".

    Returns:
        str: string value.
    """
    log.debug("key: %s, default: %s", key, default_value)
    # noinspection PyBroadException
    try:
        value: str = flask.request.cookies.get(key)
        if value and len(value.strip()) > 0:
            return value.strip()
        return default_value
    except Exception:
        return default_value
