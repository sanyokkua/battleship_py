"""_summary_

    Returns:
        _type_: _description_
"""
import logging

import flask
import werkzeug

import battleapi.api.dto as dto
import battleflask.app.context as ctx
import battleflask.app.controllers.constants as const
import battleflask.app.controllers.render_utils as render_utils
import battleflask.app.controllers.request_utils as request_utils
import battleflask.app.validation_utils as validation

log: logging.Logger = logging.getLogger(__name__)

GAME_BLUEPRINT: flask.Blueprint = flask.Blueprint(
    const.BLUE_PRINT_GAME, __name__, template_folder="templates", url_prefix="/game"
)


@GAME_BLUEPRINT.route("/start", methods=[const.METHOD_POST])
def _post_start_redirect_to_wait_page() -> werkzeug.Response:
    """_summary_

    Returns:
        werkzeug.Response: _description_
    """
    player_name: str = request_utils.get_form_string(const.FORM_PLAYER_NAME)
    log.debug("player_name: %s", player_name)
    validation.validate_is_not_empty_string(player_name)

    session_id: str = ctx.GAME_CONTROLLER_API.init_game_session()
    player: dto.PlayerDto = ctx.GAME_CONTROLLER_API.create_player_in_session(
        session_id, player_name
    )
    player_id: str = player.player_id
    log.debug("Created session: %s, player: %s", session_id, player)

    response: werkzeug.Response = flask.redirect(
        render_utils.url_for_session("_get_session_wait_page", session_id)
    )
    response.set_cookie(const.COOKIE_PLAYER_ID, player_id)
    response.set_cookie(const.COOKIE_SESSION_ID, session_id)
    log.debug("Response: %s", response)
    return response


@GAME_BLUEPRINT.route("/join", methods=[const.METHOD_POST])
def _post_join_redirect_to_prepare_page() -> werkzeug.Response:
    """_summary_

    Returns:
        werkzeug.Response: _description_
    """
    player_name: str = request_utils.get_form_string(const.FORM_PLAYER_NAME)
    session_id: str = request_utils.get_form_string(const.FORM_SESSION_ID)
    log.debug("player_name: %s", player_name)
    log.debug("session_id: %s", session_id)

    validation.validate_is_not_empty_string(player_name)
    validation.validate_is_not_empty_string(session_id)

    player: dto.PlayerDto = ctx.GAME_CONTROLLER_API.create_player_in_session(
        session_id, player_name
    )
    player_id: str = player.player_id
    log.debug("Created session: %s, player: %s", session_id, player)

    response: werkzeug.Response = flask.redirect(
        render_utils.url_for_session("_get_session_prepare_page", session_id)
    )
    response.set_cookie(const.COOKIE_PLAYER_ID, player_id)
    response.set_cookie(const.COOKIE_SESSION_ID, session_id)
    log.debug("Response: %s", response)
    return response


# GET


@GAME_BLUEPRINT.route("/<string:session_id>/wait", methods=[const.METHOD_GET])
def _get_session_wait_page(session_id: str) -> str:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        str: _description_
    """
    current_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("current_player_id: %s", current_player_id)
    validation.validate_is_not_empty_string(current_player_id)

    player: dto.PlayerDto = ctx.GAME_CONTROLLER_API.get_player_by_id(
        session_id, current_player_id
    )
    opponent: dto.PlayerDto | None = ctx.GAME_CONTROLLER_API.get_opponent(
        session_id, player.player_id
    )
    log.debug("Player: %s, opponent: %s", player, opponent)
    opponent_name = opponent.player_name if opponent is not None else ""
    return render_utils.render_wait_page(
        session_id=session_id,
        current_player_name=player.player_name,
        opponent_name=opponent_name,
    )


@GAME_BLUEPRINT.route("/<string:session_id>/prepare", methods=[const.METHOD_GET])
def _get_session_prepare_page(session_id: str) -> str:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        str: _description_
    """
    current_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    active_ship_id: str = request_utils.get_cookies_string(const.COOKIE_SHIP_ID)
    log.debug("value of current_player_id: %s", current_player_id)

    validation.validate_is_not_empty_string(current_player_id)

    player: dto.PlayerDto = ctx.GAME_CONTROLLER_API.get_player_by_id(
        session_id, current_player_id
    )
    opponent: dto.PlayerDto = ctx.GAME_CONTROLLER_API.get_opponent_prepare_status(
        session_id, current_player_id
    )
    log.debug("Player: %s, opponent: %s", player, opponent)
    ships_list: list[dto.ShipDto] = ctx.GAME_CONTROLLER_API.get_prepare_ships_list(
        session_id, current_player_id
    )
    field: list[list[dto.CellDto]] = ctx.GAME_CONTROLLER_API.get_prepare_player_field(
        session_id, current_player_id
    )
    log.debug("Ships: %s", ships_list)
    log.debug("Field: %s", field)
    ship_id_from_ships_list = ships_list[0].ship_id if len(ships_list) > 0 else ""
    ship_id: str = (
        active_ship_id if len(active_ship_id) > 0 else ship_id_from_ships_list
    )

    return render_utils.render_prepare_page(
        session_id=session_id,
        current_player_name=player.player_name,
        opponent_status=opponent.player_name,
        ships_list=ships_list,
        field=field,
        active_ship=ship_id,
    )


