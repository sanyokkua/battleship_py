import logging

import flask

import battleapi.api.dto as dto
import battleflask.app.context as ctx
import battleflask.app.controllers.constants as const
import battleflask.app.controllers.render_utils as render_utils
import battleflask.app.controllers.request_utils as request_utils
import battleflask.app.validation_utils as validation

log: logging.Logger = logging.getLogger(__name__)

GAME_COMMON_CONTROLLER: flask.Blueprint = flask.Blueprint(
    const.CONTROLLER_GAME_COMMON,
    __name__,
    template_folder="templates",
    url_prefix="/game",
)


@GAME_COMMON_CONTROLLER.route("/<string:session_id>/wait", methods=[const.METHOD_GET])
def _get_session_wait_page(session_id: str) -> str:
    current_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("current_player_id: %s", current_player_id)

    validation.validate_is_not_empty_string(current_player_id, "current_player_id")
    validation.validate_is_not_empty_string(
        request_utils.get_cookies_string(const.COOKIE_SESSION_ID),
        "check is in cookies: session_id",
    )
    validation.validate_is_not_empty_string(
        request_utils.get_cookies_string(const.COOKIE_SHIP_ID),
        "check is in cookies: ship_id",
    )
    validation.validate_is_not_empty_string(
        request_utils.get_cookies_string(const.COOKIE_SHIP_DIRECTION),
        "check is in cookies: ship_direction",
    )

    player: dto.PlayerDto = ctx.GAME_API.get_player_by_id(session_id, current_player_id)
    opponent: dto.PlayerDto | None = ctx.GAME_API.get_opponent(
        session_id, player.player_id
    )
    log.debug("Player: %s, opponent: %s", player, opponent)
    opponent_name = opponent.player_name if opponent is not None else ""
    return render_utils.render_wait_page(
        session_id=session_id,
        player_name=player.player_name,
        opponent_name=opponent_name,
    )


@GAME_COMMON_CONTROLLER.route("/<string:session_id>/finish", methods=[const.METHOD_GET])
def _get_session_finish_page(session_id: str) -> str:
    winner_player: dto.PlayerDto = ctx.GAME_API.get_winner(session_id)
    log.debug("winner: %s", winner_player)
    return render_utils.render_finish_page(session_id, winner_player.player_name)
