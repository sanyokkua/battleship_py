import logging

import flask

import battleflask.app.controllers.render_utils as render_utils
from battleflask.app.controllers.constants import CONTROLLER_INDEX, METHOD_GET

log: logging.Logger = logging.getLogger(__name__)

INDEX_CONTROLLER: flask.Blueprint = flask.Blueprint(
    CONTROLLER_INDEX, __name__, template_folder="templates"
)


@INDEX_CONTROLLER.route("/", methods=[METHOD_GET])
def _get_index_page() -> str:
    return render_utils.render_index_page()


@INDEX_CONTROLLER.route("/new", methods=[METHOD_GET])
def _get_new_game_page() -> str:
    return render_utils.render_new_game_page()


@INDEX_CONTROLLER.route("/join", methods=[METHOD_GET])
def _get_join_game_page() -> str:
    return render_utils.render_join_game_page()
