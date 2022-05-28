import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace(
        "postgres", "postgresql", 1
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "swap_user"

    username = Column(String, primary_key=True)
    balance = Column(Float, nullable=False)
    swap_metadata = Column(JSONB, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            "username": self.username,
            "balance": self.balance,
            "swap_metadata": self.swap_metadata,
        }

    def __repr__(self) -> str:
        return super().__repr__()


class Investment(db.Model):
    __tablename__ = "investment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    coin = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "coin": self.coin,
            "amount": self.amount,
            "date": self.date,
        }

    def __repr__(self) -> str:
        return super().__repr__()


#  TODO Will need models for investments and users.
#  Investments: user id, coin name, initial amount, initial price
#  Users: username, password, balance
