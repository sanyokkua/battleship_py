"""Utility module that contains all the logic for rendering all available pages."""
import logging

import flask
import werkzeug

import battleapi.api.dto as dto
import battleflask.app.controllers.constants as const

URL_GET_INDEX = "_get_index_page"
URL_GET_NEW = "_get_new_game_page"
URL_GET_JOIN = "_get_join_game_page"
URL_POST_START = "_post_start_redirect_to_wait_page"
URL_POST_JOIN = "_post_join_redirect_to_prepare_page"

URL_GET_ID_PREPARE = "_get_session_prepare_page"
URL_GET_ID_WAIT = "_get_session_wait_page"

URL_GET_ID_GAMEPLAY = "_get_session_gameplay_page"
URL_GET_ID_FINISH = "_get_session_finish_page"

URL_POST_ID_PREPARE_DELSHIP = "_post_session_prepare_delship_redirect_to_prepare_page"
URL_POST_ID_PREPARE_CHOSE = "_post_session_prepare_chose_ship_redirect_to_prepare_page"
URL_POST_ID_PREPARE_ADD_SHIP = "_post_session_prepare_addship_redirect_to_prepare_page"
URL_POST_ID_GAMEPLAY_START = "_post_session_gameplay_start_redirect_to_gameplay_page"
URL_POST_ID_GAMEPLAY_SHOT = "_post_session_gameplay_shot_redirect_to_gameplay_page"

log: logging.Logger = logging.getLogger(__name__)


def render_index_page(url_last_page_url: str = "", last_page_name: str = "") -> str:
    """Render index page.

    Args:
        url_last_page_url (str, optional): Last page for active game session.
            Defaults to "".
        last_page_name (str, optional): Last page name for active game session.
            Defaults to "".

    Returns:
        str: rendered index page.
    """
    url_get_new_game_view: str = gen_url_index(URL_GET_NEW)
    url_get_join_game_view: str = gen_url_index(URL_GET_JOIN)
    log.debug("url_get_new_game_view: %s", url_get_new_game_view)
    log.debug("url_get_join_game_view: %s", url_get_join_game_view)
    log.debug("url_last_page_url: %s", url_last_page_url)
    log.debug("last_page_name: %s", last_page_name)

    return flask.render_template(
        "index/index_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
        url_last_page_url=url_last_page_url,
        last_page_name=last_page_name,
    )


def render_new_game_page(
    url_last_page_url: str = "",
    last_page_name: str = "",
    errors: list[str] | None = None,
) -> str:
    """Render new game page.

    Args:
        url_last_page_url (str, optional): Last page for active game session.
            Defaults to "".
        last_page_name (str, optional): Last page name for active game session.
            Defaults to "".
        errors (list[str] | None, optional): any errors to show. Defaults to None.

    Returns:
        str: _description_
    """
    url_get_new_game_view: str = gen_url_index(URL_GET_NEW)
    url_get_join_game_view: str = gen_url_index(URL_GET_JOIN)
    url_post_start_game_session: str = gen_url_players(URL_POST_START)

    log.debug("url_get_new_game_view: %s", url_get_new_game_view)
    log.debug("url_get_join_game_view: %s", url_get_join_game_view)
    log.debug("url_post_start_game_session: %s", url_post_start_game_session)
    log.debug("url_last_page_url: %s", url_last_page_url)
    log.debug("last_page_name: %s", last_page_name)

    return flask.render_template(
        "index/new_game_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
        url_post_start_game_session=url_post_start_game_session,
        url_last_page_url=url_last_page_url,
        last_page_name=last_page_name,
        errors_list=errors,
    )


def render_join_game_page(
    url_last_page_url: str = "",
    last_page_name: str = "",
    errors: list[str] | None = None,
) -> str:
    """Render join game page.

    Args:
        url_last_page_url (str, optional): Last page for active game session.
            Defaults to "".
        last_page_name (str, optional): Last page name for active game session.
            Defaults to "".
        errors (list[str] | None, optional):  any errors to show. Defaults to None.

    Returns:
        str: rendered join game page.
    """
    url_get_new_game_view: str = gen_url_index(URL_GET_NEW)
    url_get_join_game_view: str = gen_url_index(URL_GET_JOIN)
    url_post_join_game_session: str = gen_url_players(URL_POST_JOIN)

    log.debug("url_get_new_game_view: %s", url_get_new_game_view)
    log.debug("url_get_join_game_view: %s", url_get_join_game_view)
    log.debug("url_post_join_game_session: %s", url_post_join_game_session)
    log.debug("url_last_page_url: %s", url_last_page_url)
    log.debug("last_page_name: %s", last_page_name)

    return flask.render_template(
        "index/join_game_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
        url_post_join_game_session=url_post_join_game_session,
        url_last_page_url=url_last_page_url,
        last_page_name=last_page_name,
        errors_list=errors,
    )


