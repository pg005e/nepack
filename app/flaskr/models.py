from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from . import db, login_manager

class Capital(db.Model):
    __tablename__ = 'capital'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    identifier = db.Column(db.Integer)
    name = db.Column(db.Text)

    def __repr__(self):
        return f"Name: {self.name}, Id: {self.identifier}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(8), unique=True, nullable=False)
    # fk to portfolios in the future

    __tableargs__ = (
        CheckConstraint('length(password) > 8', name='check_password_length')
    )

    def __repr__(self):
        return f"Id: {self.id}, Name: {self.username}"