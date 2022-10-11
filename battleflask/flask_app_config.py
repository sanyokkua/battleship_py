"""Configuration of the Flask application."""
import os

from flask import Flask

from battleflask.app.controllers import (game_common, gameplay, index, players,
                                         preparation)


def configure_flask_app(application: Flask, test_config=None) -> None:
    """Configure flask application.

    Args:
        application (Flask): application to be configured.
        test_config (_type_, optional): test configuration. Defaults to None.
    """
    key: str = os.environ["FLASK_APP_KEY"]
    app_key = key if key and len(key) > 0 else "development_key_tmp"

    application.config.from_mapping(SECRET_KEY=app_key)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile("configs.py", silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass
    application.register_blueprint(index.INDEX_CONTROLLER)
    application.register_blueprint(players.PLAYERS_CONTROLLER)
    application.register_blueprint(game_common.GAME_COMMON_CONTROLLER)
    application.register_blueprint(preparation.PREPARATION_CONTROLLER)
    application.register_blueprint(gameplay.GAME_PLAY_CONTROLLER)
