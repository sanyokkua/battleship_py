"""_summary_

    Returns:
        _type_: _description_
"""
import logging

import flask

import battleflask.app.controllers.constants as const

log: logging.Logger = logging.getLogger(__name__)


def render_new_game_page(errors: list[str] | None = None) -> str:
    """_summary_

    Args:
        errors (list[str] | None, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    url_post_start_game_session: str = flask.url_for(
        f"{const.BLUE_PRINT_GAME}._post_start_redirect_to_wait_page"
    )
    log.debug("url_post_start_game_session: %s", url_post_start_game_session)

    return flask.render_template(
        "index/new_game_page.html",
        url_post_start_game_session=url_post_start_game_session,
        errors_list=errors,
    )


def render_join_game_page(errors: list[str] | None = None) -> str:
    """_summary_

    Args:
        errors (list[str] | None, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    url_join_game_session: str = flask.url_for(
        f"{const.BLUE_PRINT_GAME}._post_join_redirect_to_prepare_page"
    )
    log.debug("url_join_game_session: %s", url_join_game_session)

    return flask.render_template(
        "index/join_game_page.html",
        url_join_game_session=url_join_game_session,
        errors_list=errors,
    )


def render_wait_page(
    session_id: str, current_player_name: str, opponent_name: str
) -> str:
    """_summary_

    Args:
        session_id (str): _description_
        current_player_name (str): _description_
        opponent_name (str): _description_

    Returns:
        str: _description_
    """
    url_get_update: str = url_for_session("_get_session_wait_page", session_id)
    url_get_prepare: str = url_for_session("_get_session_prepare_page", session_id)
    log.debug("url_get_update: %s", url_get_update)
    log.debug("url_get_prepare: %s", url_get_prepare)

    return flask.render_template(
        "game/game_session_wait_page.html",
        url_get_update=url_get_update,
        url_get_prepare=url_get_prepare,
        current_player_name=current_player_name,
        game_session_id=session_id,
        opponent_name=opponent_name,
    )


def render_prepare_page(
    session_id: str,
    current_player_name: str,
    opponent_status: str,
    ships_list: [],
    field: list[list],
    errors: list[str] | None = None,
) -> str:
    """_summary_

    Args:
        session_id (str): _description_
        current_player_name (str): _description_
        opponent_status (str): _description_
        ships_list (_type_): _description_
        field (list[list]): _description_
        errors (list[str] | None, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    url_post_start: str = url_for_session(
        "_post_session_gameplay_start_redirect_to_gameplay_page", session_id
    )
    url_post_addship: str = url_for_session(
        "_post_session_prepare_addship_redirect_to_prepare_page", session_id
    )
    url_post_delship: str = url_for_session(
        "_post_session_prepare_delship_redirect_to_prepare_page", session_id
    )
    url_get_opponent: str = url_for_session("_get_session_prepare_opponent", session_id)
    log.debug("url_post_start: %s", url_post_start)
    log.debug("url_post_addship: %s", url_post_addship)
    log.debug("url_post_delship: %s", url_post_delship)
    log.debug("url_get_opponent: %s", url_get_opponent)

    return flask.render_template(
        "game/game_session_prepare_page.html",
        url_post_start=url_post_start,
        url_post_addship=url_post_addship,
        url_post_delship=url_post_delship,
        url_get_opponent=url_get_opponent,
        current_player_name=current_player_name,
        opponent_status=opponent_status,
        ships_list=ships_list,
        field=field,
        errors_list=errors,
    )


def render_gameplay_page(
    session_id: str,
    current_player_name: str,
    opponent_name: str,
    active_player_name: str,
    number_of_cells_self: int,
    number_of_cells_opponent: int,
    player_field: list[list],
    opponent_field: list[list],
    errors: list[str] | None = None,
) -> str:
    """_summary_

    Args:
        session_id (str): _description_
        current_player_name (str): _description_
        opponent_name (str): _description_
        active_player_name (str): _description_
        number_of_cells_self (int): _description_
        number_of_cells_opponent (int): _description_
        player_field (list[list]): _description_
        opponent_field (list[list]): _description_
        errors (list[str] | None, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    url_post_shot: str = url_for_session(
        "_post_session_gameplay_shot_redirect_to_gameplay_page", session_id
    )
    url_get_update: str = url_for_session("_get_session_gameplay_page", session_id)
    log.debug("url_post_shot: %s", url_post_shot)
    log.debug("url_get_update: %s", url_get_update)

    return flask.render_template(
        "game/game_session_gameplay_page.html",
        url_post_shot=url_post_shot,
        url_get_update=url_get_update,
        current_player_name=current_player_name,
        opponent_name=opponent_name,
        active_player_name=active_player_name,
        number_of_cells_self=number_of_cells_self,
        number_of_cells_opponent=number_of_cells_opponent,
        player_field=player_field,
        opponent_field=opponent_field,
        errors_list=errors,
    )


def render_finish_page(session_id: str, winner_player_name: str) -> str:
    """_summary_

    Args:
        session_id (str): _description_
        winner_player_name (str): _description_

    Returns:
        str: _description_
    """
    url_get_index: str = flask.url_for(f"{const.BLUE_PRINT_INDEX}._get_index_page")
    log.debug("url_get_index: %s", url_get_index)

    return flask.render_template(
        "game/game_session_finish_page.html",
        url_get_index=url_get_index,
        session_id=session_id,
        winner_player_name=winner_player_name,
    )


def url_for_session(method_name: str, session_id: str) -> str:
    """_summary_

    Args:
        method_name (str): _description_
        session_id (str): _description_

    Returns:
        str: _description_
    """
    log.debug("method_name: %s, session_id: %s", method_name, session_id)
    return flask.url_for(
        f"{const.BLUE_PRINT_GAME}.{method_name}", session_id=session_id
    )
