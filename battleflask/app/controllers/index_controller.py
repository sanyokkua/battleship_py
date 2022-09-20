from flask import Blueprint, render_template, url_for

import battleflask.app.controllers.render_utils as render_utils
from battleflask.app.controllers.constants import BLUE_PRINT_INDEX, METHOD_GET

INDEX_BLUEPRINT: Blueprint = Blueprint(
    BLUE_PRINT_INDEX, __name__, template_folder="templates"
)


@INDEX_BLUEPRINT.route("/", methods=[METHOD_GET])
def _get_index_page() -> str:
    url_get_new_game_view: str = url_for(f"{BLUE_PRINT_INDEX}._get_new_game_page")
    url_get_join_game_view: str = url_for(f"{BLUE_PRINT_INDEX}._get_join_game_page")

    return render_template(
        "index/index_page.html",
        url_get_new_game_view=url_get_new_game_view,
        url_get_join_game_view=url_get_join_game_view,
    )


@INDEX_BLUEPRINT.route("/new", methods=[METHOD_GET])
def _get_new_game_page() -> str:
    return render_utils.render_new_game_page()


@INDEX_BLUEPRINT.route("/join", methods=[METHOD_GET])
def _get_join_game_page() -> str:
    return render_utils.render_join_game_page()