def render_wait_page(
    session_id: str,
    player_name: str,
    opponent_name: str,
    url_last_page_url: str = "",
    last_page_name: str = "",
) -> str:
    """Render wait page.

    Args:
        session_id (str): current game session id.
        player_name (str): current player name.
        opponent_name (str): opponent name (if joined).
        url_last_page_url (str, optional): Last page for active game session.
            Defaults to "".
        last_page_name (str, optional): Last page name for active game session.
            Defaults to "".

    Returns:
        str: rendered wait page.
    """
    url_get_new_game_view: str = gen_url_index(URL_GET_NEW)
    url_get_join_game_view: str = gen_url_index(URL_GET_JOIN)
    url_get_update: str = gen_url_game(URL_GET_ID_WAIT, session_id)
    url_get_prepare: str = gen_url_prepare(URL_GET_ID_PREPARE, session_id)

    log.debug("url_get_new_game_view: %s", url_get_new_game_view)
    log.debug("url_get_join_game_view: %s", url_get_join_game_view)
    log.debug("url_get_update: %s", url_get_update)
    log.debug("url_get_prepare: %s", url_get_prepare)
    log.debug("url_last_page_url: %s", url_last_page_url)
    log.debug("last_page_name: %s", last_page_name)

    return flask.render_template(
        "game/game_session_wait_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
        url_get_update=url_get_update,
        url_get_prepare=url_get_prepare,
        player_name=player_name,
        game_session_id=session_id,
        opponent_name=opponent_name,
        url_last_page_url=url_last_page_url,
        last_page_name=last_page_name,
    )


def render_prepare_page(
    session_id: str,
    player_name: str,
    opponent_name: str,
    opponent_status: bool,
    ships_list: list[dto.ShipDto],
    field: list[list[dto.CellDto]],
    active_ship: str,
    active_ship_direction: str,
    url_last_page_url: str = "",
    last_page_name: str = "",
    errors: list[str] | None = None,
) -> str:
    """Render prepare stage game page.

    Args:
        session_id (str): current game session id.
        player_name (str): current player name.
        opponent_name (str): opponent player name.
        opponent_status (bool): opponent status (if opponent started game -
            True will be returned)
        ships_list (list[dto.ShipDto]): current player available ships.
        field (list[list[dto.CellDto]]): current player game field (board).
        active_ship (str): ship that can be added to the field.
        active_ship_direction (str): ship direction.
        url_last_page_url (str, optional): Last page for active game session.
            Defaults to "".
        last_page_name (str, optional): Last page name for active game session.
            Defaults to "".
        errors (list[str] | None, optional):  any errors to show. Defaults to None.

    Returns:
        str: rendered game preparation stage page.
    """
    url_get_new_game_view: str = gen_url_index(URL_GET_NEW)
    url_get_join_game_view: str = gen_url_index(URL_GET_JOIN)
    url_post_start: str = gen_url_gameplay(URL_POST_ID_GAMEPLAY_START, session_id)
    url_post_addship: str = gen_url_prepare(URL_POST_ID_PREPARE_ADD_SHIP, session_id)
    url_post_chose_ship: str = gen_url_prepare(URL_POST_ID_PREPARE_CHOSE, session_id)
    url_post_delship: str = gen_url_prepare(URL_POST_ID_PREPARE_DELSHIP, session_id)

    log.debug("url_get_new_game_view: %s", url_get_new_game_view)
    log.debug("url_get_join_game_view: %s", url_get_join_game_view)
    log.debug("url_post_start: %s", url_post_start)
    log.debug("url_post_addship: %s", url_post_addship)
    log.debug("url_post_chose_ship: %s", url_post_chose_ship)
    log.debug("url_post_delship: %s", url_post_delship)
    log.debug("url_last_page_url: %s", url_last_page_url)
    log.debug("last_page_name: %s", last_page_name)

    return flask.render_template(
        "game/game_session_prepare_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
        url_post_start=url_post_start,
        url_post_addship=url_post_addship,
        url_post_chose_ship=url_post_chose_ship,
        url_post_delship=url_post_delship,
        player_name=player_name,
        opponent_name=opponent_name,
        opponent_status=opponent_status,
        ships_list=ships_list,
        field=field,
        active_ship_id=active_ship,
        active_ship_direction=active_ship_direction,
        url_last_page_url=url_last_page_url,
        last_page_name=last_page_name,
        errors_list=errors,
    )


