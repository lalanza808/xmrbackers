from datetime import datetime
from uuid import uuid4

import peewee as pw
from peewee import PostgresqlDatabase, SQL, ForeignKeyField

from xmrbackers import config


db = PostgresqlDatabase(
    config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
)

def rand_id():
    return uuid4().hex


class Creator(pw.Model):
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    wallet_address = pw.CharField()
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=True)
    bio = pw.CharField()

    class Meta:
        database = db


class Backer(pw.Model):
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.now)
    last_login_date = pw.DateTimeField(default=datetime.now)
    wallet_address = pw.CharField()
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=True)

    class Meta:
        database = db
