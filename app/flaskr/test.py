from flask import current_app
from . import create_app


def see_config():
    app = create_app()
    with app.app_context():
        content = current_app.config
        print((content))


if __name__ == "__main__":
    see_config()
