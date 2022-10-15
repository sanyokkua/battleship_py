import logging

import flask

import battleflask.app.controllers.render_utils as render_utils
from battleflask.app.controllers.constants import CONTROLLER_INDEX, METHOD_GET
import battleflask.app.controllers.request_utils as request_utils
import battleflask.app.controllers.constants as const

log: logging.Logger = logging.getLogger(__name__)

INDEX_CONTROLLER: flask.Blueprint = flask.Blueprint(
    CONTROLLER_INDEX, __name__, template_folder="templates"
)


@INDEX_CONTROLLER.route("/", methods=[METHOD_GET])
def _get_index_page() -> str:
    url_last: str = request_utils.get_cookies_string(const.COOKIE_LAST_URL)
    page_name: str = request_utils.get_cookies_string(const.COOKIE_LAST_PAGE)
    return render_utils.render_index_page(
        url_last_page_url=url_last, last_page_name=page_name
    )


@INDEX_CONTROLLER.route("/new", methods=[METHOD_GET])
def _get_new_game_page() -> str:
    url_last: str = request_utils.get_cookies_string(const.COOKIE_LAST_URL)
    page_name: str = request_utils.get_cookies_string(const.COOKIE_LAST_PAGE)
    return render_utils.render_new_game_page(
        url_last_page_url=url_last, last_page_name=page_name
    )


@INDEX_CONTROLLER.route("/join", methods=[METHOD_GET])
def _get_join_game_page() -> str:
    url_last: str = request_utils.get_cookies_string(const.COOKIE_LAST_URL)
    page_name: str = request_utils.get_cookies_string(const.COOKIE_LAST_PAGE)
    return render_utils.render_join_game_page(
        url_last_page_url=url_last, last_page_name=page_name
    )
