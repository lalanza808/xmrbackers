from datetime import datetime
from uuid import uuid4

from sqlalchemy.sql import func

from xmrbackers.factory import db
from xmrbackers import config


def rand_id():
    return uuid4().hex

class Creator(db.Model):
    __tablename__ = 'creators'

    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(db.String(80), primary_key=True, default=rand_id) # hex based id
    register_date = db.Column(db.DateTime, server_default=func.now())
    last_login_date = db.Column(db.DateTime, nullable=True)
    wallet_address = db.Column(db.String(150))
    password = db.Column(db.String(150))
    email = db.Column(db.String(150))
    handle = db.Column(db.String(150))

    def __repr__(self):
        return self.id

class Backer(db.Model):
    __tablename__ = 'backers'

    id = db.Column(db.Integer, primary_key=True)
