import logging

import flask
import werkzeug

import battleapi.api.dto as dto
import battleflask.app.context as ctx
import battleflask.app.controllers.constants as const
import battleflask.app.controllers.render_utils as render_utils
import battleflask.app.controllers.request_utils as request_utils
import battleflask.app.controllers.utils as utils
import battleflask.app.validation_utils as validation

log: logging.Logger = logging.getLogger(__name__)

PLAYERS_CONTROLLER: flask.Blueprint = flask.Blueprint(
    const.CONTROLLER_PLAYERS, __name__, template_folder="templates", url_prefix="/game"
)


@PLAYERS_CONTROLLER.route("/start", methods=[const.METHOD_POST])
def _post_start_redirect_to_wait_page() -> werkzeug.Response:
    player_name: str = request_utils.get_form_string(const.FORM_PLAYER_NAME)
    log.debug("player_name: %s", player_name)

    validation.validate_is_not_empty_string(player_name, "player_name")

    session_id: str = ctx.GAME_API.init_game_session()
    player: dto.PlayerDto = ctx.GAME_API.create_player_in_session(
        session_id, player_name
    )
    log.debug("Created session: %s, player: %s", session_id, player)

    ships_list: list[dto.ShipDto] = ctx.GAME_API.get_prepare_ships_list(
        session_id, player.player_id
    )
    log.debug("Ships: %s", ships_list)

    ship_id: str = utils.get_ship_id(ships_list)
    ship_direction: str = utils.get_ship_direction(ships_list)

    response: werkzeug.Response = render_utils.redirect_to_id_wait_page(session_id)
    response.set_cookie(const.COOKIE_PLAYER_ID, player.player_id)
    response.set_cookie(const.COOKIE_SESSION_ID, session_id)
    response.set_cookie(const.COOKIE_SHIP_ID, ship_id)
    response.set_cookie(const.COOKIE_SHIP_DIRECTION, ship_direction)
    log.debug("Response: %s", response)
    return response


@PLAYERS_CONTROLLER.route("/join", methods=[const.METHOD_POST])
def _post_join_redirect_to_prepare_page() -> werkzeug.Response:
    player_name: str = request_utils.get_form_string(const.FORM_PLAYER_NAME)
    session_id: str = request_utils.get_form_string(const.FORM_SESSION_ID)
    log.debug("player_name: %s", player_name)
    log.debug("session_id: %s", session_id)

    validation.validate_is_not_empty_string(player_name, "player_name")
    validation.validate_is_not_empty_string(session_id, "session_id")

    player: dto.PlayerDto = ctx.GAME_API.create_player_in_session(
        session_id, player_name
    )
    player_id: str = player.player_id
    log.debug("Created session: %s, player: %s", session_id, player)

    ships_list: list[dto.ShipDto] = ctx.GAME_API.get_prepare_ships_list(
        session_id, player_id
    )
    ships_list.sort(key=lambda obj: obj.ship_size)
    log.debug("Ships: %s", ships_list)
    ship_id: str = utils.get_ship_id(ships_list)
    ship_direction: str = utils.get_ship_direction(ships_list)

    response: werkzeug.Response = render_utils.redirect_to_id_prepare_page(session_id)
    response.set_cookie(const.COOKIE_PLAYER_ID, player.player_id)
    response.set_cookie(const.COOKIE_SESSION_ID, session_id)
    response.set_cookie(const.COOKIE_SHIP_ID, ship_id)
    response.set_cookie(const.COOKIE_SHIP_DIRECTION, ship_direction)
    log.debug("Response: %s", response)
    return response
