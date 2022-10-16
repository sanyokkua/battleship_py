"""Game common requests controller.

Process requests to the next endpoints:
    - GET base_url/game/<string:session_id>/wait
        Returns page with wait for player information.
    - GET base_url/game/<string:session_id>/finish
        Returns page with game results information.
Raises:
    ex.GameIsNotFinishedException: raised when winner was requested before game finished.
"""
import logging

import flask

import battleapi.api.dto as dto
import battleflask.app.context as ctx
import battleflask.app.controllers.constants as const
import battleflask.app.controllers.render_utils as render_utils
import battleflask.app.controllers.request_utils as request_utils
import battleflask.app.exceptions as ex
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
    """Return wait page.

    Args:
        session_id (str): game session id

    Returns:
        str: rendered template of wait page.
    """
    current_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    url_last: str = request_utils.get_cookies_string(const.COOKIE_LAST_URL)
    page_name: str = request_utils.get_cookies_string(const.COOKIE_LAST_PAGE)
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
        url_last_page_url=url_last,
        last_page_name=page_name,
    )


@GAME_COMMON_CONTROLLER.route("/<string:session_id>/finish", methods=[const.METHOD_GET])
def _get_session_finish_page(session_id: str) -> str:
    """Return game result page.

    Args:
        session_id (str): game session id.

    Raises:
        ex.GameIsNotFinishedException: raised if the game is not finished.

    Returns:
        str: rendered template of the finish page.
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    log.debug("current_player_id: %s", cookies_player_id)

    validation.validate_is_not_empty_string(cookies_player_id, "current_player_id")
    validation.validate_is_not_empty_string(
        request_utils.get_cookies_string(const.COOKIE_SESSION_ID),
        "check is in cookies: session_id",
    )
    winner_player: dto.PlayerDto = ctx.GAME_API.get_winner(session_id)
    log.debug("winner: %s", winner_player)

    if winner_player is None:
        raise ex.GameIsNotFinishedException("Winner information is not available!")

    player: dto.PlayerDto = ctx.GAME_API.get_player_by_id(session_id, cookies_player_id)
    opponent: dto.PlayerDto = ctx.GAME_API.get_opponent(session_id, player.player_id)
    player_field: list[list] = ctx.GAME_API.get_field(session_id, cookies_player_id)
    opponent_field: list[list] = ctx.GAME_API.get_field(
        session_id, opponent.player_id, is_for_opponent=True
    )
    return render_utils.render_finish_page(
        session_id,
        winner_player_name=winner_player.player_name,
        current_player_name=player.player_name,
        opponent_name=opponent.player_name,
        opponent_field=opponent_field,
        player_field=player_field,
    )