def render_gameplay_page(
    session_id: str,
    current_player_name: str,
    opponent_name: str,
    active_player_name: str,
    number_of_cells_self: int,
    number_of_cells_opponent: int,
    player_field: list[list[dto.CellDto]],
    opponent_field: list[list[dto.CellDto]],
    is_opponent_ready: bool,
    url_last_page_url: str = "",
    last_page_name: str = "",
    errors: list[str] | None = None,
) -> str:
    """Render gameplay page.

    Args:
        session_id (str): game session id.
        current_player_name (str): current player name.
        opponent_name (str): opponent name,
        active_player_name (str): player who should do the turn (shot).
        number_of_cells_self (int): number of cells left without shots in the player
            field.
        number_of_cells_opponent (int): number of cells left without shots in the
            opponent field.
        player_field (list[list[dto.CellDto]]): player field.
        opponent_field (list[list[dto.CellDto]]): opponent field.
        is_opponent_ready (bool): True if the opponent finished preparation stage.
        url_last_page_url (str, optional): Last page for active game session.
            Defaults to "".
        last_page_name (str, optional): Last page name for active game session.
            Defaults to "".
        errors (list[str] | None, optional): any errors to show. Defaults to None.

    Returns:
        str: _description_
    """
    url_get_new_game_view: str = gen_url_index(URL_GET_NEW)
    url_get_join_game_view: str = gen_url_index(URL_GET_JOIN)
    url_post_shot: str = gen_url_gameplay(URL_POST_ID_GAMEPLAY_SHOT, session_id)
    url_get_update: str = gen_url_gameplay(URL_GET_ID_GAMEPLAY, session_id)

    log.debug("url_get_new_game_view: %s", url_get_new_game_view)
    log.debug("url_get_join_game_view: %s", url_get_join_game_view)
    log.debug("url_post_shot: %s", url_post_shot)
    log.debug("url_get_update: %s", url_get_update)
    log.debug("url_last_page_url: %s", url_last_page_url)
    log.debug("last_page_name: %s", last_page_name)

    return flask.render_template(
        "game/game_session_gameplay_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
        url_post_shot=url_post_shot,
        url_get_update=url_get_update,
        current_player_name=current_player_name,
        opponent_name=opponent_name,
        active_player_name=active_player_name,
        number_of_cells_self=number_of_cells_self,
        number_of_cells_opponent=number_of_cells_opponent,
        player_field=player_field,
        opponent_field=opponent_field,
        is_opponent_ready=is_opponent_ready,
        url_last_page_url=url_last_page_url,
        last_page_name=last_page_name,
        errors_list=errors,
    )


def render_finish_page(
    session_id: str,
    winner_player_name: str,
    current_player_name: str,
    opponent_name: str,
    player_field: list[list[dto.CellDto]],
    opponent_field: list[list[dto.CellDto]],
    url_last_page_url: str = "",
    last_page_name: str = "",
) -> str:
    """Render result page of the game.

    Args:
        session_id (str): game session id.
        winner_player_name (str): winner player name.
        current_player_name (str): current player name.
        opponent_name (str): opponent name.
        player_field (list[list[dto.CellDto]]): player field.
        opponent_field (list[list[dto.CellDto]]): opponent field.
        url_last_page_url (str, optional): Last page for active game session.
            Defaults to "".
        last_page_name (str, optional): Last page name for active game session.
            Defaults to "".

    Returns:
        str: rendered results page.
    """
    url_get_new_game_view: str = gen_url_index(URL_GET_NEW)
    url_get_join_game_view: str = gen_url_index(URL_GET_JOIN)
    url_get_index: str = gen_url_index(URL_GET_INDEX)

    log.debug("url_get_new_game_view: %s", url_get_new_game_view)
    log.debug("url_get_join_game_view: %s", url_get_join_game_view)
    log.debug("url_get_index: %s", url_get_index)
    log.debug("url_last_page_url: %s", url_last_page_url)
    log.debug("last_page_name: %s", last_page_name)

    return flask.render_template(
        "game/game_session_finish_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
        url_get_index=url_get_index,
        session_id=session_id,
        winner_player_name=winner_player_name,
        current_player_name=current_player_name,
        opponent_name=opponent_name,
        player_field=player_field,
        opponent_field=opponent_field,
        url_last_page_url=url_last_page_url,
        last_page_name=last_page_name,
    )


