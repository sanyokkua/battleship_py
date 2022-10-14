import logging

import flask
import werkzeug

import battleapi.api.dto as dto
import battleapi.logic.utils as logic_utils
import battleflask.app.context as ctx
import battleflask.app.controllers.constants as const
import battleflask.app.controllers.render_utils as render_utils
import battleflask.app.controllers.request_utils as request_utils
import battleflask.app.controllers.utils as utils
import battleflask.app.validation_utils as validation

log: logging.Logger = logging.getLogger(__name__)

PREPARATION_CONTROLLER: flask.Blueprint = flask.Blueprint(
    const.CONTROLLER_PREPARATION,
    __name__,
    template_folder="templates",
    url_prefix="/game",
)


@PREPARATION_CONTROLLER.route(
    "/<string:session_id>/prepare", methods=[const.METHOD_GET]
)
def _get_session_prepare_page(session_id: str) -> str:
    cookie_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookie_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    cookie_ship_id: str = request_utils.get_cookies_string(const.COOKIE_SHIP_ID)
    cookie_ship_direction: str = request_utils.get_cookies_string(
        const.COOKIE_SHIP_DIRECTION
    )

    log.debug("value of cookie_player_id: %s", cookie_player_id)
    log.debug("value of cookie_session_id: %s", cookie_session_id)
    log.debug("value of cookie_ship_id: %s", cookie_ship_id)
    log.debug("value of cookie_ship_direction: %s", cookie_ship_direction)

    validation.validate_is_not_empty_string(cookie_player_id, "cookie_player_id")
    validation.validate_is_not_empty_string(cookie_session_id, "cookie_session_id")

    player: dto.PlayerDto = ctx.GAME_API.get_player_by_id(session_id, cookie_player_id)
    log.debug("Player: %s", player)

    opponent: dto.PlayerDto = ctx.GAME_API.get_opponent_prepare_status(
        session_id, cookie_player_id
    )
    log.debug("Opponent: %s", opponent)

    ships_list: list[dto.ShipDto] = ctx.GAME_API.get_prepare_ships_list(
        session_id, cookie_player_id
    )
    for ship in ships_list:
        if ship.ship_id == cookie_ship_id:
            ship.direction = cookie_ship_direction
    field: list[list[dto.CellDto]] = ctx.GAME_API.get_prepare_player_field(
        session_id, cookie_player_id
    )
    for row in field:
        for cell in row:
            if cell.has_ship:
                row = cell.row
                col = cell.col
                coordinates = logic_utils.get_neighbour_coordinates((row, col))
                for coord in coordinates:
                    c_row, c_col = coord
                    neighbour_cell = field[c_row][c_col]
                    if not neighbour_cell.has_ship:
                        neighbour_cell.is_not_available = True

    log.debug("Field: %s", field)

    render_ship_id = _get_ship_id(cookie_ship_id, ships_list)
    render_ship_direction = _get_ship_direction(cookie_ship_direction, ships_list)

    return render_utils.render_prepare_page(
        session_id=session_id,
        player_name=player.player_name,
        opponent_name=opponent.player_name,
        opponent_status=opponent.is_ready,
        ships_list=ships_list,
        field=field,
        active_ship=render_ship_id,
        active_ship_direction=render_ship_direction,
    )


def _get_ship_id(cookie_ship_id: str, ships: list[dto.ShipDto]) -> str:
    ship_id_from_ships_list: str = utils.get_ship_id(ships)
    render_ship_id: str = (
        cookie_ship_id if len(cookie_ship_id) > 0 else ship_id_from_ships_list
    )
    return render_ship_id


def _get_ship_direction(cookie_ship_direction: str, ships: list[dto.ShipDto]) -> str:
    ship_direction: str = utils.get_ship_direction(ships)
    render_ship_direction: str = (
        cookie_ship_direction if len(cookie_ship_direction) > 0 else ship_direction
    )
    return render_ship_direction


@PREPARATION_CONTROLLER.route(
    "/<string:session_id>/prepare/opponent", methods=[const.METHOD_GET]
)
def _get_session_prepare_opponent(session_id: str) -> str:
    current_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("value: %s", current_player_id)

    validation.validate_is_not_empty_string(current_player_id, "current_player_id")

    opponent: dto.PlayerDto = ctx.GAME_API.get_opponent(session_id, current_player_id)
    log.debug("Opponent: %s", opponent)
    return f"{opponent.player_name} is Ready: {opponent.is_ready}"


