from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import String
from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Capital(db.Model):
    __tablename__ = 'capital'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    identifier: Mapped[int]
    name: Mapped[str]

    def __repr__(self):
        return f"Name: {self.name}, Id: {self.identifier}"


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(25), nullable=False)

    def __repr__(self):
        return f"Id: {self.id}, Name: {self.username}"


class ShareHolderCredentials(db.Model):
    __tablename__ = 'share_holder_credentials'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_Id: Mapped[int]
    username: Mapped[str]
    password: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Client-ID: {self.client_Id}, Username: {self.username}"