def gen_url(blue_print: str, method: str, session: str) -> str:
    """Generate url for blueprint method in the session.

    Args:
        blue_print (str): controller name.
        method (str): function name that should process request.
        session (str): game session id.

    Returns:
        str: generated url.
    """
    log.debug("blue_print: %s, method: %s, session: %s", blue_print, method, session)
    return flask.url_for(f"{blue_print}.{method}", session_id=session)


def gen_url_index(method: str, session: str = "") -> str:
    """Generate url for index controller.

    Args:
        method (str): function name that should process request.
        session (str, optional): game session id. Defaults to "".

    Returns:
        str: generated url.
    """
    return gen_url(const.CONTROLLER_INDEX, method, session)


def gen_url_game(method: str, session: str = "") -> str:
    """Generate url for game controller.

    Args:
        method (str): function name that should process request.
        session (str, optional): game session id. Defaults to "".

    Returns:
        str: generated url.
    """
    return gen_url(const.CONTROLLER_GAME_COMMON, method, session)


def gen_url_players(method: str, session: str = "") -> str:
    """Generate url for players controller.

    Args:
        method (str): function name that should process request.
        session (str, optional): game session id. Defaults to "".

    Returns:
        str: generated url.
    """
    return gen_url(const.CONTROLLER_PLAYERS, method, session)


def gen_url_prepare(method: str, session: str = "") -> str:
    """Generate url for preparation controller.

    Args:
        method (str): function name that should process request.
        session (str, optional): game session id. Defaults to "".

    Returns:
        str: generated url.
    """
    return gen_url(const.CONTROLLER_PREPARATION, method, session)


def gen_url_gameplay(method: str, session: str = "") -> str:
    """Generate url for gameplay controller.

    Args:
        method (str): function name that should process request.
        session (str, optional): game session id. Defaults to "".

    Returns:
        str: generated url.
    """
    return gen_url(const.CONTROLLER_GAMEPLAY, method, session)


def gen_redirect(
    blue_print: str, method_name: str, session_id: str, page_name: str = ""
) -> werkzeug.Response:
    """Generate redirect to the controller function that will render page.

    Args:
        blue_print (str): controller name.
        method_name (str): function name that should process request.
        session_id (str): game session id
        page_name (str, optional): name of last page was rendered. Defaults to "".

    Returns:
        werkzeug.Response: redirect response.
    """
    log.debug(
        "blue_print: %s, method: %s, session: %s", blue_print, method_name, session_id
    )
    url: str = gen_url(blue_print, method_name, session_id)
    response: werkzeug.Response = flask.redirect(url)
    response.set_cookie(const.COOKIE_LAST_URL, url)
    response.set_cookie(const.COOKIE_LAST_PAGE, page_name)
    log.debug("response: %s", response)
    return response


def redirect_to_id_prepare_page(session_id: str) -> werkzeug.Response:
    """Redirect to the preparation page.

    Args:
        session_id (str): game session id.

    Returns:
        werkzeug.Response: redirect response.
    """
    return gen_redirect(
        const.CONTROLLER_PREPARATION, URL_GET_ID_PREPARE, session_id, "Prepare"
    )


def redirect_to_id_wait_page(session_id: str) -> werkzeug.Response:
    """Redirect to the wait for players page.

    Args:
        session_id (str): game session id

    Returns:
        werkzeug.Response: redirect response.
    """
    return gen_redirect(
        const.CONTROLLER_GAME_COMMON, URL_GET_ID_WAIT, session_id, "Wait"
    )


def redirect_to_id_finish_page(session_id: str) -> werkzeug.Response:
    """Redirect to the results page.

    Args:
        session_id (str): game session id

    Returns:
        werkzeug.Response: redirect response.
    """
    return gen_redirect(
        const.CONTROLLER_GAME_COMMON, URL_GET_ID_FINISH, session_id, "Results"
    )


def redirect_to_id_gameplay_page(session_id: str) -> werkzeug.Response:
    """Redirect to the gameplay page.

    Args:
        session_id (str): game session id

    Returns:
        werkzeug.Response: redirect response.
    """
    return gen_redirect(
        const.CONTROLLER_GAMEPLAY, URL_GET_ID_GAMEPLAY, session_id, "Gameplay"
    )