@GAME_BLUEPRINT.route("/<string:session_id>/gameplay", methods=[const.METHOD_GET])
def _get_session_gameplay_page(session_id: str) -> str:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        str: _description_
    """
    current_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("value: %s", current_player_id)

    validation.validate_is_not_empty_string(current_player_id)

    player: dto.PlayerDto = ctx.GAME_CONTROLLER_API.get_player_by_id(
        session_id, current_player_id
    )
    opponent: dto.PlayerDto = ctx.GAME_CONTROLLER_API.get_opponent(
        session_id, current_player_id
    )
    log.debug("Player: %s, opponent: %s", player, opponent)
    active_player_name: str = ctx.GAME_CONTROLLER_API.get_active_player(
        session_id
    ).player_name
    log.debug("active_player_name: %s", active_player_name)
    number_of_cells_self: int = ctx.GAME_CONTROLLER_API.get_number_of_cells_left(
        session_id, current_player_id
    )
    number_of_cells_opponent: int = ctx.GAME_CONTROLLER_API.get_number_of_cells_left(
        session_id, opponent.player_id
    )
    log.debug(
        "Cells self: %d, Cells opponent: %d", number_of_cells_self, number_of_cells_self
    )
    player_field: list[list] = ctx.GAME_CONTROLLER_API.get_field(
        session_id, current_player_id
    )
    opponent_field: list[list] = ctx.GAME_CONTROLLER_API.get_field(
        session_id, opponent.player_id, is_for_opponent=True
    )
    log.debug("Player Field: %s", player_field)
    log.debug("Opponent Field: %s", opponent_field)

    return render_utils.render_gameplay_page(
        session_id=session_id,
        current_player_name=player.player_name,
        opponent_name=opponent.player_name,
        active_player_name=active_player_name,
        number_of_cells_self=number_of_cells_self,
        number_of_cells_opponent=number_of_cells_opponent,
        player_field=player_field,
        opponent_field=opponent_field,
    )


@GAME_BLUEPRINT.route(
    "/<string:session_id>/prepare/opponent", methods=[const.METHOD_GET]
)
def _get_session_prepare_opponent(session_id: str) -> str:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        str: _description_
    """
    current_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("value: %s", current_player_id)

    validation.validate_is_not_empty_string(current_player_id)

    opponent: dto.PlayerDto = ctx.GAME_CONTROLLER_API.get_opponent(
        session_id, current_player_id
    )
    log.debug("Opponent: %s", opponent)
    return opponent.player_name


