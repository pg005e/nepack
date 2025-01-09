from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_login import LoginManager
import os


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)

    from . import models
    from . import auth
    from . import tradinguser
    app.register_blueprint(auth.bp)
    app.register_blueprint(tradinguser.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
