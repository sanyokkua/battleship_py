import os

from flask import Flask

from battleflask.app.controllers import index_controller, game_controller


def configure_flask_app(application: Flask, test_config=None):
    key: str = os.environ["FLASK_APP_KEY"]
    app_key = key if key and len(key) > 0 else "development_key_tmp"

    application.config.from_mapping(SECRET_KEY=app_key)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass
    application.register_blueprint(index_controller.INDEX_BLUEPRINT)
    application.register_blueprint(game_controller.GAME_BLUEPRINT)