@GAME_BLUEPRINT.route("/<string:session_id>/finish", methods=[const.METHOD_GET])
def _get_session_finish_page(session_id: str) -> str:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        str: _description_
    """
    winner_player: dto.PlayerDto = ctx.GAME_CONTROLLER_API.get_winner(session_id)
    log.debug("winner: %s", winner_player)
    return render_utils.render_finish_page(session_id, winner_player.player_name)


@GAME_BLUEPRINT.route(
    "/<string:session_id>/prepare/addship", methods=[const.METHOD_POST]
)
def _post_session_prepare_addship_redirect_to_prepare_page(
    session_id: str,
) -> werkzeug.Response:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        werkzeug.Response: _description_
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    cookies_active_ship_id: str = request_utils.get_cookies_string(const.COOKIE_SHIP_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)
    log.debug("active_ship_id: %s", cookies_active_ship_id)

    validation.validate_is_not_empty_string(cookies_player_id)
    validation.validate_is_not_empty_string(cookies_session_id)
    validation.validate_is_not_empty_string(cookies_active_ship_id)

    assert cookies_session_id == session_id

    form_ship_id: str = request_utils.get_form_string(const.FORM_CELL_SHIP_ID)
    ship_coordinate_row: int = request_utils.get_form_int(const.FORM_COORDINATE_ROW)
    ship_coordinate_column: int = request_utils.get_form_int(
        const.FORM_COORDINATE_COLUMN
    )
    ship_direction: str = request_utils.get_form_string(const.FORM_SHIP_DIRECTION)
    log.debug("ship_type: %s", form_ship_id)
    log.debug("ship_coordinate_row: %d", ship_coordinate_row)
    log.debug("ship_coordinate_column: %d", ship_coordinate_column)
    log.debug("ship_direction: %s", ship_direction)
    assert cookies_active_ship_id == form_ship_id

    validation.validate_is_not_empty_string(form_ship_id)
    validation.validate_is_correct_coordinate(ship_coordinate_row)
    validation.validate_is_correct_coordinate(ship_coordinate_column)
    validation.validate_is_not_empty_string(ship_direction)

    ctx.GAME_CONTROLLER_API.add_ship_to_field(
        session_id,
        cookies_player_id,
        form_ship_id,
        (ship_coordinate_row, ship_coordinate_column),
        ship_direction,
    )

    response: werkzeug.Response = flask.redirect(
        render_utils.url_for_session("_get_session_prepare_page", session_id)
    )
    log.debug("Response: %s", response)
    return response


@GAME_BLUEPRINT.route("/<string:session_id>/prepare/chose", methods=[const.METHOD_POST])
def _post_session_prepare_chose_ship_redirect_to_prepare_page(
    session_id: str,
) -> werkzeug.Response:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        werkzeug.Response: _description_
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_player_id)
    validation.validate_is_not_empty_string(cookies_session_id)

    assert cookies_session_id == session_id

    ship_id: str = request_utils.get_form_string(const.FORM_SHIP_ID)

    response: werkzeug.Response = flask.redirect(
        render_utils.url_for_session("_get_session_prepare_page", session_id)
    )
    response.set_cookie(const.COOKIE_SHIP_ID, ship_id)
    log.debug("Response: %s", response)
    return response


@GAME_BLUEPRINT.route(
    "/<string:session_id>/prepare/delship", methods=[const.METHOD_POST]
)
def _post_session_prepare_delship_redirect_to_prepare_page(
    session_id: str,
) -> werkzeug.Response:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        werkzeug.Response: _description_
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_player_id)
    validation.validate_is_not_empty_string(cookies_session_id)

    assert cookies_session_id == session_id

    ship_coordinate_row: int = request_utils.get_form_int(const.FORM_COORDINATE_ROW)
    ship_coordinate_column: int = request_utils.get_form_int(
        const.FORM_COORDINATE_COLUMN
    )
    log.debug("Ship Coordinate (%d, %d)", ship_coordinate_row, ship_coordinate_column)

    validation.validate_is_correct_coordinate(ship_coordinate_row)
    validation.validate_is_correct_coordinate(ship_coordinate_column)

    ctx.GAME_CONTROLLER_API.remove_ship_from_field(
        session_id, cookies_player_id, (ship_coordinate_row, ship_coordinate_column)
    )

    response: werkzeug.Response = flask.redirect(
        render_utils.url_for_session("_get_session_prepare_page", session_id)
    )
    log.debug("Response: %s", response)
    return response


@GAME_BLUEPRINT.route(
    "/<string:session_id>/gameplay/start", methods=[const.METHOD_POST]
)
def _post_session_gameplay_start_redirect_to_gameplay_page(
    session_id: str,
) -> werkzeug.Response:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        werkzeug.Response: _description_
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_session_id)

    assert cookies_session_id == session_id

    ctx.GAME_CONTROLLER_API.start_game(session_id, cookies_player_id)

    return flask.redirect(
        render_utils.url_for_session("_get_session_gameplay_page", session_id)
    )


@GAME_BLUEPRINT.route("/<string:session_id>/gameplay/shot", methods=[const.METHOD_POST])
def _post_session_gameplay_shot_redirect_to_gameplay_page(
    session_id: str,
) -> werkzeug.Response:
    """_summary_

    Args:
        session_id (str): _description_

    Returns:
        werkzeug.Response: _description_
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_player_id)
    validation.validate_is_not_empty_string(cookies_session_id)

    assert cookies_session_id == session_id

    ship_coordinate_row: int = request_utils.get_form_int(const.FORM_COORDINATE_ROW)
    ship_coordinate_column: int = request_utils.get_form_int(
        const.FORM_COORDINATE_COLUMN
    )
    log.debug("Ship Coordinate (%d, %d)", ship_coordinate_row, ship_coordinate_column)

    result: dto.ShotResultDto = ctx.GAME_CONTROLLER_API.make_shot(
        session_id, cookies_player_id, (ship_coordinate_row, ship_coordinate_column)
    )
    response: werkzeug.Response
    if result.is_finished:
        response = flask.redirect(
            render_utils.url_for_session("_get_session_finish_page", session_id)
        )
    else:
        response = flask.redirect(
            render_utils.url_for_session("_get_session_gameplay_page", session_id)
        )
    log.debug("Response: %s", response)
    return response
