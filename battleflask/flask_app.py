from flask import Flask

from battleflask.flask_app_config import configure_flask_app

FLASK_APP: Flask = Flask(__name__)
configure_flask_app(FLASK_APP)


def run_app(debug=False, host="0.0.0.0"):
    FLASK_APP.run(host=host, debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
