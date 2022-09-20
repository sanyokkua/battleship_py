from flask import render_template, url_for

import battleflask.app.controllers.constants as const


def render_new_game_page(errors: list[str] | None = None) -> str:
    url_post_start_game_session: str = url_for(
        f"{const.BLUE_PRINT_GAME}._post_new_game_redirect_to_wait_for_players_page"
    )

    return render_template(
        "index/new_game_page.html",
        url_post_start_game_session=url_post_start_game_session,
        errors_list=errors,
    )


def render_join_game_page(errors: list[str] | None = None) -> str:
    url_join_game_session: str = url_for(
        f"{const.BLUE_PRINT_GAME}._post_join_game_redirect_to_game_field_page"
    )

    return render_template(
        "index/join_game_page.html",
        url_join_game_session=url_join_game_session,
        errors_list=errors,
    )


def render_wait_page(
    session_id: str, current_player_name: str, opponent_name: str
) -> str:
    url_get_update: str = url_for_session("_get_session_wait_page", session_id)
    url_get_prepare: str = url_for_session("_get_session_prepare_page", session_id)
    return render_template(
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
) -> str:
    url_post_start: str = url_for_session(
        "_post_session_gameplay_start_redirect_to_gameplay_page",
        session_id,
    )
    url_post_addship: str = url_for_session(
        "_post_session_prepare_addship_redirect_to_prepare_page",
        session_id,
    )
    url_post_delship: str = url_for_session(
        "_post_session_prepare_delship_redirect_to_prepare_page",
        session_id,
    )
    url_get_opponent: str = url_for_session("_get_session_prepare_opponent", session_id)
    return render_template(
        "game/game_session_prepare_page.html",
        url_post_start=url_post_start,
        url_post_addship=url_post_addship,
        url_post_delship=url_post_delship,
        url_get_opponent=url_get_opponent,
        current_player_name=current_player_name,
        opponent_status=opponent_status,
        ships_list=ships_list,
        field=field,
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
) -> str:
    url_post_shot: str = url_for_session(
        "_post_session_gameplay_shot_redirect_to_gameplay_page",
        session_id,
    )
    url_get_update: str = url_for_session("_get_session_gameplay_page", session_id)
    return render_template(
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
    )


def render_finish_page(session_id: str, winner_player_name: str) -> str:
    url_get_index: str = url_for(f"{const.BLUE_PRINT_INDEX}._get_index_page")
    return render_template(
        "game/game_session_finish_page.html",
        url_get_index=url_get_index,
        session_id=session_id,
        winner_player_name=winner_player_name,
    )


def url_for_session(method_name: str, session_id: str) -> str:
    return url_for(f"{const.BLUE_PRINT_GAME}.{method_name}", session_id=session_id)
