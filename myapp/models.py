from datetime import datetime
from uuid import uuid4

from sqlalchemy.sql import func

from myapp.factory import db
from myapp import config


def rand_id():
    return uuid4().hex

class MyThing(db.Model):
    __tablename__ = 'swaps'

    # Meta
    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(db.String(80), primary_key=True, default=rand_id) # hex based id
    date = db.Column(db.DateTime, server_default=func.now())
    my_bool = db.Column(db.Boolean)
    my_int = db.Column(db.Integer)
    my_str = db.Column(db.String(150))
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.id

    def hours_elapsed(self):
        now = datetime.utcnow()
        if since_completed:
            if self.completed_date:
                diff = now - self.completed_date
            else:
                return 0
        else:
            diff = now - self.date
        return diff.total_seconds() / 60 / 60
