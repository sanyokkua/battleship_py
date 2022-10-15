"""_summary_

    Returns:
        _type_: _description_
"""
import logging

import flask

log: logging.Logger = logging.getLogger(__name__)


def get_form_string(key: str, default_value: str = "") -> str:
    """_summary_

    Args:
        key (str): _description_
        default_value (str, optional): _description_. Defaults to "".

    Returns:
        str: _description_
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
    """_summary_

    Args:
        key (str): _description_
        default_value (int, optional): _description_. Defaults to -1.

    Returns:
        int: _description_
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
    """_summary_

    Args:
        key (str): _description_
        default_value (str, optional): _description_. Defaults to "".

    Returns:
        str: _description_
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
