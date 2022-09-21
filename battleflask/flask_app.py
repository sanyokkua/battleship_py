"""Entry point module to run flask app."""
import logging

import flask

from battleflask.flask_app_config import configure_flask_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s %(funcName)s] %(message)s",
)

log: logging.Logger = logging.getLogger(__name__)

FLASK_APP: flask.Flask = flask.Flask(__name__)
configure_flask_app(FLASK_APP)


def run_app(debug=False, host="0.0.0.0") -> None:
    """Entry point to run the game.

    Args:
        debug (bool, optional): Flag to use debug mode. Defaults to False.
        host (str, optional): default host to expose server. Defaults to "0.0.0.0".
    """
    log.info("App is started with params: %s, %s", debug, host)
    FLASK_APP.run(host=host, debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
