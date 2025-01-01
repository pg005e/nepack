from flask import current_app
from flaskr import create_app
from flaskr.models import Capital
from . import db
from MeroShareAPI import MeroShare


def populate_capital():
    app = create_app()

    with app.app_context():
        capitals = MeroShare.get_capital_details()
        for capital in capitals:
            capObj = Capital(
                code=capital['code'], identifier=capital['id'], name=capital['name'])
            db.session.add(capObj)
            db.session.commit()


if __name__ == "__main__":
    populate_capital()
