"""Gameplay requests controller.

Process requests to the next endpoints:
    - GET base_url/game/<string:session_id>/gameplay
        Returns gameplay page with players fields.
    - POST base_url/game/<string:session_id>/gameplay/start
        Starts the game for player and redirect to the gameplay page.
    - POST base_url/game/<string:session_id>/gameplay/shot
        Makes shot to opponent field and redirect to the gameplay page.

Raises:
    ex.ActivePlayerIsNotSetException: Raised when active player id is
        not set in the session.
"""
import logging

import flask
import werkzeug

import battleapi.api.dto as dto
import battleflask.app.context as ctx
import battleflask.app.controllers.constants as const
import battleflask.app.controllers.render_utils as render_utils
import battleflask.app.controllers.request_utils as request_utils
import battleflask.app.exceptions as ex
import battleflask.app.validation_utils as validation

log: logging.Logger = logging.getLogger(__name__)

GAME_PLAY_CONTROLLER: flask.Blueprint = flask.Blueprint(
    const.CONTROLLER_GAMEPLAY, __name__, template_folder="templates", url_prefix="/game"
)


@GAME_PLAY_CONTROLLER.route("/<string:session_id>/gameplay", methods=[const.METHOD_GET])
def _get_session_gameplay_page(session_id: str) -> str | werkzeug.Response:
    """Return gameplay page.

    Args:
        session_id (str): game session id.

    Raises:
        ex.ActivePlayerIsNotSetException: Raised if the active player is not set.

    Returns:
        str | werkzeug.Response: rendered game play page or redirect to the results page.
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    url_last: str = request_utils.get_cookies_string(const.COOKIE_LAST_URL)
    page_name: str = request_utils.get_cookies_string(const.COOKIE_LAST_PAGE)
    log.debug("cookies_player_id: %s", cookies_player_id)

    validation.validate_is_not_empty_string(cookies_player_id, "cookies_player_id")

    player: dto.PlayerDto = ctx.GAME_API.get_player_by_id(session_id, cookies_player_id)
    opponent: dto.PlayerDto = ctx.GAME_API.get_opponent(session_id, player.player_id)
    log.debug("Player: %s, opponent: %s", player, opponent)

    active_player: dto.PlayerDto | None = ctx.GAME_API.get_active_player(session_id)
    if active_player is None:
        raise ex.ActivePlayerIsNotSetException("Active pLayer is not set!")
    active_player_name: str = active_player.player_name
    log.debug("active_player_name: %s", active_player_name)
    number_of_cells_self: int = ctx.GAME_API.get_number_of_cells_left(
        session_id, cookies_player_id
    )
    number_of_cells_opponent: int = ctx.GAME_API.get_number_of_cells_left(
        session_id, opponent.player_id
    )
    log.debug(
        "Cells self: %d, Cells opponent: %d", number_of_cells_self, number_of_cells_self
    )
    player_field: list[list] = ctx.GAME_API.get_field(session_id, cookies_player_id)
    opponent_field: list[list] = ctx.GAME_API.get_field(
        session_id, opponent.player_id, is_for_opponent=True
    )
    log.debug("Player Field: %s", player_field)
    log.debug("Opponent Field: %s", opponent_field)

    result: dto.PlayerDto | None = ctx.GAME_API.get_winner(session_id)
    if result is not None:
        return render_utils.redirect_to_id_finish_page(session_id)
    is_opponent_ready: bool = opponent.is_ready
    return render_utils.render_gameplay_page(
        session_id=session_id,
        current_player_name=player.player_name,
        opponent_name=opponent.player_name,
        active_player_name=active_player_name,
        number_of_cells_self=number_of_cells_self,
        number_of_cells_opponent=number_of_cells_opponent,
        player_field=player_field,
        opponent_field=opponent_field,
        is_opponent_ready=is_opponent_ready,
        url_last_page_url=url_last,
        last_page_name=page_name,
    )


@GAME_PLAY_CONTROLLER.route(
    "/<string:session_id>/gameplay/start", methods=[const.METHOD_POST]
)
def _post_session_gameplay_start_redirect_to_gameplay_page(
    session_id: str,
) -> werkzeug.Response:
    """Process start game request and redirect to the gameplay.

    Args:
        session_id (str): game session id.

    Returns:
        werkzeug.Response: Redirect response.
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_session_id, "cookies_session_id")

    validation.validate_is_session_in_cookies_the_same(session_id, cookies_session_id)

    ctx.GAME_API.start_game(session_id, cookies_player_id)

    return render_utils.redirect_to_id_gameplay_page(session_id)


@GAME_PLAY_CONTROLLER.route(
    "/<string:session_id>/gameplay/shot", methods=[const.METHOD_POST]
)
def _post_session_gameplay_shot_redirect_to_gameplay_page(
    session_id: str,
) -> werkzeug.Response:
    """Process shot request and redirect to gameplay page.

    Args:
        session_id (str): game session id.

    Returns:
        werkzeug.Response: Redirect response.
    """
    cookies_player_id: str = request_utils.get_cookies_string(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request_utils.get_cookies_string(const.COOKIE_SESSION_ID)
    log.debug("cookies_player_id: %s", cookies_player_id)
    log.debug("cookies_session_id: %s", cookies_session_id)

    validation.validate_is_not_empty_string(cookies_player_id, "cookies_player_id")
    validation.validate_is_not_empty_string(cookies_session_id, "cookies_session_id")

    validation.validate_is_session_in_cookies_the_same(session_id, cookies_session_id)

    ship_coordinate_row: int = request_utils.get_form_int(const.FORM_COORDINATE_ROW)
    ship_coordinate_column: int = request_utils.get_form_int(
        const.FORM_COORDINATE_COLUMN
    )
    log.debug("Ship Coordinate (%d, %d)", ship_coordinate_row, ship_coordinate_column)

    result: dto.ShotResultDto = ctx.GAME_API.make_shot(
        session_id, cookies_player_id, (ship_coordinate_row, ship_coordinate_column)
    )
    response: werkzeug.Response
    if result.is_finished:
        response = render_utils.redirect_to_id_finish_page(session_id)
    else:
        response = render_utils.redirect_to_id_gameplay_page(session_id)
    log.debug("Response: %s", response)
    return response
