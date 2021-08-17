import sqlalchemy as db
from app.db.base_class import Base


class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True)
    phone_number = db.Column(db.Unicode(255), unique=True)
    first_name = db.Column(db.Unicode(255))
    middle_name = db.Column(db.Unicode(255))
    last_name = db.Column(db.Unicode(255))
    gender = db.Column(db.Unicode(1))
    birthday = db.Column(db.DateTime)
    email = db.Column(db.Unicode(255))
    password_hash = db.Column(db.Unicode(255))
    last_seen = db.Column(db.DateTime)
    joined_date = db.Column(db.DateTime)
    confirmed = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    avatar = db.Column(db.Unicode(255))