@PREPARATION_CONTROLLER.route(
    "/<string:session_id>/prepare/addship", methods=[const.METHOD_POST]
)
def _post_session_prepare_addship_redirect_to_prepare_page(
    session_id: str,
) -> werkzeug.Response:
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_ship_id: str = request_utils.get_cookies_string(const.COOKIE_SHIP_ID)
    cookies_ship_direction: str = request_utils.get_cookies_string(
        const.COOKIE_SHIP_DIRECTION
    )

    log.debug("value of cookies_session_id: %s", cookies_session_id)
    log.debug("value of cookies_player_id: %s", cookies_player_id)
    log.debug("value of cookies_ship_id: %s", cookies_ship_id)
    log.debug("value of cookies_ship_direction: %s", cookies_ship_direction)

    validation.validate_is_not_empty_string(cookies_session_id, "cookies_session_id")
    validation.validate_is_not_empty_string(cookies_player_id, "cookies_player_id")
    validation.validate_is_not_empty_string(cookies_ship_id, "cookies_ship_id")
    validation.validate_is_not_empty_string(
        cookies_ship_direction, "cookies_ship_direction"
    )
    validation.validate_is_session_in_cookies_the_same(session_id, cookies_session_id)

    form_coord_row: int = request_utils.get_form_int(const.FORM_COORDINATE_ROW)
    form_coord_col: int = request_utils.get_form_int(const.FORM_COORDINATE_COLUMN)

    log.debug("form_coord_row: %d", form_coord_row)
    log.debug("form_coord_col: %d", form_coord_col)

    validation.validate_is_correct_coordinate(form_coord_row, "form_coord_row")
    validation.validate_is_correct_coordinate(form_coord_col, "form_coord_col")

    try:
        ctx.GAME_API.add_ship_to_field(
            session_id,
            cookies_player_id,
            cookies_ship_id,
            (form_coord_row, form_coord_col),
            cookies_ship_direction,
        )
    except Exception as ex:
        log.warning(ex)

    response: werkzeug.Response = render_utils.redirect_to_id_prepare_page(session_id)
    _refresh_cookies_for_prepare_page(cookies_player_id, response, session_id)
    log.debug("Response: %s", response)
    return response


def _refresh_cookies_for_prepare_page(cookies_player_id, response, session_id):
    player: dto.PlayerDto = ctx.GAME_API.get_player_by_id(session_id, cookies_player_id)
    ships_list: list[dto.ShipDto] = ctx.GAME_API.get_prepare_ships_list(
        session_id, cookies_player_id
    )
    log.debug("Ships: %s", ships_list)
    ship_id: str = utils.get_ship_id(ships_list)
    ship_direction: str = utils.get_ship_direction(ships_list)
    response.set_cookie(const.COOKIE_PLAYER_ID, player.player_id)
    response.set_cookie(const.COOKIE_SESSION_ID, session_id)
    response.set_cookie(const.COOKIE_SHIP_ID, ship_id)
    response.set_cookie(const.COOKIE_SHIP_DIRECTION, ship_direction)


@PREPARATION_CONTROLLER.route(
    "/<string:session_id>/prepare/delship", methods=[const.METHOD_POST]
)
def _post_session_prepare_delship_redirect_to_prepare_page(
    session_id: str,
) -> werkzeug.Response:
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_session_id, "cookies_session_id")
    validation.validate_is_not_empty_string(cookies_player_id, "cookies_player_id")
    validation.validate_is_session_in_cookies_the_same(session_id, cookies_session_id)

    form_coord_row: int = request_utils.get_form_int(const.FORM_COORDINATE_ROW)
    form_coord_col: int = request_utils.get_form_int(const.FORM_COORDINATE_COLUMN)
    log.debug("Ship Coordinate (%d, %d)", form_coord_row, form_coord_col)

    validation.validate_is_correct_coordinate(form_coord_row, "form_coord_row")
    validation.validate_is_correct_coordinate(form_coord_col, "form_coord_col")

    try:
        ctx.GAME_API.remove_ship_from_field(
            session_id, cookies_player_id, (form_coord_row, form_coord_col)
        )
    except Exception as ex:
        log.warning(ex)

    response: werkzeug.Response = render_utils.redirect_to_id_prepare_page(session_id)
    _refresh_cookies_for_prepare_page(cookies_player_id, response, session_id)
    log.debug("Response: %s", response)
    return response


@PREPARATION_CONTROLLER.route(
    "/<string:session_id>/prepare/chose", methods=[const.METHOD_POST]
)
def _post_session_prepare_chose_ship_redirect_to_prepare_page(
    session_id: str,
) -> werkzeug.Response:
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    log.debug("value of cookies_player_id: %s", cookies_player_id)
    log.debug("value of cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_player_id, "cookies_player_id")
    validation.validate_is_not_empty_string(cookies_session_id, "cookies_session_id")
    validation.validate_is_session_in_cookies_the_same(session_id, cookies_session_id)

    form_ship_id: str = request_utils.get_form_string(const.FORM_SHIP_ID)
    form_ship_direction: str = request_utils.get_form_string(const.FORM_SHIP_DIRECTION)
    log.debug("form_ship_id: %d", form_ship_id)
    log.debug("form_ship_direction: %d", form_ship_direction)

    validation.validate_is_not_empty_string(form_ship_id, "form_ship_id")
    validation.validate_is_not_empty_string(form_ship_direction, "form_ship_direction")

    response: werkzeug.Response = render_utils.redirect_to_id_prepare_page(session_id)

    response.set_cookie(const.COOKIE_SHIP_ID, form_ship_id)
    response.set_cookie(const.COOKIE_SHIP_DIRECTION, form_ship_direction)
    log.debug("Response: %s", response)
    return response
