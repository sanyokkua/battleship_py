from flask import Blueprint, make_response, redirect, render_template, request, url_for
from werkzeug import Response
import battleflask.app.controllers.constants as const
import battleflask.app.controllers.render_utils as render_utils
from battleflask.app.context import GAME_CONTROLLER as game
import battleflask.app.validation_utils as validation
import battleflask.app.exceptions as ex

GAME_BLUEPRINT: Blueprint = Blueprint(
    const.BLUE_PRINT_GAME, __name__, template_folder="templates", url_prefix="/game"
)


@GAME_BLUEPRINT.route("/start", methods=[const.METHOD_POST])
def _post_start_redirect_to_wait_page() -> Response:
    player_name: str = request.form[const.FORM_PLAYER_NAME]
    try:
        validation.validate_is_not_empty_string(player_name)
    except ex.IsEmptyStringException:
        return redirect(url_for(f"{const.BLUE_PRINT_INDEX}._get_new_game_page"))

    session_id: str = game.init_game_session()
    player = game.create_player_in_session(session_id, player_name)
    player_id: str = player.player_id

    rendered_template = redirect(
        render_utils.url_for_session("_get_session_wait_page", session_id)
    )
    resp = make_response(rendered_template)
    resp.set_cookie(const.COOKIE_PLAYER_ID, player_id)
    resp.set_cookie(const.COOKIE_SESSION_ID, session_id)
    return resp


@GAME_BLUEPRINT.route("/join", methods=[const.METHOD_POST])
def _post_join_redirect_to_prepare_page() -> Response:
    player_name: str = request.form[const.FORM_PLAYER_NAME]
    session_id: str = request.form[const.FORM_SESSION_ID]

    player = game.create_player_in_session(session_id, player_name)
    player_id: str = player.player_id

    rendered_template = redirect(
        render_utils.url_for_session("_get_session_prepare_page", session_id)
    )

    resp = make_response(rendered_template)
    resp.set_cookie(const.COOKIE_PLAYER_ID, player_id)
    resp.set_cookie(const.COOKIE_SESSION_ID, session_id)
    return resp


# GET


@GAME_BLUEPRINT.route("/<string:session_id>/wait", methods=[const.METHOD_GET])
def _get_session_wait_page(session_id: str) -> str:
    current_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)

    current_player_name: str = game.get_player_by_id(
        session_id, current_player_id
    ).player_name
    opponent_name: str = game.get_opponent(session_id, current_player_id).player_name

    return render_utils.render_wait_page(
        session_id=session_id,
        current_player_name=current_player_name,
        opponent_name=opponent_name,
    )


@GAME_BLUEPRINT.route("/<string:session_id>/prepare", methods=[const.METHOD_GET])
def _get_session_prepare_page(session_id: str) -> str:
    current_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)

    current_player_name: str = game.get_player_by_id(
        session_id, current_player_id
    ).player_name
    opponent_status: str = game.get_opponent_prepare_status(
        session_id, current_player_id
    )
    ships_list: list = game.get_prepare_ships_list(session_id, current_player_id)
    field: list[list] = game.get_prepare_player_field(session_id, current_player_id)

    return render_utils.render_prepare_page(
        session_id=session_id,
        current_player_name=current_player_name,
        opponent_status=opponent_status,
        ships_list=ships_list,
        field=field,
    )


@GAME_BLUEPRINT.route("/<string:session_id>/gameplay", methods=[const.METHOD_GET])
def _get_session_gameplay_page(session_id: str) -> str:
    current_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)

    current_player_name: str = game.get_player_by_id(
        session_id, current_player_id
    ).player_name
    opponent = game.get_opponent(session_id, current_player_id)
    active_player_name: str = game.get_active_player(session_id).player_name
    number_of_cells_self: int = game.get_number_of_cells_left(
        session_id, current_player_id
    )
    number_of_cells_opponent: int = game.get_number_of_cells_left(
        session_id, opponent.player_id
    )
    player_field: list[list] = game.get_field(session_id, current_player_id)
    opponent_field: list[list] = game.get_field(session_id, opponent.player_id)

    return render_utils.render_gameplay_page(
        session_id=session_id,
        current_player_name=current_player_name,
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
    current_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)
    opponent = game.get_opponent(session_id, current_player_id)
    return opponent.player_name


@GAME_BLUEPRINT.route("/<string:session_id>/finish", methods=[const.METHOD_GET])
def _get_session_finish_page(session_id: str) -> str:
    winner_player = game.get_winner(session_id)
    return render_utils.render_finish_page(session_id, winner_player.player_name)


@GAME_BLUEPRINT.route(
    "/<string:session_id>/prepare/addship", methods=[const.METHOD_POST]
)
def _post_session_prepare_addship_redirect_to_prepare_page(session_id: str) -> Response:
    cookies_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)

    assert cookies_session_id == session_id

    ship_type = request.form[const.FORM_SHIP_TYPE]
    ship_coordinate_row = request.form[const.FORM_COORDINATE_ROW]
    ship_coordinate_column = request.form[const.FORM_COORDINATE_COLUMN]
    ship_direction = request.form[const.FORM_SHIP_DIRECTION]

    game.add_ship_to_field(
        session_id,
        cookies_player_id,
        ship_type,
        (ship_coordinate_row, ship_coordinate_column),
        ship_direction,
    )

    rendered_template = redirect(
        render_utils.url_for_session("_get_session_prepare_page", session_id)
    )
    resp = make_response(rendered_template)
    return resp


@GAME_BLUEPRINT.route(
    "/<string:session_id>/prepare/delship", methods=[const.METHOD_POST]
)
def _post_session_prepare_delship_redirect_to_prepare_page(session_id: str) -> Response:
    cookies_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)

    assert cookies_session_id == session_id

    ship_coordinate_row = request.form[const.FORM_COORDINATE_ROW]
    ship_coordinate_column = request.form[const.FORM_COORDINATE_COLUMN]

    game.remove_ship_from_field(
        session_id, cookies_player_id, (ship_coordinate_row, ship_coordinate_column)
    )

    rendered_template = redirect(
        render_utils.url_for_session("_get_session_prepare_page", session_id)
    )
    resp = make_response(rendered_template)
    return resp


@GAME_BLUEPRINT.route(
    "/<string:session_id>/gameplay/start", methods=[const.METHOD_POST]
)
def _post_session_gameplay_start_redirect_to_gameplay_page(session_id: str) -> Response:
    cookies_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)

    assert cookies_session_id == session_id

    game.start_game(session_id)

    return redirect(
        render_utils.url_for_session("_get_session_gameplay_page", session_id)
    )


@GAME_BLUEPRINT.route("/<string:session_id>/gameplay/shot", methods=[const.METHOD_POST])
def _post_session_gameplay_shot_redirect_to_gameplay_page(session_id: str) -> Response:
    cookies_player_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)
    cookies_session_id: str = request.cookies.get(const.COOKIE_PLAYER_ID)

    assert cookies_session_id == session_id

    ship_coordinate_row = request.form[const.FORM_COORDINATE_ROW]
    ship_coordinate_column = request.form[const.FORM_COORDINATE_COLUMN]

    result = game.make_shot(
        session_id, cookies_player_id, (ship_coordinate_row, ship_coordinate_column)
    )

    if result.finished:
        redirect(render_utils.url_for_session("_get_session_finish_page", session_id))
    else:
        return redirect(
            render_utils.url_for_session("_get_session_gameplay_page", session_id)
        )
